from flask import Flask, request, jsonify, make_response
app = Flask(__name__, static_url_path="/static", static_folder="static")
import sqlite3
import secrets
from passlib.hash import sha256_crypt
from calculate_measures import get_measures
from smtplib import SMTP_SSL, SMTPException
import datetime
import env

user_db = '/home/ubuntu/capstone/users.db'
data_db = '/home/ubuntu/capstone/records.db'

user_tokens = []
admin_tokens = []

@app.route('/login', methods=['POST'])
def generateToken():
	username = request.form.get("username")
	password = request.form.get("password")
	users_conn = sqlite3.connect(user_db)
	users_conn.row_factory = sqlite3.Row
	cur = users_conn.cursor()
	cur.execute("SELECT * FROM admins WHERE username = ?", (username,))
	results = cur.fetchall()
	if (len(results) == 1):
		if (sha256_crypt.verify(password, results[0]["password"])):
			token = secrets.token_urlsafe(32)
			toAdd = {}
			toAdd["user"] = results[0]["username"]
			toAdd["token"] = token
			admin_tokens.append(toAdd)
			res = make_response("Logged in as admin", 200)
			res.set_cookie("token", token)
			res.set_cookie("admin", "True")
			return res

	cur.execute("SELECT * FROM users WHERE username = ?", (username,))
	results = cur.fetchall()
	if (len(results) == 1):
		if (sha256_crypt.verify(password, results[0]["password"])):
			token = secrets.token_urlsafe(32)
			toAdd = {}
			toAdd["user"] = results[0]["username"]
			toAdd["token"] = token
			toAdd["hospital"] = results[0]["hospital"]
			user_tokens.append(toAdd)
			res = make_response("Logged in as user", 200)
			res.set_cookie("token", token)
			res.set_cookie("admin", "False")
			return res

	return jsonify(request.form), 400

def userCheck(token):
	for x in user_tokens:
		if x["token"] == token:
			return True
	for x in admin_tokens:
		if x["token"] == token:
			return True
	return False

def adminCheck(token):
	for x in admin_tokens:
		if x["token"] == token:
			return True
	return False

@app.route('/createUser', methods=['POST'])
def createUser():
	if (adminCheck(request.cookies.get("token"))):
		users_conn = sqlite3.connect(user_db)
		users_conn.row_factory = sqlite3.Row
		cur = users_conn.cursor()
		username = request.form.get("username")
		password = request.form.get("password")
		hospital = request.form.get("hospital")
		try:
			hospital = int(hospital)
		except ValueError as e:
			return "Invalid hospital ID", 400
		if not (username and password and hospital):
			return "400 bad request", 400
		cur.execute("INSERT INTO users VALUES (?, ?, ?)", (username, sha256_crypt.hash(password), hospital))
		users_conn.commit()
	else:
		return "403 Unauthorized", 403

@app.route('/createAdmin', methods=['POST'])
def createAdmin():
	if (adminCheck(request.cookies.get("token"))):
		users_conn = sqlite3.connect(user_db)
		users_conn.row_factory = sqlite3.Row
		cur = users_conn.cursor()
		username = request.form.get("username")
		email = request.form.get("email")
		token = secrets.token_urlsafe(32)
		if not (username and email):
			return "400 bad request", 400
		cur.execute("INSERT INTO pending_admins VALUES (?, ?, ?)", (username, email, token))
		sendEmail(email, "OPQIC Data Portal Invitation", f"You have been added as an admin to the OPQIC data portal with the username {username}. Click the link below to create your account:\n\nhttp://ec2-3-21-217-21.us-east-2.compute.amazonaws.com/admin?token={token}")
		users_conn.commit()
	else:
		return "403 Unauthorized", 403

@app.route('/', methods=['GET'])
def mainPage():
	if request.cookies.get("token"):
		if userCheck(request.cookies.get("token")):
			return app.send_static_file("OmnoDashboard.html")
	return app.send_static_file("LoginView.html")

@app.route('/data', methods=['GET'])
def data():
	if not (userCheck(request.cookies.get("token"))):
		return "403 Unauthorized", 403
	return get_measures()

def sendEmail(email, subject, message):
	try:
		smtpObj = SMTP_SSL("mail.opqic.org", port=465)
		smtpObj.login(env.email, env.email_pass)
		smtpObj.sendmail("dataportal@opqic.org", email, f"From: {fromAddr}\r\nTo: {toAddr}\r\nSubject: {subject}\r\n\r\n{message}")
		print("No errors!")
		smtpObj.quit()
	except SMTPException as e:
		print("Error")
		print(e)

@app.route('/accountCreate', methods=['GET'])
def adminPropose():
	return app.send_static_file("accountCreation.html")

@app.route('/accountAccept', methods=['POST'])
def adminAccept():
	token = request.form.get("token")
	username = request.form.get("username")
	password = request.form.get("password")
	users_conn = sqlite3.connect(user_db)
	users_conn.row_factory = sqlite3.Row
	cur = users_conn.cursor()
	cur.execute("SELECT * FROM pending_admins WHERE token = ? AND username = ?", (token, username))
	results = cur.fetchall()
	if (len(results) == 1):
		cur.execute("INSERT INTO admins VALUES (?, ?, ?)", (username, results[0]["email"], sha256_crypt.hash(password)))
		cur.execute("DELETE FROM pending_admins WHERE token = ? AND username = ?", (token, username))
		token = secrets.token_urlsafe(32)
		toAdd = {}
		toAdd["user"] = results[0]["username"]
		toAdd["token"] = token
		admin_tokens.append(toAdd)
		res = make_response("admin", 200)
		res.set_cookie("token", token)
		res.set_cookie("admin", "True")
		return res
	cur.execute("SELECT * FROM pending_users WHERE token = ? AND username = ?", (token, username))
	results = cur.fetchall()
	if (len(results) == 1):
		cur.execute("INSERT INTO users VALUES (?, ?, ?)", (username, results[0]["email"], results[0]["hospital_id"], sha256_crypt.hash(password)))
		cur.execute("DELETE FROM pending_users WHERE token = ? AND username = ?", (token, username))
		token = secrets.token_urlsafe(32)
		toAdd = {}
		toAdd["user"] = results[0]["username"]
		toAdd["token"] = token
		admin_tokens.append(toAdd)
		res = make_response("admin", 200)
		res.set_cookie("token", token)
		res.set_cookie("admin", "False")
		return res


if (__name__ == "__main__"):
	app.run()

print('Running website')
