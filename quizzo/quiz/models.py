from quiz import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from datetime import datetime

start = datetime(2021, 4, 21)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key = True)
    roll = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    q_level = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=20)

    def __init__(self, roll, username, password):
        self.roll = roll
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"{self.roll},{self.username}"


class Question(db.Model):
    qid = db.Column(db.Integer, primary_key=True)
    question =db.Column(db.String, nullable=False)
    option1 = db.Column(db.String, nullable=False)
    option2 = db.Column(db.String, nullable=False)
    option3 = db.Column(db.String, nullable=False)
    option4 = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)

    def __init__(self, question, option1, option2, option3, option4, answer):
        self.question=question
        self.option1=option1
        self.option2=option2
        self.option3=option3
        self.option4=option4
        self.answer=answer

    def __repr__(self):
        return f"{self.question},{self.option1},{self.option2},{self.option3},{self.option4},{self.answer}"
