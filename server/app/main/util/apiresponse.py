def apiResponse(success,message,data=None,error=None):
    return {success: success, 'data': data, 'message': message, 'error': error,}