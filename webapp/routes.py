from flask import Flask, redirect, render_template, flash, request, Response
from twilio.rest import Client
from flask_mail import Mail, Message
from flask_sslify import SSLify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from multiprocessing import Process
import time
import sys
import os


class ContactForm(FlaskForm):
    name = StringField(label='Your Name', validators=[DataRequired()])
    address = StringField(label='Your Home Address', validators=[DataRequired()])
    email = StringField(label='Your Email', validators=[DataRequired()])
    problem = TextAreaField(label='What Do You Need Help With?', validators=[DataRequired()])
    date = StringField(label='What Date/Time Works Best?', validators=[DataRequired()])
    submit = SubmitField(label='Submit A Request!', validators=[DataRequired()])


class ReviewForm(FlaskForm):
    info = TextAreaField(label='', validators=[DataRequired()])

class UnsuscribeForm(FlaskForm):
    email = StringField(label='Please enter your email to be removed from the mailing list:', validators=[DataRequired()])


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
# flask forms
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# flask mail
app.config['MAIL_SERVER'] = "mail.privateemail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = "reed@reedtechsupport.info"
app.config['MAIL_PASSWORD'] = os.environ.get('PRIVATEEMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ("The Website", "reed@reedtechsupport.info")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['TESTING'] = False
mail = Mail(app)
# flask sslify
# if os.environ.get('ENVIRONMENT') != 'DEV':
#     sslify = SSLify(app)
# sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('AWS_DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


def send_text(msg):
    client.messages.create(
                body=msg, 
                from_='+14152377516', 
                to='+14159145311')
    print('text sent')


def send_email(subject, body):
    msg = Message(subject,
                  recipients=["reed@reedtechsupport.info"])
    msg.body = body
    mail.send(msg)
    print('email sent')


class SupportRequests(db.Model):
    __tablename__ = 'support_requests'
    __table_args__ = {'extend_existing': True}
    id = db.Column('id', db.Integer, primary_key=True)
    client_name = db.Column('client_name', db.String(255))
    visit_time = db.Column('visit_time', db.Text)
    problem = db.Column('problem', db.Text)
    email = db.Column('email', db.Text)
    address = db.Column('address', db.Text)
    request_time = db.Column('request_time', db.Integer)
    notes = db.Column('notes', db.Text)
    completed = db.Column('completed', db.Boolean)

    def __init__(self, client_name, visit_time, problem, email, address, request_time):
        self.client_name = client_name
        self.visit_time = visit_time
        self.problem = problem
        self.email = email
        self.address = address
        self.request_time = request_time

def add_support_request(form):
        new_request = SupportRequests(client_name=form.name.data, visit_time=form.date.data, problem=form.problem.data,
                        email=form.email.data, address=form.address.data, request_time=str(time.strftime('%l:%M %p (%Z)')))
        db.session.add(new_request)
        db.session.commit()
        print('added to database')

@app.route('/')
def redirect_home():
    return redirect('001011010')


@app.route('/admin/')
def admin():
    return render_template('home.html')



@app.route('/home/')
def home():
#    return render_template('home.html')


@app.route('/static/me.png')
def nice_try():
    return render_template('404.html')


@app.route('/static/me.png/')
def nice_try_1():
    return render_template('404.html')


@app.route('/test_support_request/')
def test():
    try:
        # email
        p = Process(target=send_email, args=('Testing Support Request', 'Testing 1 2 3',))
        p.start()
        # text
        p2 = Process(target=send_text, args=('Testing 1 2 3',))
        p2.start()
    except:
        return Response(f'<body style="background-color: red;"><div style="top: 100vh;">\
                <h2 style="color: white; text-align: center;">Not Sent</h2></div></body>')
    return Response('<body style="background-color: green;">\
            <div style="top: 100vh;"><h2 style="color: white; text-align: center;">\
            Sent</h2></div>\</body>')


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # message
        support_request_message = f"-\nName:\n{form.name.data}\
                    \n\nDate:\n{form.date.data}\n\nProblem:\n{form.problem.data}\
                    \n\nAddress:\n{form.address.data}\n\nEmail:\n{form.email.data}\
                    \n\nRequest:\n{time.strftime('%l:%M %p (%Z)')}"
        print(str(support_request_message))
        # text
        text = Process(target=send_text, args=(support_request_message,))
        text.start()
        # email
        email = Process(target=send_email, args=('Support Request!', support_request_message,))
        email.start()
        # database
        database = Process(target=add_support_request, args=(form,))
        database.start()
        return render_template('request_received.html')
    return render_template('contact.html', form=form)


@app.route('/success/')
def success():
    return render_template('success.html')


@app.route('/qr-code/')
def qr_code():
    try:
        p = Process(target=send_text, args=('Someone used a qr-code!',))
        p.start()
    except:
        pass
    return redirect('/home/')


@app.route('/google_maps/')
def g_maps():
    try:
        p = Process(target=send_text, args=('Someone clicked on the google maps link!',))
        p.start()
    except:
        pass
    return redirect('/home/')

@app.route('/testimony/')
def testimony():
    return redirect('/review/')

@app.route('/review/', methods=['GET', 'POST'])
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        print(str(form.info.data))
        p = Process(target=send_text, args=("Testimony: " + str(form.info.data),))
        p.start()
        p2 = Process(target=send_email, args=("Testimony", "Testimony: " + str(form.info.data)))
        p2.start()
        return render_template('thank_you.html')
    return render_template('review.html', form=form)


@app.route('/unsubscribe/', methods=['GET', 'POST'])
def unsuscribe():
    form = UnsuscribeForm()
    if form.validate_on_submit():
        print("Unsubscription-" + str(form.email.data))
        p = Process(target=send_text, args=("Unsubscription: " + str(form.email.data),))
        p.start()
        p2 = Process(target=send_email, args=("Unsubscription", "Unsubscription: " + str(form.email.data)))
        p2.start()
        flash('You have been unsubscribed!')
        return render_template('success.html')
    return render_template('unsubscribe.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
