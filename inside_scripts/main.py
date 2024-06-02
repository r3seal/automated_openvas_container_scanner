from general import Main
from mail import Mail
from scan import Scan
import time

if __name__ == "__main__":
    time.sleep(1200)
    scan = Scan("admin", "admin")
    mail = Mail(open("mail.txt", "r").read(), open("password.txt", "r").read())
    Main(mail, scan).run()
