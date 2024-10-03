from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    detail = None
    status_code = None

    def __init__(self, detail, code):
        super().__init__(detail, code)
        self.detail = detail
        self.status_code = code
        
class FailedToCreateOrGetVote(BaseCustomException):
    def __init__(self, detail):
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class FailedToGetPlan(BaseCustomException):
   def __init__(self, detail):
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
class FailedToUpdateVoteRecords(BaseCustomException):
   def __init__(self, detail):
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR) 

class FailedToVote(BaseCustomException):
   def __init__(self, detail):
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        
class FailedToGetPlans(BaseCustomException):
   def __init__(self, detail):
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
class FailedToGetVotesRecord(BaseCustomException):
   def __init__(self, detail):
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
class FailedToGetVote(BaseCustomException):
   def __init__(self, detail):
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR) 

class FailedToGetResults(BaseCustomException):
   def __init__(self, detail):
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR) 