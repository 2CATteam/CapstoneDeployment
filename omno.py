from flask import Flask, request, jsonify, make_response
app = Flask(__name__, static_url_path="/static", static_folder="static")
import sqlite3
import secrets
from passlib.hash import sha256_crypt
from calculate_measures import get_measures
from smtplib import SMTP_SSL, SMTPException
import _thread as thread
import datetime
import env

user_db = '/home/ubuntu/capstone/users.db'
data_db = '/home/ubuntu/capstone/records.db'

this_domain = 'http://ec2-3-21-217-21.us-east-2.compute.amazonaws.com'

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
			cur.execute("INSERT INTO tokens VALUES (?, ?, ?)", (username, token, 1))
			users_conn.commit()
			users_conn.close()
			res = make_response("Logged in as admin", 200)
			res.set_cookie("token", token)
			res.set_cookie("admin", "True")
			res.set_cookie("username", username)
			res.set_cookie("email", results[0]["email"])
			res.set_cookie("hospital_name", "Admin")
			return res

	cur.execute("SELECT * FROM users WHERE username = ?", (username,))
	results = cur.fetchall()
	if (len(results) == 1):
		if (sha256_crypt.verify(password, results[0]["password"])):
			token = secrets.token_urlsafe(32)
			cur.execute("INSERT INTO tokens VALUES (?, ?, ?)", (username, token, 0))
			users_conn.commit()
			users_conn.close()
			res = make_response("Logged in as user", 200)
			res.set_cookie("token", token)
			res.set_cookie("admin", "False")
			res.set_cookie("email", results[0]["email"])
			res.set_cookie("username", username)
			res.set_cookie("hospital_id", results[0]["hospital_id"])
			records_conn = None
			records_conn = sqlite3.connect(data_db)
			records_conn.row_factory = sqlite3.Row
			cur = records_conn.cursor()
			cur.execute("SELECT * FROM Hospital WHERE hospital_id = ?", (str(results[0]["hospital_id"]),))
			results = cur.fetchall()
			if (len(results) == 1):
				res.set_cookie("hospital_name", results[0]["hospital_name"])

			return res

	return jsonify(request.form), 403

def userCheck(token):
	if (not token):
		return False
	conn = sqlite3.connect(user_db)
	cur = conn.cursor()
	cur.execute("SELECT * FROM tokens WHERE token = ?;", (token,))
	if (len(cur.fetchall()) > 0):
		return True
	return False

def adminCheck(token):
	if (not token):
		return False
	conn = sqlite3.connect(user_db)
	cur = conn.cursor()
	cur.execute("SELECT * FROM tokens WHERE token = ? AND admin = 1;", (token,))
	if (len(cur.fetchall()) > 0):
		return True
	return False

@app.route('/createUser', methods=['POST'])
def createUser():
	if (adminCheck(request.cookies.get("token"))):
		users_conn = sqlite3.connect(user_db)
		users_conn.row_factory = sqlite3.Row
		cur = users_conn.cursor()
		email = request.form.get("email")
		username = request.form.get("username")
		hospital = request.form.get("hospital")
		try:
			hospital = int(hospital)
		except ValueError as e:
			return "Invalid hospital ID", 400
		if not (username and hospital and email):
			return "400 bad request", 400
		cur.execute("INSERT INTO pending_users VALUES (?, ?, ?, ?)", (username, email.lower(), token, hospital))
		(sendEmail(email, "OPQIC Data Portal Invitation", f"You have been added as a user to the OPQIC data portal with the username {username}\n\nClick on the following link to create your account:\n\n{this_domain}/accountCreate?token={token}"))
		users_conn.commit()
		users_conn.close()
		return "200 Success", 200
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
			print(username)
			print(email)
			return "400 bad request", 400
		cur.execute("INSERT INTO pending_admins VALUES (?, ?, ?)", (username, email.lower(), token))
		(sendEmail(email, "OPQIC Data Portal Invitation", f"You have been added as an admin to the OPQIC data portal with the username {username}\n\nClick on the following link to create your account:\n\n{this_domain}/accountCreate?token={token}"))
		users_conn.commit()
		users_conn.close()
		return "200 Success", 200
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
	thread.start_new_thread(actuallySend, (email, subject, message))

