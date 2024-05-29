# import smtplib
# from datetime import datetime
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
#
#
# class Mail:
#
#     def send_email(self, sender, recipients, password, msg):
#         smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#         smtp_server.login(sender, password)
#         smtp_server.sendmail(sender, recipients, msg.as_string())
#         smtp_server.quit()
#
#     def create_msg(self, subject, body, sender, recipients):
#         msg = MIMEMultipart()
#         msg['Subject'] = subject
#         msg['From'] = sender
#         msg['To'] = ', '.join(recipients)
#
#         msg.attach(MIMEText(body))
#
#         return msg
#
#     def add_attachment(self, attachment_path, msg):
#         with open(attachment_path, "rb") as attachment:
#             part = MIMEApplication(attachment.read(), Name=attachment_path)
#         part['Content-Disposition'] = f'attachment; filename="{attachment_path}"'
#         msg.attach(part)
#
#         return msg
#
#
# import gvm
# from gvm.protocols.latest import Gmp
# from gvm.xml import pretty_print
# from lxml import etree
# import base64
# import io
# import time
#
#
# # connect to openvas
# connection = gvm.connections.UnixSocketConnection(path='/run/gvmd/gvmd.sock')
# with Gmp(connection=connection) as gmp:
#     gmp.authenticate(username='admin', password='c5dd894a-3bb9-449d-9bad-034e9cd7fb51')
#
#
#     # find task_id of "scan" task
#     response = gmp.get_tasks(filter_string='python_program_scan')
#     root = etree.fromstring(response)
#     task_element = root.find('.//task')
#     task_id = task_element.get('id')
#     print("Task id: " + task_id)
#
#     # start task
#     task_response = gmp.start_task(task_id)
#     print("Task response: " + task_response)
#
#     # find report_id from task_response
#     root = etree.fromstring(task_response)
#     report_id = root.find('report_id').text
#     print("Report id: " + report_id)
#
#     # check if task is done
#     while(True):
#         report = gmp.get_report(report_id)
#         first_index = report.index('<scan_run_status>')
#         last_index = report.index('</scan_run_status>')
#         status = report[first_index + len('<scan_run_status>'): last_index]
#         print("Status of task: " + status)
#         if status == "Done":
#             break
#         else:
#             time.sleep(300)
#
#     # get xml of pdf report
#     report = gmp.get_report(report_id, report_format_id='c402cc3e-b531-11e1-9163-406186ea4fc5')
#
#     # save report to pdf file
#     start_index = report.index('</report_format>')
#     last_index = report.index('</report>')
#
#     encoded_report_pdf = report[start_index + len('</report_format>'): last_index]
#
#     decoded_bytes = base64.b64decode(encoded_report_pdf)
#
#     with open("report.pdf", 'wb') as f:
#         f.write(decoded_bytes)
#
#     # send mail
#     subject = "Email Subject"
#     body = "This is the body of the text message"
#     attachment_path = "report.pdf"
#
#     sender = "example.mail.test.test@gmail.com"
#     recipients = ["example.mail.test.test@gmail.com"]
#     password = "crbhqbaqllvulyme"
#
#     mail = Mail()
#     msg = mail.create_msg(subject, body, sender, recipients)
#     msg = mail.add_attachment(attachment_path, msg)
#     mail.send_email(sender, recipients, password, msg)

from PIL import Image
im = Image.open('favorite-hiking-place.png')
print(im.getexif())
