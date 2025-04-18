import smtplib
import ssl
from email.message import EmailMessage
from typing import List


class Notifier:
    def __init__(self, smtp_server: str, port: int, sender_email: str, sender_password: str):
        """
        مقداردهی اولیه به Notifier با اطلاعات SMTP.

        :param smtp_server: آدرس سرور SMTP
        :param port: پورت سرور SMTP
        :param sender_email: ایمیل فرستنده
        :param sender_password: رمز عبور ایمیل فرستنده
        """
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipients: List[str], subject: str, body: str):
        """
        ارسال ایمیل به لیستی از گیرندگان.

        :param recipients: لیست ایمیل گیرندگان
        :param subject: موضوع ایمیل
        :param body: محتوای ایمیل
        """
        message = EmailMessage()
        message["From"] = self.sender_email
        message["To"] = ", ".join(recipients)
        message["Subject"] = subject
        message.set_content(body)

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
                print("ایمیل با موفقیت ارسال شد.")
        except Exception as e:
            print(f"خطا در ارسال ایمیل: {e}")
