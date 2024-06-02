from datetime import datetime
import time


class Main:
    def __init__(self, mail, scan):
        self.mail = mail
        self.scan = scan
        self.send_period = 18000  # 5 hours
        self.recipients = []

    def run(self):
        while True:
            hosts_list = []

            with open("hostIPS.txt", "r") as f:
                for line in f:
                    hosts_list.append(line)
            with open("recipients.txt", "r") as f:
                for line in f:
                    self.recipients.append(line.strip())

            target_id = self.scan.create_target("automated_openvas_targets", hosts_list=hosts_list)
            task_id = self.scan.create_task("automated_openvas_scan", target_id)
            task_response = self.scan.start_task(task_id)
            report_id = self.scan.find_report_id_from_task_response(task_response)
            while not self.scan.is_task_finished(report_id):
                time.sleep(600)  # 10 minutes
            self.scan.save_report_to_pdf(report_id, "report.pdf")
            self.send_mail("report.pdf")
            time.sleep(self.send_period)

    def send_mail(self, attachment_path):
        subject = "[Scan Report][" + str(datetime.now()) + "]"
        body = "Automated scan results"

        msg = self.mail.create_message(subject, body, self.recipients)
        msg = self.mail.add_attachment(attachment_path, msg)
        self.mail.send_email(self.recipients, msg)
