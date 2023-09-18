from datetime import datetime, date
from pydantic import BaseModel


class GroupMember(BaseModel):
    nickname: str
    qq: int
    gender: str
    qq_age: str
    qq_created_at: date
    joint_at: date
    last_active_at: date
    gid: int
