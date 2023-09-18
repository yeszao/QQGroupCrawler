from datetime import datetime
from pydantic import BaseModel


class GroupMember(BaseModel):
    nickname: str
    qq: int
    gender: str
    qq_age: str
    joint_at: datetime
    last_active_at: datetime
