from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Email

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=4, max=20, message='Имя пользователя должно быть от 4 до 20 символов.'),
        Regexp('^[a-zA-Z0-9]+$', message='Имя пользователя может содержать только буквы и цифры.')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Введите корректный адрес электронной почты.')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=6, max=50, message='Пароль должен быть от 6 до 50 символов.'),
        Regexp('^[a-zA-Z0-9]+$', message='Пароль может содержать только буквы и цифры.')
    ])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')