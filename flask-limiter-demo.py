from flask import Flask, request, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)


"""
默认的限制器
key_func参数是判断函数,表示以何种条件判断算一次访问?这里使用的是get_remote_address,此函数返回的是客户端的访问地址.
default_limits 是一个数组,用于依次提同判断条件.比如100/day是指一天100次访问限制.
常用的访问限制字符串格式如下:
10 per hour
10/hour
10/hour;100/day;2000 per year
100/day, 500/7days
注意默认的限制器对所有视图都有效,除非你自定义一个限制器用来覆盖默认限制器,或者使用limiter.exempt装饰器来取消限制
"""
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["100/day, 2/minute, 1/second"])


@limiter.request_filter
def filter_func():
    """
    定义一个限制器的过滤器函数,如果此函数返回True,
    则不会施加任何限制.一般用这个函数创建访问速度
    限制的白名单,可以使用某些celeb集中处理需要
    limiter.exempt的情况
    """
    path_url = request.path
    white_list = ['/exempt']
    if path_url in white_list:
        return True
    else:
        return False


@app.route('/')
@limiter.exempt                               # 取消默认限制器
def hello_world():
    return render_template("login.html")


@app.route("/exempt")
def exempt_func():
    """此视图函数被过滤器忽略"""
    return "no limited"


@app.route('/h1', methods=['post', 'get'])
# 自定义限制器覆盖了默认限制器
@limiter.limit("100/day;10/hour;3/minute")
def h1_func():
    return "h1"


def get_key():
    """自定义的key_fun函数"""
    return request.host_url


@app.route('/h2', methods=['post', 'get'])
# 自定义限制器覆盖了默认限制器,同时自定义了key_func函数
@limiter.limit(limit_value="100/day;10/hour;3/minute", key_func=get_key)
def h2_func():
    return "h2"


@app.route('/h3', methods=['post', 'get'])
# 自定义限制器覆盖了默认限制器,参数说明如下:
# 1. param limit_value: 访问限制阈值
# 1. param exempt_when: 例外条件  (限制器只对使用不带debug访问的请求生效)
# 2. param error_message: 错误的返回信息(注意,暂不支持中文,如果使用中文,请自定义错误页)
# 3. param methods: 对哪些方法启用限制器?
@limiter.limit(limit_value="1/minute",
               exempt_when=lambda: request.args.get("debug") is not None or request.form.get("debug") is not None,
               error_message="request be rejected",
               methods=['get'])
def h3_func():
    return "h3"


"""共享限制次数的限制器"""
shared_limiter = limiter.shared_limit(limit_value="7/minute", scope="aaa")


@app.route("/s1")
# 和s2_func视图共享shared_limiter的限制阈值
@shared_limiter
def s1_func():
    return "s1"


@app.route("/s2")
# 和s1_func视图共享shared_limiter的限制阈值
@shared_limiter
def s2_func():
    return "s2"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5011, debug=True)
