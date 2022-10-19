from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .models import User


class LoginForm(FlaskForm):
	email = EmailField('Email', 
			validators=[DataRequired(), Email()])
	password = PasswordField('Password',
			validators=[DataRequired(), Length(min=4)])
	remember = BooleanField('Remember')
	submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
	name = StringField('Name', 
			validators=[DataRequired()])
	email = EmailField('Email', 
			validators=[DataRequired(), Email()])
	password = PasswordField('Password', 
			validators=[DataRequired(), Length(min=4)])
	check_password = PasswordField('Check Password', 
			validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')
	
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Account already exists for this email")

