import smtplib
from email.message import EmailMessage
from email.utils import formataddr


def send_email(receivers, subject, body):
    msg = EmailMessage()
    port = 465
    host = "smtpdm.aliyun.com"
    sender = "no-reply@mail.runlala.com"
    password = "UkB78yxqf0t"

    msg['From'] = formataddr(('润拉拉', sender))
    # msg['To'] = receivers
    msg['Bcc'] = receivers
    msg['Subject'] = subject
    msg.add_alternative(body, subtype='html')

    with smtplib.SMTP_SSL(host, port, timeout=10) as server:
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
