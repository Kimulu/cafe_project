from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,BooleanField
from wtforms.validators import DataRequired, URL

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

class Create_Cafe_Form(FlaskForm):
    name =StringField("Name", validators=[DataRequired()])
    city= StringField("City", validators=[DataRequired()])
    description = StringField("description", validators=[DataRequired()])
    image = StringField("image Url", validators=[DataRequired()])
    wifi = BooleanField("Does the place have Wifi?", default=True,validators=[DataRequired()],false_values=None)
    power_outlets = BooleanField("Does the place have power outlets?",default=True, validators=[DataRequired()],false_values=None)
    submit = SubmitField("Add Cafe")
