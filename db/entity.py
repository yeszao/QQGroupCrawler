from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Text, ForeignKey, Table, Boolean

from db.engine import Base, DbEngine


job_skill_association = Table('qq_users_groups_association',
                              Base.metadata,
                              Column('qq', Integer, ForeignKey('qq_users.qq')),
                              Column('gid', Integer, ForeignKey('qq_groups.gid')),
                              Column('joint_at', Date, nullable=False, default=datetime.min),
                              Column('last_active_at', Date, nullable=False, default=datetime.min),
                              )


class BaseEntity(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class QqUser(BaseEntity):
    __tablename__ = 'qq_users'
    nickname = Column(String(100), nullable=False, default='')
    qq = Column(Integer, nullable=False, unique=True)
    gender = Column(String(2), nullable=False)
    qq_age = Column(String(5), nullable=False)


class QqGroup(BaseEntity):
    __tablename__ = 'qq_groups'
    gid = Column(Integer, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    admin_qq = Column(Integer, nullable=False)
    crawled = Column(Boolean, nullable=False, default=False)


if __name__ == '__main__':
    Base.metadata.create_all(DbEngine)


