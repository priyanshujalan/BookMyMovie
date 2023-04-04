from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import send_file
from flask import request

import os

import flask_login

from datetime import datetime

from models import db
from models import shows
from models import venues
from models import users
from models import bookings

from pdf import PDF

from utils import convertToTitle

appRoutes = Blueprint('appRoutes', __name__, template_folder='templates')

@appRoutes.route('/')
@flask_login.login_required
def homepage():
    # Main Homepage
    getShows = shows.query.all()
    currentShows = []
    for s in getShows:
        v = venues.query.filter_by(v_id=s.s_venue).first()
        s.venue = v.v_name
        s.place = v.place
        if datetime.strptime(s.date, '%Y-%m-%d')>= datetime.now():
            currentShows.append(s)

    user = users.query.filter_by(id=flask_login.current_user.id).first()
    
    return render_template('homepage.html', shows=currentShows, user=user)

@appRoutes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', error='none')

    my_user = users.query.filter_by(id=request.form['username']).first()
    if my_user == None:
        return render_template('login.html', error='No User Found')

    if my_user.password == request.form['password']:
        flask_login.login_user(my_user)
        return redirect(url_for('appRoutes.homepage'))

    elif my_user.password != request.form['password']:
        return render_template('login.html', error='Password Incorrect')

    return render_template('login.html', error='An Error Occured')

@appRoutes.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', error = 'none')

    my_user = users.query.filter_by(id=request.form['username']).first()
    if my_user != None:
        return render_template('signup.html', error = 'User Already Exists!')

    if request.form['pass'] != request.form['pass2']:
        return render_template('signup.html', error = 'Both Passwords dont Match!')
    
    if len(request.form['pass'])<8 or len(request.form['pass'])>16:
        return render_template('signup.html', error = 'Password must be of 8 to 16 chars!')
    
    
    add_user = users(id=request.form['username'], password=request.form['pass'], name=request.form['name'], mode='consumer')
    db.session.add(add_user)
    db.session.commit()
    return redirect(url_for('appRoutes.login'))

@appRoutes.route('/user/<userID>', methods=['GET', 'POST'])
@flask_login.login_required
def user_booking(userID):
    if flask_login.current_user.id == userID:
        booked = bookings.query.filter_by(username=flask_login.current_user.id).all()
        user = users.query.filter_by(id=flask_login.current_user.id).first()

        for b in booked:
            s = shows.query.filter_by(s_id=b.s_id).first()
            v = venues.query.filter_by(v_id=s.s_venue).first()
            b.s_name = s.s_name
            b.d_t = s.date + " & " + s.time
            b.place = v.place

        return render_template('userBookings.html', booked=list(reversed(booked)), user=user)

    return redirect(url_for('appRoutes.homepage'))

@appRoutes.route('/book/<s_id>', methods=['GET', 'POST'])
@flask_login.login_required
def book(s_id):
    error = None
    if request.method == 'POST':
        show = shows.query.filter_by(s_id=s_id).first()
        venue = venues.query.filter_by(v_id=show.s_venue).first()
        return render_template('venueView.html', row=venue.row, column=venue.column, show=show)
    
@appRoutes.route('/bill/<s_id>', methods=['GET', 'POST'])
@flask_login.login_required
def bill(s_id):
    if request.method == 'POST':
        
        show = shows.query.filter_by(s_id=s_id).first()
        venue = venues.query.filter_by(v_id=show.s_venue).first()
        checks = request.form.getlist('seats')
        n = len(checks)
        to_be_booked = []
        for check in checks:
            [i,j] = check.split(':')
            to_be_booked.append((int(i)*venue.column + int(j)))

        seats = show.seating
        l = list(seats)
        for i in to_be_booked:
            l[i] = '0'
        show.seating = "".join(l)
        show.available = show.available - n

        tickets = ''
        for t in checks:
            [i,j] = t.split(":")
            tickets = tickets + convertToTitle(int(i)+1)+str(int(j)+1)+" "

        add_booking = bookings(username=flask_login.current_user.id, s_id = s_id, seats=tickets)
        db.session.add(add_booking)
        getBooking = bookings.query.filter_by(username=add_booking.username, s_id=add_booking.s_id).first()
        db.session.commit()

        print(getBooking.b_id)
        return render_template('booked.html', getBooking=getBooking)

    return redirect(url_for('appRoutes.logout'))

