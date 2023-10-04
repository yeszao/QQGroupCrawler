import itertools
import time
from socks import GeneralProxyError, ProxyConnectionError

from db.dao import get_qqs, set_sent_status, get_email_template, get_all_groups, get_group_by_gid
from mail.aliyun import send_email

TEST_GID = 10
sender_list = [
    "customer@maila.runlala.org",
    "customer@mailb.runlala.org",
    "customer@mailc.runlala.org",
    "customer@maild.runlala.org",
    "customer@maile.runlala.org",
]
senders = itertools.cycle(sender_list)


def get_template(variable_id: int) -> (str, str):
    var, t = get_email_template(variable_id)

    subject = t.subject
    content = t.content
    for k, v in var.variables.items():
        subject = subject.replace("{" + k + "}", v)
        content = content.replace("{" + k + "}", v)
    return subject, content


def start_send():
    groups = get_all_groups()
    for group in groups:
        if group.email_variable_id == 0:
            continue
        loop_send_group(group)

    print("All done.")


def loop_send_group(group):
    while True:
        qqs = get_qqs(group.gid, 5)
        if len(qqs) == 0:
            break

        sender = senders.__next__()
        emails = [str(qq) + "@qq.com" for qq in qqs]
        print(f"Sending emails to {qqs[0]} - {qqs[-1]} with {sender}")

        subject, content = get_template(group.email_variable_id)
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

    print(f"Done for group {group.gid} - {group.name}")


if __name__ == '__main__':
    loop_send_group(get_group_by_gid(TEST_GID))
