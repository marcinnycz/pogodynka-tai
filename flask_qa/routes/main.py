from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

import requests
import json

from flask_qa.extensions import db
from flask_qa.models import Question, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    questions = Question.query.filter(Question.answer != None).all()

    favourites = ["London", "Quebec"]

    context = {
        'questions' : questions,
        'favourites' : favourites
    }

    return render_template('home.html', **context)

@main.route('/weather', methods=['GET'])
@login_required
def weather():

    #Get favourite places data
    fav1 = {
        'lat': '10',
        'lon': '10'
    }
    fav2 = {
        'lat': '10',
        'lon': '10'
    }
    favourites = [(fav1, 'Londyn'), (fav2, 'Quebec')]

    #Initialize list
    weather = []

    #Get data from api
    for f in favourites:
        #weather.append(f)
        payload = {'lat': f[0]["lat"], 'lon': f[0]["lon"], 'appid': 'b7f46f673b72edc826d89c62775cb19b', 'units': 'metric'}
        dataJSON = requests.get('https://api.openweathermap.org/data/2.5/weather', params=payload).content
        data = json.loads(dataJSON)
        weather.append((data, f[1]))

    #Prepare data for HTML
    context = {
        'weather' : weather
    }

    #Render
    return render_template('currentWeather.html', **context)

@main.route('/answer/<int:question_id>', methods=['GET', 'POST'])
@login_required
def answer(question_id):
    if not current_user.expert:
        return redirect(url_for('main.index'))

    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        question.answer = request.form['answer']
        db.session.commit()

        return redirect(url_for('main.unanswered'))

    context = {
        'question' : question
    }

    return render_template('answer.html', **context)

@main.route('/question/<int:question_id>')
def question(question_id):
    question = Question.query.get_or_404(question_id)

    context = {
        'question' : question
    }

    return render_template('question.html', **context)

@main.route('/unanswered')
@login_required
def unanswered():
    if not current_user.expert:
        return redirect(url_for('main.index'))

    unanswered_questions = Question.query\
        .filter_by(expert_id=current_user.id)\
        .filter(Question.answer == None)\
        .all()

    context = {
        'unanswered_questions' : unanswered_questions
    }

    return render_template('unanswered.html', **context)

@main.route('/users')
@login_required
def users():
    if not current_user.admin:
        return redirect(url_for('main.index'))

    users = User.query.filter_by(admin=False).all()

    context = {
        'users' : users
    }

    return render_template('users.html', **context)

@main.route('/promote/<int:user_id>')
@login_required
def promote(user_id):
    if not current_user.admin:
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)

    user.expert = True
    db.session.commit()

    return redirect(url_for('main.users'))

@main.route('/add_favourite', methods=['GET', 'POST'])
@login_required
def add_favourite():
    if request.method == 'POST':
        name = request.form['name']
        lat = request.form['lat']
        lat = request.form['lon']

        # -------------------------------------------------------------------- TO DO -------------------------------------------------------

        # #Create database entry
        # favourite = Favourite(
        #     name=name, 
        #     lat=lat,
        #     lon=lon
        # )

        # #Add to database
        # db.session.add(favourite)
        # db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('addFavourite.html')    