from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,IntegerField,FileField,BooleanField
from wtforms.validators import DataRequired, length, ValidationError

from flask_wtf.file import FileRequired
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя',validators=[DataRequired()])
    password = PasswordField('Пароль')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

