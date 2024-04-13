from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, Mapped
from database import Base

class TerminalEventModel(Base):
    __tablename__ = 'terminal_events'

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str]
    type: Mapped[str]
    message: Mapped[str]
    created_at: Mapped[datetime]
    # rp: Mapped[int]
    # tn: Mapped[int]
    # mvz: Mapped[int]
    # be_name: Mapped[str]
    # first_name: Mapped[str]
    # last_name: Mapped[str]
    # middle_name: Mapped[Optional[str]]
    # full_name: Mapped[Optional[str]]
    # organization_uid: Mapped[str]
    # birthday: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    # passport: Mapped[Optional[str]]
    # email: Mapped[Optional[str]]
    # open_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # id: Mapped[int] = mapped_column(primary_key=True)
    # service_number: Mapped[int]
    # first_name: Mapped[str]
    # last_name: Mapped[str]
    # middle_name: Mapped[Optional[str]]
    # full_name: Mapped[Optional[str]]
    # organization_uid: Mapped[str]
    # email: Mapped[Optional[str]]
    # open_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    # closed_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __str__(self):
        return f"TerminalEventModel #{self.id}"
