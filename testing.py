import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from email.utils import formataddr
from datetime import datetime


headers = {
    "from": ("Fullstack", "no-reply@eliaseriksson.io"),
    "to": [
        ("Elias Eriksson", "eliaseriksson95@gmail.com"),
    ],
}

mail = MIMEMultipart()
mail["From"] = formataddr(("Fullstack", "no-reply@eliaseriksson.io"))
mail["To"] = ", ".join([formataddr(("Elias Eriksson", "eliaseriksson95@gmail.com"))])
mail["Date"] = formatdate(datetime.now().timestamp())
mail["Subject"] = "Testing sending mail with python+postfix"

mail.attach(MIMEText("Hello world!"))

with smtplib.SMTP("192.168.1.20", 587) as connection:
    connection.starttls()
    connection.sendmail(
        headers["from"][1], [mail for name, mail in headers["to"]], mail.as_string()
    )
    connection.close()
