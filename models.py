import flask_login
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class venues(db.Model):
    __tablename__ = 'venues'
    __table_args__ = {'extend_existing': True}
    v_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    v_name = db.Column(db.String, nullable=False)
    row = db.Column(db.Integer, nullable=False)
    column = db.Column(db.Integer, nullable=False)
    place = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)

class shows(db.Model):
    __tablename__ = 'shows'
    __table_args__ = {'extend_existing': True}
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String, nullable=False)
    s_venue = db.Column(db.Integer, db.ForeignKey('venues.v_id'), nullable=False)
    seating = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer)
    available = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String, nullable=False)

class users(flask_login.UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, nullable=False, primary_key=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    mode = db.Column(db.String, nullable=False)

class bookings(db.Model):
    __tablename__ = 'bookings'
    b_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey('shows.s_id'), nullable=False)
    seats = db.Column(db.String, nullable=False)
