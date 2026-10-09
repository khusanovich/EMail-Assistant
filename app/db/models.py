"""SQLAlchemy database models."""

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class ProviderType(str, PyEnum):
    """Email provider types."""

    GMAIL = "gmail"
    IMAP = "imap"
    OUTLOOK = "outlook"


class EventType(str, PyEnum):
    """Application event types with status priority."""

    APPLICATION_SENT = "application_sent"
    IN_REVIEW = "in_review"
    ASSESSMENT = "assessment"
    INTERVIEW_INVITE = "interview_invite"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    REJECTION = "rejection"
    OFFER = "offer"
    WITHDRAWN = "withdrawn"
    GHOSTED = "ghosted"
    OTHER_JOB_RELATED = "other_job_related"


# Status priority for determining current_status
STATUS_PRIORITY = {
    EventType.OFFER: 9,
    EventType.REJECTION: 8,
    EventType.INTERVIEW_SCHEDULED: 7,
    EventType.INTERVIEW_INVITE: 6,
    EventType.ASSESSMENT: 5,
    EventType.IN_REVIEW: 4,
    EventType.APPLICATION_SENT: 3,
    EventType.WITHDRAWN: 2,
    EventType.GHOSTED: 1,
    EventType.OTHER_JOB_RELATED: 0,
}


class MailAccount(Base):
    """Email account configuration."""

    __tablename__ = "mail_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    credentials_ref: Mapped[str] = mapped_column(
        Text, nullable=True
    )  # JSON or file path reference
    last_sync_cursor: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )  # historyId or IMAP UID
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    emails: Mapped[list["Email"]] = relationship("Email", back_populates="account")


class Email(Base):
    """Email message."""

    __tablename__ = "emails"
    __table_args__ = (
        UniqueConstraint("account_id", "provider_message_id", name="uq_account_message"),
        Index("ix_emails_received_at", "received_at"),
        Index("ix_emails_is_job_related", "is_job_related"),
        Index("ix_emails_thread_id", "thread_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("mail_accounts.id"), nullable=False
    )
    provider_message_id: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # Unique per account
    thread_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    from_address: Mapped[str] = mapped_column(String(255), nullable=False)
    from_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    body_text: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # Truncated to ~4000 chars
    received_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_job_related: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    notified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    account: Mapped["MailAccount"] = relationship("MailAccount", back_populates="emails")
    events: Mapped[list["ApplicationEvent"]] = relationship(
        "ApplicationEvent", back_populates="email"
    )


class Application(Base):
    """Job application."""

    __tablename__ = "applications"
    __table_args__ = (Index("ix_applications_company_domain", "company_domain"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    company_domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(500), nullable=False)
    source: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # LinkedIn, StepStone, etc.
    first_contact_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    current_status: Mapped[str] = mapped_column(
        String(50), default=EventType.APPLICATION_SENT.value, nullable=False
    )
    last_event_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    events: Mapped[list["ApplicationEvent"]] = relationship(
        "ApplicationEvent", back_populates="application", order_by="ApplicationEvent.event_date"
    )


class ApplicationEvent(Base):
    """Event in the application timeline."""

    __tablename__ = "application_events"
    __table_args__ = (
        Index("ix_events_application_id", "application_id"),
        Index("ix_events_event_date", "event_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("applications.id"), nullable=False
    )
    email_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("emails.id"), nullable=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    interview_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )  # For interview events
    llm_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    llm_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    needs_review: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    application: Mapped["Application"] = relationship("Application", back_populates="events")
    email: Mapped["Email"] = relationship("Email", back_populates="events")
