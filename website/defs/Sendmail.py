from email.message import EmailMessage
import smtplib


def sendmail(**kwargs):
    try:
        email = EmailMessage()
        email['Subject'] = kwargs['subject']
        email['From'] = 'REDACTED'
        email['To'] = kwargs['receiver']
        email.set_content(kwargs['body'], subtype='html')

        with smtplib.SMTP("REDACTED", 000) as s:
            s.starttls()
            s.login('REDACTED', 'REDACTED')
            s.send_message(email)
            
    except Exception as e:
        print(e)