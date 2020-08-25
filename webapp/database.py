from flask_sqlalchemy import SQLAlchemy


from routes import db

class SupportRequests(db.Model):
    __tablename__ = 'reedtechsupport'
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
        # new_request = SupportRequests(client_name=form.name.data, visit_time=form.date.data, problem=form.problem.data,
                        # email=form.email.data, address=form.address.data, request_time=str(time.strftime('%l:%M %p (%Z)')))
        new_request = SupportRequests(client_name=form.name, visit_time=form.date, problem=form.problem,
                        email=form.email, address=form.address, request_time=str(time.strftime('%l:%M %p (%Z)')))
        db.session.add(new_request)
        db.session.commit()