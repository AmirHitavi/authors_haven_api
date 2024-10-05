from rest_framework.exceptions import APIException


class CantFollowYourself(APIException):
    status_code = 403
    default_code = "forbidden"
    default_detail = "You can't follow yourself."


class CantFollowYourFollower(APIException):
    status_code = 400
    default_code = "forbidden"
    default_detail = "You can't follow your followers."


class CantUnfollowYourself(APIException):
    status_code = 403
    default_code = "forbidden"
    default_detail = "You can't unfollow yourself."


class CantUnfollowNotYourFollower(APIException):
    status_code = 400
    default_code = "forbidden"
    default_detail = "You can't unfollow someone who is not your follower."
