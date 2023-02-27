import smtplib
from email.mime.text import MIMEText


def send_email(subject, body, recipients):
    sender = "lcatool.mail@gmail.com"
    password = "toxz tbrl ilhc iabe"  # TODO Not secured! Try to retrieved the password securely
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()
