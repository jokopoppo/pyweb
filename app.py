from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
# from tabledef import *
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
# from register import *
engine = create_engine('sqlite:///tutorial.db', echo=True)

app = Flask(__name__)

@app.route('/')
def home(name=""):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return hello(name=name)

@app.route('/test')
def test():
    return "Deploy Success"


@app.route('/login', methods=['POST'])
def do_admin_login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home(POST_USERNAME)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/hello/<string:name>/")
def hello(name):
    #    return name
    quotes = [ "'If people do not believe that mathematics is simple, it is only because they do not realize how complicated life is.' -- John Louis von Neumann ",
               "'Computer science is no more about computers than astronomy is about telescopes' --  Edsger Dijkstra ",
               "'To understand recursion you must first understand recursion..' -- Unknown",
               "'You look at things that are and ask, why? I dream of things that never were and ask, why not?' -- Unknown",
               "'Mathematics is the key and door to the sciences.' -- Galileo Galilei",
               "'Not everyone will understand your journey. Thats fine. Its not their journey to make sense of. Its yours.' -- Unknown"  ]
    randomNumber = randint(0,len(quotes)-1)
    quote = quotes[randomNumber]

    return render_template('test.html',**locals())


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])

    def reset(self):
        blankData = MultiDict([ ('csrf', self.reset_csrf() ) ])
        self.process(blankData)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = ReusableForm(request.form)

    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
        email=request.form['email']
        print (name, " ", email, " ", password)

        if form.validate():
            # Save the comment here.
            Session = sessionmaker(bind=engine)
            s = Session()
            query = s.query(User).filter(User.username.in_([name]), User.password.in_([password]) )
            result = query.first()
            if not result:
                regismember(name,password)
                session['logged_in'] = True
                return home(name=name)
            else:
                flash('Error: Duplicate username. ')
        else:
            flash('Error: All the form fields are required. ')

    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)