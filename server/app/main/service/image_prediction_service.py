from app.main.service.image_save_service import image_save
from app.main.util.apiresponse import apiResponse

from flask import  request
import numpy as np
import cv2
from app.main.config import face_cascade,eye_cascade
import pywt
import json
import joblib
import os

def get_cropped_image_if_2_eyes(image_path):
    img=cv2.imread(image_path)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.3,5)
    if len(faces) == 0:
        return 0
    return_rois=[]
    for x,y,w,h in faces:
        # face_image=cv2.rectangle(img,(x,y), (x+w,y+h),(255,0,0),2)
        roi_gray=gray[y: y+h, x: x+w]
        # roi_color=face_image[y:y+h, x: x+w]
        roi_color=img[y:y+h, x: x+w]
        eyes=eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >=2:
            return_rois.append(roi_color)
    return return_rois

def w2d(img,mode='haar', level=1):
    imArray=img

    imArray=cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    print(imArray.shape)
    imArray=np.float32(imArray)
    
    imArray/=255
    
    coeffs=pywt.wavedec2(imArray,mode, level=level)

    coeffs_H=list(coeffs)
    coeffs_H[0]*=0

    imArray_H=pywt.waverec2(coeffs_H,mode)
    imArray_H*=255
    imArray_=np.uint8(imArray_H)

    return imArray_

def load_saved_artifacts():
    with open('./artifact/celebrity_class_dictionary.json', 'r') as f:
        class_name_to_number=json.load(f)
        class_number_to_name={v:k for k,v in class_name_to_number.items() }

    with open('./artifact/celebrity_detection_model.pkl', 'rb') as f:
        model=joblib.load(f)

    return class_name_to_number, class_number_to_name, model

def celebrity_image_classification(new_request):
    try:
        image_path, message=image_save(new_request)
        if message:
            return apiResponse(False, message), 400
        cropped_images=get_cropped_image_if_2_eyes(image_path)
        if cropped_images == 0:
            return apiResponse(False, 'Face Not Found'),400
        combined_imgs=[]
        for cropped_image in cropped_images:
            print(cropped_image.shape)
            img_har=w2d(cropped_image)
            scalled_img_har=cv2.resize(img_har,(32,32))
            scalled_raw_img=cv2.resize(cropped_image,(32,32))
            combined_imgs.append(np.vstack((scalled_raw_img.reshape(32*32*3,1), scalled_img_har.reshape(32*32,1))))
        final=[]
        len_image_array=32*32*3 + 32*32
        for combined_img in combined_imgs:
            final.append(combined_img.reshape(1,len_image_array).astype(float))

        name_to_number, number_to_name, model= load_saved_artifacts()

        results=[]
        for img in final:
            prediction=model.predict(img)[0]
            results.append(prediction)

        results=list(set(results))

        names=[]
        if len(results) > 0:
            msg=''
            for result in results:
                msg=msg + number_to_name[result].replace('_', ' ').capitalize() + ', '
                names.append(number_to_name[result])

            msg=msg[:-2]
            msg=msg.replace(',', ' and')
            msg=msg + ' Found in the given Image'

        else:
            msg='Unknown Face Found'

        os.remove(image_path)
        return apiResponse(True,msg,{'faces': names}),200

    except Exception as e:
        return apiResponse(False,'Error occured', None, str(e)), 500