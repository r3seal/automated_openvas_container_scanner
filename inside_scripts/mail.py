import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class Mail:

    def __init__(self, sender, password):
        self.sender = sender
        self.password = password

    def send_email(self, recipients, message):
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(self.sender, self.password)
        smtp_server.sendmail(self.sender, recipients, message.as_string())
        smtp_server.quit()

    def create_message(self, subject, body, recipients):
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = self.sender
        message['To'] = ', '.join(recipients)

        message.attach(MIMEText(body))

        return message

    def add_attachment(self, attachment_path, message):
        with open(attachment_path, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=attachment_path)
        part['Content-Disposition'] = f'attachment; filename="{attachment_path}"'
        message.attach(part)

        return message
