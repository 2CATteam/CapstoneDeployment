import env
from smtplib import SMTP_SSL, SMTPException

print("Got here")
try:

	email = "2CATteam@gmail.com"
	subject = "test"
	message = "This is a test"

	print(env.email, env.email_pass)
	smtpObj = SMTP_SSL("mail.opqic.org", port=465)
	smtpObj.set_debuglevel(1)
	smtpObj.login(env.email, env.email_pass)
	print("Got here too")
	smtpObj.sendmail("dataportal@opqic.org", email, f"From: {env.email}\r\nTo: {email}\r\nSubject: {subject}\r\n\r\n{message}")
	print("No errors!")
	smtpObj.quit()
except SMTPException as e:
	print("Error")
	print(e)
