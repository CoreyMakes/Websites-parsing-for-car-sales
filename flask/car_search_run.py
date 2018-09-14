from flask import Flask, render_template, request, redirect, url_for
from flask_material import Material 
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
from flask_pymongo import PyMongo

app = Flask(__name__)  
Material(app)  
app.config['SECRET_KEY'] = 'USE-YOUR-OWN-SECRET-KEY-DAMNIT'
app.config['RECAPTCHA_PUBLIC_KEY'] = 'TEST'
app.config["MONGO_URI"] = "mongodb://localhost:27017/autoria"
mongo = PyMongo(app)

class ExampleForm(Form):
	mark_name = TextField('Mark', validators = [validators.required()])
	model_name = TextField('Model')	  
			
	submit_button = SubmitField('Find me a car!')	

class LoginForm(Form):
	login = TextField('Enter your login', [validators.required()])
	password = TextField('Enter your password', [validators.required()])
	
	#remember_me = BooleanField('remember_me')
	

@app.route('/')  
def welcome():
	form = LoginForm()
	return render_template('index.html', form = form)  
	
	if __name__ == '__main__':  
		app.run(debug = True)  
	
	
	
@app.route('/start', methods=['GET', 'POST'])
def start():
	form = ExampleForm(request.form)
	
	if form.validate_on_submit():
		cars = list(mongo.db.new_cars.find( {"mark_name" : form.mark_name.data }))
		return render_template('check.html', data = cars)
	
	return render_template('start.html', form = form)
	
@app.route('/checkDB')
def checkDB():
	cars = list(mongo.db.new_cars.find())
		
	return render_template('check.html', data = cars)

@app.route('/register', methods = ['GET', 'POST'])
def register():
	
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for ' + form.login.data + '", remember_me=' + str(form.remember_me.data))
		return redirect('/index')
	return render_template('register.html', 
		title = 'Sign In',
		form = form)
