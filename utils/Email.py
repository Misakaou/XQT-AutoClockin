import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

class Email:
    _smtp_host = None
    _smtp_port = None
    _smtp_sender_email = None
    _smtp_sender_password = None
    _smtp_server = None
    _multi_part = None
    
    def __init__(self, smtp_host, smtp_port, smtp_sender_email, smtp_sender_password) -> None:
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._smtp_sender_email = smtp_sender_email
        self._smtp_sender_password = smtp_sender_password
        try:
            self._smtp_server = smtplib.SMTP_SSL(host=self._smtp_host, port=self._smtp_port)
        except:
            self._smtp_server = smtplib.SMTP(host=self._smtp_host, port=self._smtp_port)
            self._smtp_server.ehlo()
            self._smtp_server.starttls()
        try:
            self._smtp_server.login(self._smtp_sender_email, self._smtp_sender_password)
        except smtplib.SMTPException as e:
            raise Exception('email error: ' + str(e))
        self._multi_part = MIMEMultipart()
    
    def send(self, smtp_receiver_list_list:list, email_subject:str, email_text:str) -> bool:
        smtp_receiver_list_list = ', '.join(smtp_receiver_list_list)
        self._multi_part['From'] = self._smtp_sender_email
        self._multi_part['To'] = smtp_receiver_list_list
        # self._multi_part['Cc'] = None
        # self._multi_part['Bcc'] = None
        self._multi_part['Subject'] = Header(email_subject, "utf-8")
        self._multi_part.attach(MIMEText(email_text, 'plain', 'utf-8'))
        try:
            self._smtp_server.sendmail(self._smtp_sender_email, smtp_receiver_list_list, self._multi_part.as_string())
            return True
        except smtplib.SMTPException as e:
            return False
    
    def quit(self):
        self._smtp_server.quit()
