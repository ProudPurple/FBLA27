from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    sessionmaker,
)

from .paths import user_data_dir

DB_PATH = user_data_dir() / "app.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class SignupEvent(Base):
    __tablename__ = "signup_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    last_synced: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    slots: Mapped[list["SignupSlot"]] = relationship(
        back_populates="event", cascade="all, delete-orphan", order_by="SignupSlot.name"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "last_synced": self.last_synced.isoformat() if self.last_synced else None,
            "slots": [slot.to_dict() for slot in self.slots],
        }


class SignupSlot(Base):
    """One slot category within a sign-up sheet, e.g. "Teacher Volunteers"."""

    __tablename__ = "signup_slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("signup_events.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slots_total: Mapped[int] = mapped_column(Integer, default=0)
    slots_filled: Mapped[int] = mapped_column(Integer, default=0)

    event: Mapped[SignupEvent] = relationship(back_populates="slots")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slots_total": self.slots_total,
            "slots_filled": self.slots_filled,
        }


def init_db() -> None:
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return SessionLocal()
