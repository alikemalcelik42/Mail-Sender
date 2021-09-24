from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import sys, smtplib


# Mail Gönderici

class Window(QWidget):
    def __init__(self, title, shape, icon):
        super().__init__()
        self.title = title
        self.x, self.y, self.w, self.h = shape
        self.icon = QIcon(icon)
        self.vbox = QVBoxLayout()
        self.initUI()
        self.setLayout(self.vbox)
        self.show()

    def SendMail(self):
        from_mail = self.from_mail_text.text()
        to_mail = self.to_mail_text.text()
        subject = self.subject_text.text()
        context = self.context_text.toPlainText()
        passwd = self.passwd_text.text()

        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.ehlo()
        smtp.starttls()
        try:
            smtp.login(from_mail, passwd)
        except smtplib.SMTPAuthenticationError:
            QMessageBox.warning(self, "Mail Sender", "Couldn't login to the server!")
            exit()

        msg = MIMEMultipart()
        msg["From"] = from_mail
        msg["To"] = to_mail
        msg["Subject"] = subject

        message = context
        msg.attach(MIMEText(message, "plain"))
        msg = msg.as_string()

        try:
            smtp.sendmail(from_mail, to_mail, msg)
        except:
            QMessageBox.warning(self, self.title, "Couldn't send mail!")
            exit()

        QMessageBox.information(self, self.title, "Mail sended!")
        
        smtp.close()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)
        self.setGeometry(self.x, self.y, self.w, self.h)
        self.setFont(QFont("Arial", 12))

        self.from_mail_text = QLineEdit()
        self.passwd_text = QLineEdit()
        self.passwd_text.setEchoMode(QLineEdit.Password)
        self.to_mail_text = QLineEdit()
        self.subject_text = QLineEdit()
        self.context_text = QTextEdit()
        self.send_btn = QPushButton(text="Send", clicked=self.SendMail)

        grid = QGridLayout()
        grid.addWidget(QLabel(text="From Mail: "), 1, 0)
        grid.addWidget(self.from_mail_text, 1, 1)
        grid.addWidget(QLabel(text="Password: "))
        grid.addWidget(self.passwd_text)
        grid.addWidget(QLabel(text="To Mail: "))
        grid.addWidget(self.to_mail_text)
        grid.addWidget(QLabel(text="Subject: "))
        grid.addWidget(self.subject_text)
        grid.addWidget(QLabel(text="Context: "))
        grid.addWidget(self.context_text)
        grid.addWidget(self.send_btn, 6, 0, 1, 2)
        self.vbox.addLayout(grid)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window("Mail Sender", (100, 100, 500, 500), "../img/icon.jpg")
    app.setStyle("Windows")
    app.exec_()