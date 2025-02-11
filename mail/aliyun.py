import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from tenacity import wait_random_exponential, stop_after_attempt, retry
import requests
import socks

from db.entity import Sender


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def send_email(sender: Sender, receivers, subject, body) -> dict:
    msg = EmailMessage()
    msg['From'] = formataddr(('润拉拉', sender.email))
    # msg['To'] = receivers
    msg['Bcc'] = receivers
    msg['Subject'] = subject
    msg.add_alternative(body, subtype='html')

    # proxy_ip, proxy_port = get_proxy()
    # print(f"Using proxy {proxy_ip}:{proxy_port}")
    # proxy = socks.socksocket()
    # proxy.setproxy(socks.HTTP, proxy_ip, proxy_port)
    # proxy.connect((host, port))

    with smtplib.SMTP_SSL(sender.smtp_server, sender.smtp_port, timeout=20) as server:
        server.login(sender.email, sender.password)
        return server.send_message(msg)


def get_proxy() -> (str, int):
    resp = requests.get('http://localhost:5555/random')
    proxy = resp.text.split(':')
    return proxy[0], int(proxy[1])
