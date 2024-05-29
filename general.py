from datetime import datetime
import time


class Main:
    def __init__(self, mail, scan):
        self.mail = mail
        self.scan = scan
        self.send_period = 18000  # 5 hours
        self.recipients = ["example.mail.test.test@gmail.com"]

    def run(self):
        while True:
            self.scan.print_version()
            target_id = self.scan.create_target()
            task_id = self.scan.get_task_id("python_program_scan")
            task_response = self.scan.start_task(task_id)
            report_id = self.scan.find_report_id_from_task_response(task_response)
            while not self.scan.is_task_finished(report_id):
                time.sleep(600)  # 10 minutes
            self.scan.save_report_to_pdf(report_id, "report.pdf")
            self.send_mail("report.pdf")
            time.sleep(self.send_period)

    def send_mail(self, attachment_path):
        subject = "[Report][Metasploitable][" + str(datetime.now()) + "]"
        body = "Scan of 'Metasploitable'"

        msg = self.mail.create_message(subject, body, self.recipients)
        msg = self.mail.add_attachment(attachment_path, msg)
        self.mail.send_email(self.recipients, msg)
