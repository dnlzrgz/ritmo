import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base: Any = declarative_base()


class Habit(Base):
    """
    Habits define the habits table which contains the name, description, type, start date, and end date of an habit.
    """

    __tablename__ = "habits"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    type = Column(
        String,
        CheckConstraint("type='boolean' OR type='numerical'"),
        nullable=False,
        default="boolean",
    )
    start_date = Column(Date, nullable=False, default=datetime.datetime.utcnow)
    end_date = Column(Date)


class HabitLog(Base):
    """
    HabitLog define the habit_logs table which contains the habit id, date, completed, and completed_at of an habit.
    """

    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    habit = relationship("Habit", backref=backref("habit_logs", order_by=id))
    date = Column(Date, nullable=False, default=datetime.datetime.utcnow)
    completed = Column(Boolean, nullable=False, default=True)
    completed_at = Column(Date, nullable=False, default=datetime.datetime.utcnow)
