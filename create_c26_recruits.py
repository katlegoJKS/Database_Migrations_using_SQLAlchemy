import psycopg2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

connection = psycopg2.connect(database='prod', user='postgres', password='pass', host='localhost', port=5430)
cursor = connection.cursor()

query = """INSERT INTO recruits(first_name, surname, rocketchat_user, github_name, personal_email, cohort) 
VALUES 
('Shaun','Thomas','ShaunT26','ShaunGHub','Shau@example.com','C26 Data Eng'),
('Nthabi','Moleko','NthabiM26','NthabiGHub','Ntha@example.com','C26 Data Eng'),
('Kabi','Jones','KabiJ26','KabiJGHub','kabi@example.com','C26 Data Eng'),
('Matt','Hew','MattHew26','MattHewGHub','Matt@example.com','C26 Data Eng'),
('Zack','Oteng','ZackO26','ZackGHub','ZackO@example.com','C26 Data Eng');"""

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