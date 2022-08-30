import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.ini')
# from sqlalchemy import create_engine
# engine = create_engine('mysql://root:ala123@localhost/mydb')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ala123@localhost/mydb'

db = SQLAlchemy(app)

# client_meeting_schedule = db.Table('client_meeting_schedule',
#     db.Column('client_id', db.Integer, db.ForeignKey('client.id')),
#     db.Column('meeting_schedule_id', db.Integer, db.ForeignKey('meeting_schedule.id')))
#
#
# class Client(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(45))
#     last_name = db.Column(db.String(45))
#     phone_number = db.Column(db.Integer)
#     date_of_birth = db.Column(db.Date)
#     email = db.Column(db.String(45))
#     is_active = db.Column(db.Boolean)
#     address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
#     participation = db.relationship('MeetingSchedule', secondary = client_meeting_schedule, backref = 'participants' )
#
#     def __repr__(self):
#         return f"{Client.id}, {Client.name}, {Client.last_name}, {Client.phone_number}, {Client.email}"
#
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(45))
    postal_code = db.Column(db.String(10))
    street = db.Column(db.String(45))
    building_number = db.Column(db.Integer)
    apartment_number= db.Column(db.Integer)
#
#     client = db.relationship('Client', backref='address', uselist=False)
#
# class MeetingSchedule(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     subject = db.Column(db.String(45))
#     rate = db.Column(db.Integer)
#     duration = db.Column(db.Integer)
#     time = db.Column(db.Time)
#     week_day = db.Column(db.String(15))
#     is_online = db.Column(db.Boolean)
#     is_active = db.Column(db.Boolean)
#     start_date = db.Column(db.Date)
#     end_date = db.Column(db.Date)
#
#     meetings = db.relationship('Meeting', backref='meetingSchedule', lazy='dynamic')
#
# class Meeting(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     rate = db.Column(db.Integer)
#     duration = db.Column(db.Integer)
#     time = db.Column(db.Time)
#     is_online = db.Column(db.Boolean)
#     date = db.Column(db.Date)
#     week_number = db.Column(db.Integer)
#     notes = db.Column(db.String(200))
#     meetingSchedule_id = db.Column(db.Integer, db.ForeignKey('meetingSchedule.id'))
#     cancellation_id = db.Column(db.Integer, db.ForeignKey('cancellation.id'))

class Cancellation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cancellation_time_before_class = db.Column(db.Integer)
    reason = db.Column(db.String(45))
    is_cancelled_by_student = db.Column(db.Boolean)
    holiday_id = db.Column(db.Integer, db.ForeignKey('holiday.id'))

    # meeting = db.relationship('Meeting', backref='cancellation')

#uselist - uzywane w one to one relation, by default = True
    def __repr__(self):
        return f"{self.id}, {self.reason}"

class Holiday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    holiday_type = db.Column(db.String(45))
    start_date_time = db.Column(db.DateTime)
    end_date_time = db.Column(db.DateTime)

    cancellations = db.relationship('Cancellation', backref='holiday', lazy='dynamic')

    def __repr__(self):
        return f"{self.id}, {self.holiday_type}"

# @app.route("/")
# def hello_world():
#     L = Client.query.all()  # client.query- BaseQuery           # select * from client
#     # L = client.query.first()        # client.query- BaseQuery           # select * from client
#     c = L[0]
#     print(c)
#     db.session.commit()
#     return str(f"{c.name}, {c.last_name}, {c.id}")

@app.route("/")
def index():
    return "index ok"

@app.route("/add_holiday")
def add_holiday():
    h=Holiday(holiday_type ='Urlop', start_date_time= datetime.datetime(year=2022, month = 8, day = 1) , end_date_time = datetime.datetime(year=2022, month = 8, day = 31) )
    db.session.add(h)
    db.session.commit()
    return 'holiday added'

@app.route("/get_holiday")
def get_holiday():
    h=Holiday.query.filter(Holiday.holiday_type =='Gwiazdka').first()
    print(type(h))
    print(h)
    return str(h)

@app.route("/modify_holiday")
def modify_holiday():
    h=Holiday.query.filter(Holiday.id == 2).first()
    h.holiday_type = "Przerwa swiateczna"
    db.session.commit()
    # print(type(h))
    # print(h)
    return str(h)
#
@app.route("/delete_holiday")
def delete_holiday():
    h=Holiday.query.filter(Holiday.holiday_type =='Gwiazdka').first()
    db.session.delete(h)
    db.session.commit()
    return 'holiday deleted'
# #modyfikacja
# #pozostale klasy po jednej
# #usuwanie

@app.route("/add_cancellation")
def add_cancellation():
    c=Cancellation(cancellation_time_before_class ='24', reason= 'Bo tak' , is_cancelled_by_student = True)
    db.session.add(c)
    db.session.commit()
    return 'cancellation added'

@app.route('/add_client')
def add_client():

    pass

@app.route('/add_address/<string:city>/<string:postal_code>/<string:street>/<int:building_number>/<int:apartment_number>')
def add_address(city, postal_code, street, building_number, apartment_number):

    a = Address(city=city, postal_code=postal_code, street=street, building_number=building_number, apartment_number=apartment_number)
    # a=Address()
    db.session.add(a)
    db.session.commit()
    return 'address added'

# @app.route('/add_address')
# def add_address():
#     request.query_string
#     request.args['city', 'postal_code', 'street', 'building_number', 'apartment_number']
#     for p in request.args:
#         print(p, request.args[p])
#     city = ''
#     postal_code = ''
#     street = ''
#     building_number = 1
#     apartment_number = 1
#     if 'city' in request.args:
#         city = request.arg['city']
#     if 'postal_code' in request.args:
#         postal_code = request.args['postal_code']
#     a = Address(city=city, postal_code=postal_code, street=street, building_number=building_number, apartment_number=apartment_number)
#     # a=Address()
#     db.session.add(a)
#     db.session.commit()
#     return 'address added'


@app.route('/add_meeting')
def add_meeting():
    pass



@app.route("/create_all")
def create_all():
    db.create_all()
    return 'create_all_OK'



app.run(port='5001')


# INSERT INTO `mynewdb`.`holiday` (`id`, `holiday_type`, `start_date_time`, `end_date_time`) VALUES ('1', 'Wielkanoc', '01.04.2022', '02.04.2022')
