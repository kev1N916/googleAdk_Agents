import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

class MailSender:
    def __init__(self):
        load_dotenv()
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465

    def sendMail(self, subject, recipient, body):
        # Create a plain text email message
        msg = MIMEText(body, "plain")
        msg["From"] = self.email_address
        msg["To"] = recipient
        msg["Subject"] = subject

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.email_address, self.email_password)
                server.sendmail(self.email_address, recipient, msg.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print("Failed to send email:", e)

# Example usage:
# if __name__ == "__main__":
#     mailer = MailSender()
#     mailer.sendMail(
#         subject="Hello from MailSender!",
#         recipient="kevintj169@gmail.com",
#         body="This is a plain text email from Python using the MailSender class."
#     )
