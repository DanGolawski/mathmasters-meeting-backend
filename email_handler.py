from app_data import EMAIL_DATA
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def create_message(receiver, subject, text):
    message = MIMEMultipart()
    message['From'] = EMAIL_DATA['email']
    message['To'] = receiver
    message['Subject'] = subject
    message.attach(MIMEText(text, 'plain'))
    return message

def send_message(message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_DATA['email'], EMAIL_DATA['password'])
        server.sendmail(EMAIL_DATA['email'], message['TO'], message.as_string())
        server.quit()

        return 'Email Sent!'
    except Exception as e:
        return str(e)