def actuallySend(email, subject, message):
	print("Got here")
	try:
		print(env.email, env.email_pass)
		smtpObj = SMTP_SSL("mail.opqic.org", port=465)
		smtpObj.login(env.email, env.email_pass)
		smtpObj.sendmail("dataportal@opqic.org", email, f"From: {env.email}\r\nTo: {email}\r\nSubject: {subject}\r\n\r\n{message}")
		print("No errors!!")
		smtpObj.quit()
	except SMTPException as e:
		print("Error")
		print(e)

@app.route('/accountCreate', methods=['GET'])
def accountPropose():
	return app.send_static_file("accountCreation.html")

@app.route('/accountAccept', methods=['POST'])
def accountAccept():
	token = request.form.get("token")
	username = request.form.get("username")
	password = request.form.get("password")
	if not token or not username or not password:
		res = make_response("Invalid username or token. Be sure you are using the link and username provided to you in the email.", 400)
		return res
	users_conn = sqlite3.connect(user_db)
	users_conn.row_factory = sqlite3.Row
	cur = users_conn.cursor()
	cur.execute("SELECT * FROM pending_admins WHERE token = ? AND username = ?", (token, username))
	results = cur.fetchall()
	if (len(results) == 1):
		cur.execute("INSERT INTO admins VALUES (?, ?, ?)", (results[0]["email"], username, sha256_crypt.hash(password)))
		cur.execute("DELETE FROM pending_admins WHERE token = ? AND username = ?", (token, username))
		token = secrets.token_urlsafe(32)
		cur.execute("INSERT INTO tokens VALUES (?, ?, ?)", (username, token, 1))
		res = make_response("Logged in as admin", 200)
		users_conn.commit()
		users_conn.close()
		res.set_cookie("token", token)
		res.set_cookie("admin", "True")
		res.set_cookie("username", username)
		res.set_cookie("email", results[0]["email"])
		res.set_cookie("hospital_name", "Admin")
		return res
	print(username, token)
	cur.execute("SELECT * FROM pending_users WHERE token = ? AND username = ?", (token, username))
	results = cur.fetchall()
	if (len(results) >= 1):
		cur.execute("INSERT INTO users VALUES (?, ?, ?)", (results[0]["email"], username, sha256_crypt.hash(password), results[0]["hospital_id"]))
		cur.execute("DELETE FROM pending_users WHERE token = ? AND username = ?", (token, username))
		token = secrets.token_urlsafe(32)
		cur.execute("INSERT INTO tokens VALUES (?, ?, ?)", (username, token, 0))
		users_conn.commit()
		users_conn.close()
		res = make_response("Logged in as user", 200)
		res.set_cookie("token", token)
		res.set_cookie("admin", "False")
		res.set_cookie("username", username)
		res.set_cookie("email", results[0]["email"])
		res.set_cookie("hospital_id", results[0]["hospital_id"])
		records_conn = sqlite3.connect(data_db)
		records_conn.row_factory = sqlite3.Row
		cur = records_conn.cursor()
		cur.execute("SELECT * FROM Hospital WHERE hospital_id = ?", (str(results[0]["hospital_id"]),))
		results = cur.fetchall()
		if (len(results) == 1):
			res.set_cookie("hospital_name", results[0]["hospital_name"])
		return res
	users_conn.close()
	res = make_response("Invalid username or token. Be sure you are using the link and username provided to you in the email.", 400)
	return res

