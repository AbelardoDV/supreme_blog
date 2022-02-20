from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(label='Username',validators=[DataRequired('Username es obligatorio')])
    password = PasswordField(label='Password',validators=[DataRequired()],render_kw={'autocomplete':'on'})
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label='Sign In')
