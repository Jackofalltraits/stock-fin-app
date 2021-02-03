from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_required, current_user
from . import db
import sqlite3
import yfinance as yf

main = Blueprint('main', __name__)

conn = sqlite3.connect("users.db",check_same_thread=False)
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, password TEXT)')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)

#################################################
##################################################

@main.route("/signup",methods=['POST','GET'])
def signup():
	if request.method=='POST':
		name=request.form["name"]
		email=request.form["email"]
		password=request.form["password"]
		
        
		c.execute("INSERT INTO users (name, email, password) values (?,?,?)",(name, email, password))
		conn.commit()

		return render_template('profile.html')
	else:
		return render_template('signup.html')

@main.route("/table")
def table():
		result = c.execute("Select * from users")
		result = result.fetchall()
		return render_template('Table.html',result=result)

@main.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')
    #if request.method=='GET':
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if (not user or not check_password_hash(user.password, password)):
        flash('Please check your login details and try again.')
        #return redirect(url_for('main.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    if(user and check_password_hash(users.password, password)):

        return redirect(url_for('main.profile'))

@main.route('/logout')
def logout():
    return redirect(url_for('main.index'))

# API Route for pulling the stock quote
@main.route("/quote")
def display_quote():
	# get a stock ticker symbol from the query string
	# default to AAPL
	symbol = request.args.get('symbol', default="AAPL")
	# pull the stock quote
	quote = yf.Ticker(symbol)
	#return the object via the HTTP Response
	return quote.info

# API route for pulling the stock history
@main.route("/history")
def display_history():
	#get the query string parameters
	symbol = request.args.get('symbol', default="AAPL")
	period = request.args.get('period', default="1y")
	interval = request.args.get('interval', default="1mo")
	#pull the quote
	quote = yf.Ticker(symbol)	
	#use the quote to pull the historical data from Yahoo finance
	hist = quote.history(period=period, interval=interval)
	#convert the historical data to JSON
	data = hist.to_json()
	#return the JSON in the HTTP response
	return data

if __name__ == "__main__":
	main.run()