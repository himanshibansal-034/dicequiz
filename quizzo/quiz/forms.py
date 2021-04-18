from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError
from quiz.models import User

class LoginForm(FlaskForm):
    roll = StringField('Roll Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    roll = IntegerField('Roll Number', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message="Passwords must Match!")])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_roll(self,roll):
        if User.query.filter_by(roll=self.roll.data).first():
            raise ValidationError("Roll Number already registered!")

    def validate_username(self,username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username already registered!")

class QuestionForm(FlaskForm):
    question = StringField('Question',validators=[DataRequired()])
    option1 = StringField('option1',validators=[DataRequired()])
    option2 = StringField('option2',validators=[DataRequired()])
    option3 = StringField('option3',validators=[DataRequired()])
    option4 = StringField('option4',validators=[DataRequired()])
    answer = StringField('answer',validators=[DataRequired()])
    submit = SubmitField('Submit')

class Restart(FlaskForm):
    submit=SubmitField('Restart')

class RollForm(FlaskForm):
    submit = SubmitField('Roll')
