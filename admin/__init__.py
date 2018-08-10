"""
为了防止db循环调用
将db在仅初始化时调用的admin中注册
"""

from flask_admin import Admin, AdminIndexView
from flask_mongoengine import MongoEngine
from flask import Flask, url_for, redirect, render_template, request, make_response

from wtforms import form, fields, validators
from flask_restful import Resource
import flask_login as login
from flask_admin.contrib.mongoengine import ModelView

db = MongoEngine()


class User(db.Document):

    username = db.StringField(max_length=80, unique=True)
    email = db.StringField(max_length=120)
    password = db.StringField(max_length=64)

    # Flask-Login integration
    # NOTE: is_authenticated, is_active, and is_anonymous
    # are methods in Flask-Login < 0.3.0
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    # Required for administrative interface
    def __unicode__(self):
        return self.username


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    username = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User.objects(login=self.username.data).first()


class RegistrationForm(form.Form):
    username = fields.StringField(validators=[validators.required()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if User.objects(login=self.username.data):
            raise validators.ValidationError('Duplicate username')


# Create customized model view class
class MyModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated


# Create customized index view class
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_authenticated


# Flask views
# @app.route('/')

class Index(Resource):
    def get(self):
        return make_response(render_template('index.html'))


class Login_View(Resource):
    def __init__(self):
        self.form = LoginForm(request.form)

    def get(self):
        return make_response(render_template('form.html', form=self.form))

    def post(self):
        if self.form.validate():
            user = self.form.get_user()
            login.login_user(user)
            return redirect(url_for('index'))
        return make_response(render_template('form.html', form=self.form))


class Register_View(Resource):

    def __init__(self):
        self.form = RegistrationForm(request.form)

    def get(self):
        return make_response(render_template('form.html', form=self.form))

    def post(self):

        if self.form.validate():
            user = User()

            self.form.populate_obj(user)
            user.save()

            login.login_user(user)
            return redirect(url_for('index'))
        return make_response(render_template('form.html', form=self.form))


class Logout_View(Resource):

    def get(self):
        login.logout_user()
        return redirect(url_for('index'))


admin = Admin(
    index_view=MyAdminIndexView(),
    name=u"课程管理系统"
)
