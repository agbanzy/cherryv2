import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def read_email(user_email, password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(user_email, password)
    mail.select("inbox")

    _, message_numbers = mail.uid('search', None, "ALL")
    message_numbers = message_numbers[0].split()

    emails = []

    for num in message_numbers:
        _, data = mail.uid('fetch', num, '(BODY[HEADER.FIELDS (SUBJECT FROM DATE)])')
        raw_email = data[0][1].decode("utf-8")
        email_message = email.message_from_string(raw_email)
        emails.append({
            'from': email_message['From'],
            'subject': decode_header(email_message['Subject'])[0][0].decode(),
            'date': email_message['Date']
        })

    return emails

def send_email(user_email, password, recipient_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = user_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user_email, password)
    text = msg.as_string()
    server.sendmail(user_email, recipient_email, text)
    server.quit()
