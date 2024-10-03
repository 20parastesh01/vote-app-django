from rest_framework.views import exception_handler
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        response.data['message'] = 'Validation error occurred.'
        response.data['code'] = response.status_code
    elif response is not None:
        if 'detail' in response.data:
            response.data['message'] = response.data['detail']
            response.data['code'] = response.status_code
            del response.data['detail']
        else:
            response.data['message'] = 'An unexpected error occurred.'
            response.data['code'] = response.status_code
    else:
        response = Response(
            {'message': 'An unexpected error occurred.', 'code': 500},
            status=500
        )

    return response