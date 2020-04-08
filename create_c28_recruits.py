import psycopg2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

connection = psycopg2.connect(database='prod', user='postgres', password='pass', host='localhost')
cursor = connection.cursor()

query = """INSERT INTO recruits(first_name, surname, rocketchat_user, github_name, personal_email, cohort) 
VALUES 
('Tapz','Thomas','Tapz28','TapzGHub','Tapz@example.com','C28 Data Eng'),
('Peter','Parker','PeteP28','PeterPGHub','PP@example.com','C28 Data Eng'),
('Bruce','Wayne','BruceW28','BruceGHub','BW@example.com','C28 Data Eng'),
('Dave','East','Dave28','DaveEGHub','DEast@example.com','C28 Data Eng'),
('Lass','Man','Lass28','LassGHub','Lass@example.com','C28 Data Eng');"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass@127.0.0.1/prod'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    recruit = db.relationship('Recruit', backref='owner', lazy='dynamic')

class Recruits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    first_name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    rocketchat_user = db.Column(db.VARCHAR(15))
    github_name = db.Column(db.VARCHAR(20))
    personal_email = db.Column(db.VARCHAR(20), unique=True)
    cohort = db.Column(db.VARCHAR(20))

cursor.execute(query)
connection.commit()
if __name__=='__main__':
    manager.run()