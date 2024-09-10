import enum
import uuid

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sql import Base


class UserStatus(enum.Enum, str):
    blocked = "blocked"
    user = "user"
    admin = "admin"
    owner = "owner"


class MemberStatus(enum.Enum, str):
    executor = "executor"
    admin = "admin"
    owner = "owner"


class EventStatus(enum.Enum, str):
    inactive = "inactive"
    in_progress = "in_progress"
    completed = "completed"


class EventType(enum.Enum, str):
    planned = "planned"
    disposable = "disposable"
    cycled = "cycled"


class TaskStatus(enum.Enum, str):
    wait = "wait"
    error = "error"
    in_process = "in_process"
    completed = "completed"


class TaskType(enum.Enum, str):
    optional = "optional"
    disposable = "disposable"
    cycled = "cycled"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str]
    email: Mapped[str]
    tel: Mapped[str | None] = mapped_column(nullable=True, default=None)
    password: Mapped[str]
    salt: Mapped[str]
    status: Mapped[UserStatus] = mapped_column(default=UserStatus.user)
    timestanp: Mapped[DateTime] = mapped_column(default=func.now)

    event_group_members: Mapped[list["EventGroupMember"]] = relationship()


class EventGroup(Base):
    __tablename__ = "event_groups"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str]
    subtitle: Mapped[str | None] = mapped_column(nullable=True, default=None)
    description: Mapped[str | None] = mapped_column(
        nullable=True, default=None
    )
    timestanp: Mapped[DateTime] = mapped_column(default=func.now)

    event_group_members: Mapped[list["EventGroupMember"]] = relationship()
    events: Mapped[list["Event"]] = relationship()


class EventGroupMember(Base):
    __tablename__ = "event_group_members"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    event_group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("event_groups.id"))
    status: Mapped[MemberStatus] = mapped_column(default=MemberStatus.executor)
    timestanp: Mapped[DateTime] = mapped_column(default=func.now)

    user: Mapped["User"] = relationship()
    event_group: Mapped["EventGroup"] = relationship()
    events: Mapped[list["Event"]] = relationship()
    tasks: Mapped[list["Task"]] = relationship()


class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    member_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("event_group_members.id")
    )
    event_group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("event_groups.id")
    )
    name: Mapped[str]
    subtitle: Mapped[str | None] = mapped_column(nullable=True, default=None)
    description: Mapped[str | None]  = mapped_column(
        nullable=True, default=None
    )
    type: Mapped[EventType]
    status: Mapped[EventStatus] = mapped_column(default=EventStatus.inactive)
    start_at: Mapped[str | None] = mapped_column(nullable=True, default=None)
    finish_at: Mapped[str | None] = mapped_column(nullable=True, default=None)
    timestanp: Mapped[DateTime] = mapped_column(default=func.now)

    event_group: Mapped["EventGroup"] = relationship()
    event_group_member: Mapped["EventGroupMember"] = relationship()
    tasks: Mapped[list["Task"]] = relationship()


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("events.id"))
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("event_group_members.id")
    )
    assigned_member_id: Mapped[uuid.UUID | None] = mapped_column(
        nullable=True, default=None
    )
    name: Mapped[str]
    subtitle: Mapped[str | None] = mapped_column(nullable=True, default=None)
    description: Mapped[str | None] = mapped_column(
        nullable=True, default=None
    )
    type: Mapped[TaskType]
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.wait)
    do_before: Mapped[bool]
    do_during: Mapped[bool]
    do_after: Mapped[bool]
    timestanp: Mapped[DateTime] = mapped_column(default=func.now)

    event: Mapped["Event"] = relationship()
    created_by: Mapped["EventGroupMember"] = relationship()