@appRoutes.route('/download/<booking_id>', methods=['GET'])
@flask_login.login_required
def downloadBill(booking_id):
    pdf = PDF(orientation='P', unit ='mm', format='A4')
    getBooking = bookings.query.filter_by(b_id=booking_id).first()
    getShow = shows.query.filter_by(s_id=getBooking.s_id).first()
    getVenue = venues.query.filter_by(v_id=getShow.s_venue).first()
    pdf.add_page()
    pdf.print_bill(getShow.s_name, getVenue.v_name+", "+getVenue.place, getBooking.seats, getShow.date+" "+getShow.time, flask_login.current_user.id)
    file_name = flask_login.current_user.id+booking_id+".pdf" 
    pdf.output('bills\\'+file_name,'F')
    path = appRoutes.root_path+'\\bills\\'+file_name
    return send_file(path, as_attachment=True)
    

@appRoutes.route('/admin', methods=['GET', 'POST'])
@flask_login.login_required
def admin():
    msg = None
    if flask_login.current_user.id == 'admin':
        getVenues = venues.query.all()
        getShows = shows.query.all()
        if request.method == 'GET':
            msg = None
    
        return render_template('admin.html', shows=getShows, venues=getVenues)
    
@appRoutes.route('/addShow', methods=['GET', 'POST'])
@flask_login.login_required
def addShow():
    error = None
    if request.method == "POST":
        getVenue = venues.query.filter_by(v_id=request.form['venue']).first()
        getCap = getVenue.row * getVenue.column
        seating = "1" * getCap
        add_show = shows(s_venue=request.form['venue'], s_name=request.form['name'], available=getCap, date=request.form['date'],
                            time=request.form['time'], rating=request.form['rating'], seating=seating, genre=request.form['genre'])
        db.session.add(add_show)
        db.session.commit()
    
    return redirect(url_for('appRoutes.admin'))

@appRoutes.route('/editShow', methods=['GET', 'POST'])
@flask_login.login_required
def editShow():
    error = None
    if request.method == "POST":
        getVenue = venues.query.filter_by(v_id=request.form['venue']).first()
        getShow = shows.query.filter_by(s_id=request.form['show']).first()

        if int(request.form['venue']) != getShow.s_venue:
            getCap = getVenue.row * getVenue.column
            getShow.available = getCap
            getShow.seating = "1" * getCap
            getShow.s_venue=request.form['venue']

        getShow.s_name=request.form['name']
        getShow.date=request.form['date']
        getShow.time=request.form['time']
        getShow.rating=request.form['rating']
        getShow.genre=request.form['genre']
        db.session.commit()
    
    return redirect(url_for('appRoutes.admin'))

@appRoutes.route('/deleteShow', methods=['GET', 'POST'])
@flask_login.login_required
def deleteShow():
    error = None
    if request.method == "POST":
        shows.query.filter_by(s_id=request.form['show']).delete()
        db.session.commit()
    
    return redirect(url_for('appRoutes.admin'))

@appRoutes.route('/addVenue', methods=['GET','POST'])
@flask_login.login_required
def addVenue():
    error = None
    if request.method == "POST":
        add_venue = venues(v_name=request.form['v_name'], place=request.form['place'], row=request.form['row'], column=request.form['column'])
        db.session.add(add_venue)
        db.session.commit()
    return redirect(url_for('appRoutes.admin'))

@appRoutes.route('/editVenue', methods=['GET','POST'])
@flask_login.login_required
def editVenue():
    error = None
    if request.method == "POST":
        venue = venues.query.filter_by(v_id=request.form['venue']).first()
        venue.v_name = request.form['v_name']
        venue.place = request.form['place']
        venue.row = request.form['row']
        venue.column = request.form['column']
        db.session.commit()
    return redirect(url_for('appRoutes.admin'))

@appRoutes.route('/deleteVenue', methods=['GET','POST'])
@flask_login.login_required
def deleteVenue():
    error = None
    if request.method == "POST":
        shows.query.filter_by(s_venue=request.form['venue']).delete()
        venues.query.filter_by(v_id=request.form['venue']).delete()
        db.session.commit()
    return redirect(url_for('appRoutes.admin'))


@appRoutes.route('/logout')
@flask_login.login_required
def logout():
    name = flask_login.current_user.id
    flask_login.logout_user()
    return render_template('logout.html', user=name)


