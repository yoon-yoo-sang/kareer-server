# Description: 이 파일은 오류 메시지를 정의하는 파일입니다.

# Not Found
OBJECT_DOES_NOT_EXIST = "Object가 존재하지 않음"

# Invalid
EMAIL_OR_PASSWORD_INCORRECT = "이메일 또는 비밀번호가 올바르지 않습니다"

# Already Exists
AUTH_USER_ALREADY_EXISTS = "User는 이미 존재함"
EMAIL_ALREADY_EXISTS = "이미 가입된 이메일입니다"
USER_PROFILE_ALREADY_EXISTS = "UserProfile은 이미 존재함"
USER_SETTING_ALREADY_EXISTS = "UserSetting은 이미 존재함"


class CrawlError(Exception):
    """
    크롤링 에러를 나타내는 예외 클래스입니다.
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message
