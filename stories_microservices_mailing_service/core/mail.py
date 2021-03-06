from email import message
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



from .config import EmailConfig

class SendMAil(EmailConfig):

    def __init__(self, subject, body, to=None, subtype='html', *args, **kwargs):
        self.subject = subject
        self.body = body
        self.recipients = to or []
        self.subtype = subtype
        self.send_mail_recipient()

    def send_mail_recipient(self):
        for recipient in self.recipients:
            self.send_mail(recipient)
    
    def get_mail_messege(self, recipient):
        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.EMAIL_HOST_USER
        message["To"] = recipient
        if self.subtype == 'html':
            part = MIMEText(self.body, 'html')
        else:
            part = MIMEText(self.body, 'plain')
        message.attach(part)
        return message

    
    def send_mail(self, recipient):
        message = self.get_mail_messege(recipient)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.EMAIL_HOST, 465, context=context) as server:
            server.login(self.EMAIL_HOST_USER, self.EMAIL_HOST_PASSWORD)
            server.sendmail(
                self.EMAIL_HOST_USER, recipient, message.as_string()
            )

# SendMAil(subject="""
#             Hi,
#             How are you?
#             Real Python has many great tutorials:
#             www.realpython.com""",
#             body = """
#             <html>
#             <body>
#                 <p>Hi,<br>
#                 How are you?<br>
#                 <a href="http://www.realpython.com">Real Python</a> 
#                 has many great tutorials.
#                 </p>
#             </body>
#             </html>
#             """,
#             to=['husubayliv@gmail.com'],
#             subtype='html',
# )


