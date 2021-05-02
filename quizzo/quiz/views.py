from flask import render_template, request, Blueprint, redirect, url_for, flash, abort, session
from quiz import app,db
from flask_login import login_user, login_required, logout_user, current_user
from quiz.models import User, Question
from quiz.forms import LoginForm, RegistrationForm, QuestionForm, RollForm
import math, random
from datetime import datetime, timedelta

start=datetime(2021, 5, 2, 23, 35, 00 )
end=datetime(2021, 5, 2, 23, 55, 00)

my_view=Blueprint('my_view',__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(roll=form.roll.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(roll=form.roll.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            next=request.args.get('next')
            if next==None or not not next[0]=='/':
                next=url_for('index')
            return redirect(next)

        else:
            flash("Username or Password is incorrect!")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/quesupload', methods=['POST','GET'])
@login_required
def quesupload():
    form = QuestionForm()

    if form.validate_on_submit():
        ques = Question(question=form.question.data,
                         option1=form.option1.data,
                         option2=form.option2.data,
                         option3=form.option3.data,
                         option4=form.option4.data,
                         answer=form.answer.data)
        db.session.add(ques)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('qupload.html', form=form)


@app.route('/quiz', methods=['GET','POST'])
@login_required
def quiz():
    remaining=end-datetime.now()
    inttime=int(remaining.total_seconds())
    session["max"]=int((end-start).total_seconds())
    session["mins"]=math.floor(inttime/60)
    session["secs"]=inttime-session["mins"]*60;
    session["exercise"]=inttime
    questions = Question.query.all()
    if current_user.q_level>=20:
        return redirect('results')
    if int(remaining.total_seconds())<=0:
        return redirect('results')
    if datetime.now()<start:
        return redirect('/')
    ques=questions[current_user.q_level]
    current_user.points-=1
    db.session.commit()
    die_val=0
    die_1=random.randint(1,6)
    die_2=random.randint(1,6)
    return render_template('quiz.html', ques= ques, die_1=die_1, die_2=die_2, die_tot=die_1+die_2)

@app.route('/check_<ans>_<int:point>')
@login_required
def check(ans,point):
    ques=Question.query.filter_by(qid=current_user.q_level+1).first()
    if ans == ques.answer :
        current_user.q_level+=1
        current_user.points+=point
        message="Hooray! You got that right."
    else:
        current_user.q_level+=1
        current_user.points-=point
        message="Alas! That was a wrong choice."

    db.session.commit()
    flash(message)
    return redirect('quiz')

@app.route('/results', methods=['GET','POST'])
@login_required
def results():
    return render_template('results.html')

@app.route('/leaderboard')
def leaderboard():
    if datetime.now()<datetime(2021, 5, 16, 21, 00, 00):
        return render_template("awaiting.html")
    users=User.query.order_by(User.points.desc()).all()
    return render_template('leaderboard.html',users=users)

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')
