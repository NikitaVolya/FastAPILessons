from sqlalchemy import Table, Column, Integer, ForeignKey
from db.session import Base


user_event = Table(
    "user_event",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("event_id", Integer, ForeignKey("event.id"))
)