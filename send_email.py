import itertools
import time
from socks import GeneralProxyError, ProxyConnectionError
import logging
from db.dao import get_qqs, set_sent_status, get_email_template, get_all_groups, get_group_by_gid, get_all_senders, \
    increase_sender_count
from mail.aliyun import send_email
from utils import get_today

TEST_GID = 10
SEND_BATCH_SIZE = 5
DAILY_SEND_COUNT_OF_ONE_SENDER = 150
all_senders = get_all_senders()
senders = itertools.cycle(all_senders)
done_senders = set()


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

    logging.info("All done.")


def loop_send_group(group):
    while True:
        qqs = get_qqs(group.gid, SEND_BATCH_SIZE)
        if len(qqs) == 0:
            break
        emails = [str(qq) + "@qq.com" for qq in qqs]

        sender = senders.__next__()
        today = get_today()
        if sender.last_sent_date == today and sender.last_sent_count > DAILY_SEND_COUNT_OF_ONE_SENDER:
            done_senders.add(sender.id)

            if len(done_senders) == len(all_senders):
                logging.info("All senders have sent enough emails today, stop.")
                break
            else:
                logging.info(f"Sender {sender.email} has sent {sender.last_sent_count} emails today, skip.")
                continue

        logging.info(f"Sending emails to {qqs[0]} - {qqs[-1]} with {sender.email}")
        subject, content = get_template(group.email_variable_id)
        try:
            failed = send_email(sender, emails, subject, content)
            failed_qq = []
            if len(failed) > 0:
                for email, fail_mgs in failed.items():
                    failed_qq.append(int(email.split('@')[0]))

            set_sent_status([qq for qq in qqs if qq not in failed_qq])
            sender.last_sent_date = today
            sender.last_sent_count += len(qqs)
            increase_sender_count(sender.id, len(qqs))

            logging.info(f"Total [{len(qqs)}], failed [{len(failed)}], success [{len(qqs) - len(failed)}]")
        except (GeneralProxyError, ProxyConnectionError) as e:
            logging.info(f"Error and continue: {e}")
            continue

        time.sleep(3)


def init_log():
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                        datefmt='%Y-%d-%m %I:%M:%S',
                        level=logging.DEBUG,
                        handlers=[logging.FileHandler('app.log'), logging.StreamHandler()])


if __name__ == '__main__':
    init_log()
    start_send()
    # loop_send_group(get_group_by_gid(TEST_GID))
