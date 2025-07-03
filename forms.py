from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Label
from wtforms.validators import DataRequired, Length


class EditPasswordForm(FlaskForm):
    site_username = StringField('Site Username', validators=[
                                DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    masterkey = PasswordField('Masterkey Confirmation',
                              validators=[DataRequired()])
    submit = SubmitField("Update")
