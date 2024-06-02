from general import Main
from mail import Mail
from scan import Scan
import time

if __name__ == "__main__":
    time.sleep(1200)
    scan = Scan(open("scan_name.txt", "r").read().strip(), open("scan_password.txt", "r").read().strip())
    mail = Mail(open("mail.txt", "r").read().strip(), open("mail_password.txt", "r").read().strip())
    Main(mail, scan).run()
