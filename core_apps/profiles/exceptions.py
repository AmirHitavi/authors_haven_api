from rest_framework.exceptions import APIException


class CantFollowYourself(APIException):
    status_code = 403
    default_code = "forbidden"
    default_detail = "You can't follow yourself."
