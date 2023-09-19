from typing import List

from com.models import GroupMember
from db.engine import DbSession
from db.entity import QqGroup, QqUser, qq_users_groups_association


def get_groups() -> List[QqGroup]:
    with DbSession() as session:
        return session.query(QqGroup).filter(QqGroup.crawled == False).all()


def set_group_crawled(gid: int):
    with DbSession() as session:
        group = session.query(QqGroup).filter(QqGroup.gid == gid).first()
        group.crawled = True
        session.commit()


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


