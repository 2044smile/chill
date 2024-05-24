from rest_framework.exceptions import APIException


# 수강생 인원 초과
class OvercapacityOfStudents(APIException):
    status_code = 403
    default_detail = 'The maximum number of students who can attend has been exceeded.'


# 종료 된 강의장
class TerminatedHall(APIException):
    status_code = 410
    default_detail = 'A lecture hall that has been terminated'


# 본인이 작성한 강의에 등록 불가
class TakeYourOwnCourse(APIException):
    status_code = 400
    default_detail = 'You cannot enroll in a lecture you have created'


class HallNotFound(APIException):
    status_code = 404
    default_detail = 'Hall not found'


class X_USER_IDOrX_ROOM_IDNotFound(APIException):
    status_code = 400
    default_detail = 'Invalid X-ROOM-ID or X-USER-ID'
