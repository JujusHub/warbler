from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image_url = StringField('Image URL', validators=[Length(max=255)])
    header_image_url = StringField('Header Image URL', validators=[Length(max=255)])
    bio = StringField('Bio', validators=[Length(max=500)])
    password = PasswordField('Password', validators=[DataRequired()])
