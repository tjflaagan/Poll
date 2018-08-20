from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class GetPoll(Form):
    poll_id = StringField('Poll ID', validators=[DataRequired()])
    submit = SubmitField('Go to poll')