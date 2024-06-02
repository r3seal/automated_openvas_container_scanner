from general import Main
from mail import Mail
from scan import Scan
import time

if __name__ == "__main__":
    time.sleep(1200)
    scan = Scan("admin", "admin")
    mail = Mail("example.mail.test.test@gmail.com", "crbhqbaqllvulyme")
    Main(mail, scan).run()
