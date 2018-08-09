import jwt, datetime, time
from flask import jsonify, current_app


class Auth():

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            data = jwt.decode(auth_token, current_app.config["SECRET_KEY"], options={'verify_exp': False})
            user = {}
            userInfo = {
                "id": data["id"],
                "name": data["name"],
                "openid": data["openid"],
                "unionid": data["unionid"]
            }

            return True, userInfo
        except jwt.ExpiredSignatureError:
            return False, 'Token过期'
        except jwt.InvalidTokenError:
            return False, '无效Token'
        except KeyError:
            return False, user
