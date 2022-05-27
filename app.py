from flask import Flask, request, flash, url_for, redirect, render_template, abort
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'cockroachdb://maxroach@localhost:26257/students' #'postgresql://postgres:10153@localhost/students'
app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)

class Students(db.Model):
    __tablename__ = 'students'
    sid = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(200))
    course = db.Column(db.String(200))
    skill = db.Column(db.String(200))
    size = db.Column(db.Integer)
    notes = db.Column(db.Text())
    group_name = db.Column(db.Integer)


    def __init__(self, sid, name, course, skill, size, notes):
        self.sid = sid
        self.name = name
        self.course = course
        self.skill = skill
        self.size = size
        self.notes = notes
        self.group_name = None

@app.route('/')
def index():
    def callback(session):
        return render_template('index.html')
    return run_transaction(sessionmaker, callback)
    #return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        sid = request.form['sid']
        name = request.form['name']
        course = request.form['course']
        skill = request.form['skill']
        size = request.form['size']
        notes = request.form['notes']
        print(sid, name, course, skill, size, notes)
        
        if sid == '' or name == '':
            def callback(session):
                return render_template('index.html', message='Please enter required fields')
            return run_transaction(sessionmaker, callback)
            
        if db.session.query(Students).filter(Students.sid == sid).count() != 0:
            return render_template('index.html', message='You have already submitted this form.')
        else:
            def callback(session):
                data = Students(sid, name, course, skill, size, notes)
                db.session.add(data)
                db.session.commit()
            run_transaction(sessionmaker, callback)

            if db.session.query(Students).filter(Students.course == course, Students.skill == skill, Students.size == size, Students.group_name == None).count() < int(size):
                def callback(session):
                    return render_template('searching.html')
                return run_transaction(sessionmaker, callback)
            else:
                potential = db.session.query(Students).filter(Students.course == course, Students.skill == skill, Students.size == size, Students.group_name == None)
                potential = potential.limit(int(size))
                group_ids = []
                m = ''
                for i in potential:
                    group_ids.append(i.sid)
                    m += i.name + ' '
                m = 'Your team members are: ' + m
                group_name = group_ids[0]

                def callback(session):
                    for i in group_ids:
                        db.session.query(Students).filter(Students.sid == i).update({Students.group_name : group_name})
                    db.session.commit()
                    return render_template('success.html', message=m)
                #send_mail(customer, dealer, rating, comments)
                return run_transaction(sessionmaker, callback)



if __name__ == '__main__':
    app.run()
