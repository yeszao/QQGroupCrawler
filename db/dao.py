from typing import List
from sqlalchemy import text
from com.models import GroupMember
from db.engine import DbSession
from db.entity import QqGroup, QqUser, qq_users_groups_association, EmailVariable, EmailTemplate, Sender
from utils import get_today


def get_groups() -> List[QqGroup]:
    with DbSession() as session:
        return session.query(QqGroup).filter(QqGroup.crawled == False).all()


def set_group_crawled(gid: int):
    with DbSession() as session:
        group = session.query(QqGroup).filter(QqGroup.gid == gid).first()
        group.crawled = True
        session.commit()


def get_all_groups() -> List[QqGroup]:
    with DbSession() as session:
        return session.query(QqGroup).all()


def get_all_senders() -> List[Sender]:
    with DbSession() as session:
        return session.query(Sender).all()


def increase_sender_count(sender_id: int, num: int):
    today = get_today()
    with DbSession() as session:
        sender = session.query(Sender).filter(Sender.id == sender_id).first()
        if sender.last_sent_date == today:
            sender.last_sent_count += num
        else:
            sender.last_sent_date = today
            sender.last_sent_count = num
        session.commit()


def get_group_by_gid(gid: int) -> QqGroup:
    with DbSession() as session:
        return session.query(QqGroup).filter(QqGroup.gid == gid).first()


def get_or_add_group(g: dict, login_qq: int) -> QqGroup:
    with DbSession(expire_on_commit=False) as session:
        group = session.query(QqGroup).filter(QqGroup.gid == g["gid"]).first()
        if group:
            return group

        group = QqGroup(gid=g["gid"], name=g["name"], login_qq=login_qq, crawled=False)
        session.add(group)
        session.commit()
        return session.query(QqGroup).filter(QqGroup.gid == g["gid"]).first()


def save_member(m: GroupMember, gid: int):
    with DbSession() as session:
        user = session.query(QqUser).filter(QqUser.qq == m.qq).first()
        if user is None:
            user = QqUser(nickname=m.nickname, qq=m.qq, gender=m.gender, qq_age=m.qq_age, qq_created_at=m.qq_created_at)
            session.add(user)

        group = session.query(QqGroup).filter(QqGroup.gid == gid).first()

        new_association = {
            'qq': user.qq,
            'gid': group.gid,
            'joint_at': m.joint_at,
            'last_active_at': m.last_active_at,
        }
        session.execute(qq_users_groups_association.insert().values(new_association))

        session.commit()


def get_qqs(gid: int, limit: int) -> List[int]:
    with DbSession() as session:
        sql = text("""
            select distinct qu.qq from qq_users qu
            inner join qq_users_groups_association quga on qu.qq = quga.qq
            where quga.gid = :gid and qu.sent = 0
            limit :limit
        """)
        result = session.execute(sql, {"gid": gid, "limit": limit})
        return [row[0] for row in result]


def set_sent_status(all_qqs: List[int]):
    if len(all_qqs) == 0:
        return
    with DbSession() as session:
        sql = text("""
            update qq_users set sent = 1 where qq in :qqs
        """)
        session.execute(sql, {"qqs": all_qqs})
        session.commit()


def get_email_template(variable_id: int) -> (EmailVariable, EmailTemplate):
    with DbSession() as session:
        return session.query(EmailVariable, EmailTemplate)\
            .join(EmailTemplate, EmailVariable.template_id == EmailTemplate.id)\
            .filter(EmailVariable.id == variable_id)\
            .first()