@app.route('/adminInfo', methods=['POST'])
def getUsers():
	token = request.cookies.get("token")
	if not adminCheck(token):
		return "403 Unauthorized", 403
	toSend = {"users": [], "hospitals": []}
	conn = sqlite3.connect(user_db)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("SELECT * FROM users")
	results = cur.fetchall()
	for i in results:
		toSend["users"].append({"username": i["username"], "email": i["email"], "admin": "False", "hospital_id": i["hospital_id"]})
	cur.execute("SELECT * FROM admins")
	results = cur.fetchall()
	for i in results:
		toSend["users"].append({"username": i["username"], "email": i["email"], "admin": "True"})
	conn.close()
	conn = sqlite3.connect(data_db)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("SELECT * FROM Hospital")
	results = cur.fetchall()
	for i in results:
		toSend["hospitals"].append({"hospital_id": i["hospital_id"], "hospital_name": i["hospital_name"]})
	return toSend

@app.route('/deleteUser', methods=['POST'])
def deleteUser():
	token = request.cookies.get("token")
	user = request.form.get("username")
	if not (token and user):
		return "400 Bad Request", 400
	conn = sqlite3.connect(user_db)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("SELECT * FROM tokens WHERE token = ? AND username = ?", (token, user))
	results = cur.fetchall()
	if (len(results) == 1 or adminCheck(token)):
		cur.execute("DELETE FROM tokens WHERE username = ?", (user,))
		cur.execute("DELETE FROM users WHERE username = ?", (user,))
		cur.execute("DELETE FROM admins WHERE username = ?", (user,))
		conn.commit()
		conn.close()
		return "User has been deleted", 200
	return "Invalid username or token", 400

@app.route('/forgotPassword', methods=['GET'])
def forgotPasswordPage():
	return app.send_static_file("forgotPassword.html")

@app.route('/forgotPassword', methods=['POST'])
def forgotPassword():
	username = request.form.get("username")
	email = request.form.get("email")
	if not email or not username:
		return "400 Bad Request", 400
	email = email.lower()
	token = secrets.token_urlsafe(32)
	conn = sqlite3.connect(user_db)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("SELECT * FROM users WHERE username = ? AND email = ?", (username, email))
	results = cur.fetchall()
	if (len(results) >= 1):
		cur.execute("INSERT INTO tokens VALUES (?, ?, ?)", (username, token, 0))
		conn.commit()
		conn.close()
		(sendEmail(email, "OMNO Password Reset", f"You recently requested a password reset for the OMNO data portal. In order to complete this request, click the link below:\n\n{this_domain}/resetPassword?token={token}"))
		return "An email has been sent containing a link to reset your password.", 200
	cur.execute("SELECT * FROM admins WHERE username = ? AND email = ?", (username, email))
	results = cur.fetchall()
	if (len(results) >= 1):
		cur.execute("INSERT INTO tokens VALUES (?, ?, ?)", (username, token, 1))
		conn.commit()
		conn.close()
		(sendEmail(email, "OMNO Password Reset", f"You recently requested a password reset for the OMNO data portal. In order to complete this request, click the link below:\n\n{this_domain}/resetPassword?token={token}&admin=True"))
		return "An email has been sent containing a link to reset your password.", 200
	return "Invalid username or email", 400

@app.route('/resetPassword', methods=['GET'])
def resetPasswordGet():
	return app.send_static_file("resetPassword.html")

@app.route('/resetPassword', methods=['POST'])
def resetPassword():
	password = request.form.get("password")
	token = request.form.get("token")
	if not password or not token:
		return "Invalid token or password", 400
	conn = sqlite3.connect(user_db)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("SELECT * FROM tokens WHERE token = ?", (token,))
	res = cur.fetchall()
	if len(res) >= 1:
		cur.execute(f"UPDATE {('admins' if res[0]['admin'] > 0 else 'users')} SET password = ? WHERE username = ? LIMIT 1;", (sha256_crypt.hash(password), res[0]["username"]))
		cur.execute("DELETE FROM tokens WHERE username = ?;", (res[0]["username"],))
		conn.commit()
		conn.close()
		return "Password reset", 200
	return "Invalid token", 400

if (__name__ == "__main__"):
	app.run()

print('Running website')
