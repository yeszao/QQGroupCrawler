import smtplib
from email.message import EmailMessage
from email.utils import formataddr

import requests
import socks


def send_email(sender, receivers, subject, body) -> dict:
    msg = EmailMessage()
    port = 465
    host = "smtpdm.aliyun.com"
    password = "UkB78yxqf0t"

    msg['From'] = formataddr(('润拉拉', sender))
    # msg['To'] = receivers
    msg['Bcc'] = receivers
    msg['Subject'] = subject
    msg.add_alternative(body, subtype='html')

    # proxy_ip, proxy_port = get_proxy()
    # print(f"Using proxy {proxy_ip}:{proxy_port}")
    # proxy = socks.socksocket()
    # proxy.setproxy(socks.HTTP, proxy_ip, proxy_port)
    # proxy.connect((host, port))

    with smtplib.SMTP_SSL(host, port, timeout=10) as server:
        server.login(sender, password)
        return server.send_message(msg)


def get_proxy() -> (str, int):
    resp = requests.get('http://localhost:5555/random')
    proxy = resp.text.split(':')
    return proxy[0], int(proxy[1])
