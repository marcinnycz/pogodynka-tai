from flask_qa import variables

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required


from datetime import datetime
import requests
import json

from flask_qa.extensions import db
from flask_qa.models import User, Favorite

main = Blueprint('main', __name__)

@main.route('/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    if not current_user or not current_user.admin:
        return redirect(url_for('main.index'))

    fav = Favorite.query.filter_by(user_id=user_id).first()
    while fav:
        db.session.delete(fav)
        db.session.commit()
        fav = Favorite.query.filter_by(user_id=user_id).first()

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('main.users'))

@main.route('/')
def index():

    if current_user.is_authenticated:
        favourites = Favorite.query.filter_by(user_id=current_user.id).all()
    else:
        favourites = None    

    context = {
        'favourites' : favourites
    }

    return render_template('home.html', **context)

@main.route('/weather', methods=['GET'])
@login_required
def weather():

    #Get favourite places data
    favourites = Favorite.query.filter_by(user_id=current_user.id).all()

    #Initialize list
    weatherList = []

    #Get data from api
    for f in favourites:

        weather={
            "name": "No data",
            "description": "No data",
            "temperature": "No data",
            "humidity": "No data"
        }

        #weather.append(f)
        payload = {'lat': f.latitude, 'lon': f.longitude, 'appid': 'b7f46f673b72edc826d89c62775cb19b', 'units': 'metric'}
        dataJSON = requests.get('https://api.openweathermap.org/data/2.5/weather', params=payload).content
        data = json.loads(dataJSON)

        try:
            weather['description'] = data['weather'][0]['description']
            weather['temperature'] = data['main']['temp']
            weather['humidity'] = data['main']['humidity']
        except KeyError:
            weather['description'] = "No data"
            weather['temperature'] = "No data"
            weather['humidity'] = "No data"
        weather['name'] = f.name
        weatherList.append(weather)


    #Prepare data for HTML
    context = {
        'favourites' : favourites,
        'weather' : weatherList
    }

    #Render
    return render_template('currentWeather.html', **context)

@main.route('/deleteFavorite/<int:favorite_id>', methods=['GET', 'POST'])
@login_required
def delete_favorite(favorite_id):
    
    fav = Favorite.query.get_or_404(favorite_id)
    
    #Redirect users other than the owner of the favourite
    if current_user.id != fav.user_id:
        return redirect(url_for('main.index'))

    db.session.delete(fav)
    db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/forecast/<int:favorite_id>')
@login_required
def forecast(favorite_id):

    #Database
    favourites = Favorite.query.filter_by(user_id=current_user.id).all()
    favourite = Favorite.query.get_or_404(favorite_id)

    #Redirect users other than the owner of the favourite
    if favourite.user_id != current_user.id:
        return redirect(url_for('main.index'))

    #Initialize list
    weatherList = []

    payload = {'lat': favourite.latitude, 'lon': favourite.longitude, 'appid': 'b7f46f673b72edc826d89c62775cb19b', 'units': 'metric', 'exclude': 'current,minutely,hourly,alerts'}
    dataJSON = requests.get('https://api.openweathermap.org/data/2.5/onecall', params=payload).content
    data = json.loads(dataJSON)

    for i in range(7):
        weather={
            "day": "No data",
            "dayTemperature": "No data",
            "nightTemperature": "No data",
            "description": "No data",
            "windSpeed": "No data",
            "humidity": "No data"
        }
        
        try:
            dataD = data['daily'][i]

            weather['day'] = datetime.utcfromtimestamp(int(dataD['dt'])).strftime('%Y-%m-%d ')
            weather['description'] = dataD['weather'][0]['description']
            weather['dayTemperature'] = dataD['temp']['day']
            weather['nightTemperature'] = dataD['temp']['night']
            weather['humidity'] = dataD['humidity']
            weather['windSpeed'] = dataD['wind_speed']
        except KeyError:
            weather['day'] = "No data"
            weather['description'] = "No data"
            weather['dayTemperature'] = "No data"
            weather['nightTemperature'] = "No data"
            weather['humidity'] = "No data"
            weather['windSpeed'] = "No data"

        weatherList.append(weather)



    context = {
        'favourites':favourites,
        'name' : favourite.name,
        'weather' : weatherList
    }

    return render_template('forecast.html', **context)

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

@main.route('/add_favourite', methods=['GET', 'POST'])
@login_required
def add_favourite():
    if request.method == 'POST':
        #if variables.recaptcha.verify():
            name = request.form['name']
            lat = request.form['lat']
            lon = request.form['lon']

            #Create database entry
            favourite = Favorite(
                name=name, 
                latitude=lat,
                longitude=lon,
                user_id=current_user.id
            )

            #Add to database
            db.session.add(favourite)
            db.session.commit()


            return redirect(url_for('main.index'))
  
    return render_template('addFavourite.html')    


