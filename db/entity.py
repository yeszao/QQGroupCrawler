from datetime import datetime, date
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Date, Text, ForeignKey, Table, Boolean

from db.engine import Base, DbEngine

qq_users_groups_association = Table('qq_users_groups_association',
                                    Base.metadata,
                                    Column('qq', BigInteger, ForeignKey('qq_users.qq')),
                                    Column('gid', BigInteger, ForeignKey('qq_groups.gid')),
                                    Column('joint_at', Date, nullable=False, default=date.min),
                                    Column('last_active_at', Date, nullable=False, default=date.min),
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
    qq = Column(BigInteger, nullable=False, unique=True)
    gender = Column(String(2), nullable=False)
    qq_age = Column(String(5), nullable=False)
    qq_created_at = Column(Date, nullable=False, default=date.today)


class QqGroup(BaseEntity):
    __tablename__ = 'qq_groups'
    gid = Column(BigInteger, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    login_qq = Column(BigInteger, nullable=False)
    crawled = Column(Boolean, nullable=False, default=False)


if __name__ == '__main__':
    Base.metadata.create_all(DbEngine)
