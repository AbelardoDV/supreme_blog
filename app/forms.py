from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField,\
    SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email
from app.models import User


class PostForm(FlaskForm):
    body = TextAreaField(label='Write a post:', validators=[DataRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[
                           DataRequired('Username es obligatorio')])
    password = PasswordField(label='Password', validators=[
                             DataRequired()], render_kw={'autocomplete': 'on'})
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label='Sign In')


class EmptyForm(FlaskForm):
    submit = SubmitField()


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[
                           DataRequired('Username es obligatorio')])
    email = EmailField(label='email', validators=[DataRequired(), Email()])
    password = PasswordField(label='password', validators=[DataRequired()])
    password2 = PasswordField(label='repeat password', validators=[
                              DataRequired(), EqualTo('password',
                                                      'password not match')])
    submit = SubmitField(label='Register')

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('username in use')

    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError('email in ise')
