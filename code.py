from captcha.image import ImageCaptcha
from random import random
from flask import Flask, Response, request, session
import gvcode, os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


def captcha():
    image = ImageCaptcha()
    x = int(round(random() * 10000))
    if x < 1000:
        x += 1000
    return image.generate(str(x), 'png')


def get_code():
    base64_str, code = gvcode.base64()

    # 把code存到session中
    session['verify_code'] = code
    # 把base64_str 返回给用户
    return str(base64_str, "utf-8")


def user_login():
    if request.method == 'POST':
        # 获得用户输入的验证码
        user_code = request.get_json['code'].lower()
        print('user_code',user_code)
        # 获取实际的验证码
        act_code = request.session.get('verify_code').lower()
        print('act_code',act_code)
        # #进行验证
        if user_code == act_code:
            return '验证成功'
    return 'ok'


@app.route('/', methods=["GET"])
def index():
    code = get_code()
    return """
    <img src=" data:image/jpeg;base64,%s">
    """ % code


if __name__ == "__main__":
    app.run(debug=True)
