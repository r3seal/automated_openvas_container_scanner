from general import Main
from mail import Mail
from scan import Scan

# docker run --detach --publish 8080:9392 -e PASSWORD="admin" --name openvas immauss/openvas --publish 9390:9390 -e HTTPS=true

if __name__ == "__main__":
    scan = Scan("admin", "admin")
    mail = Mail("example.mail.test.test@gmail.com", "crbhqbaqllvulyme")
    Main(mail, scan).run()
