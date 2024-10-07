from rest_framework.exceptions import APIException


class YouAlreadyHaveBookmarked(APIException):
    status_code = 400
    default_detail = "You already have bookmarked the article."
    default_code = "bad_request"
