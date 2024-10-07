from rest_framework.exceptions import APIException


class YouAlreadyClapped(APIException):
    status_code = 400
    default_detail = "You already clapped the article"
    default_code = "bad_request"
