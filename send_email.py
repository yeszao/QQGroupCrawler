import time
import itertools

from db.dao import get_qqs, set_sent_status
from mail.aliyun import send_email
from socks import  GeneralProxyError, ProxyConnectionError

subject = "机会难得！美国【高级PHP开发工程师】职位推荐"
content = """
<p>您好，</p>

<p>我是润拉拉的招聘顾问，我们对您在网络上的个人资料印象深刻，认为您非常适合位于美国的【高级PHP开发工程师】岗位。</p>

<p>该职位要求必备如下的一些技能：</p>
<ul>
<li>2 年以上 PHP 后端开发经验。</li>
<li>扎实的 PHP 知识。</li>
<li>扎实的 SQL 和数据库设计知识。</li>
<li>设计模式和面向对象编程。</li>
<li>有各种 API 的开发经验。</li>
<li>理解 MVC 设计，有实际应用 HTML5、JavaScript 和 CSS3 的技术。</li>
</ul>

<p>如果您符合以上条件，这将是一次千载难逢的机会。如果您对这个职位感兴趣，请点击以下链接查看详细信息：</p>

<p><a href="https://runlala.com/job/18addb4e8c9" target="_blank">查看该【高级PHP开发工程师】职位详情</a>。</p>

<p>如果您暂时不考虑这个职位，但认识有兴趣的朋友，请不要犹豫将这个机会介绍给他们。</p>

<p>谢谢！</p>
<p>润拉拉招聘顾问</p>
"""

sender_list = [
    "customer@maila.runlala.org",
    "customer@mailb.runlala.org",
    "customer@mailc.runlala.org",
    "customer@maild.runlala.org",
    "customer@maile.runlala.org",
]
senders = itertools.cycle(sender_list)


def start_send():
    while True:
        qqs = get_qqs('php', 5)
        if len(qqs) == 0:
            break

        sender = senders.__next__()
        emails = [str(qq) + "@qq.com" for qq in qqs]
        print(f"Sending emails to {qqs[0]} - {qqs[-1]} with {sender}")

        try:
            failed = send_email(sender, emails, subject, content)
            failed_qq = []
            if len(failed) > 0:
                for email, fail_mgs in failed.items():
                    failed_qq.append(int(email.split('@')[0]))

            set_sent_status([qq for qq in qqs if qq not in failed_qq])
            print(f"Total [{len(qqs)}], failed [{len(failed)}], success [{len(qqs) - len(failed)}]")
        except (GeneralProxyError, ProxyConnectionError) as e:
            print(f"Error and continue: {e}")
            continue

        time.sleep(3)

    print("All done.")


if __name__ == '__main__':
    start_send()