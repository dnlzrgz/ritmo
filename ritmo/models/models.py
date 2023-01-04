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

# Create a base class for the models to inherit from.
Base: Any = declarative_base()


class Habit(Base):
    """
    Habits define the habits table.
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


class HabitDay(Base):
    """
    HabitDays define the habit_days table.
    """

    __tablename__ = "habit_days"

    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    habit = relationship("Habit", backref=backref("habit_days", order_by=id))
    date = Column(Date, nullable=False, default=datetime.datetime.utcnow)
    completed = Column(Boolean, nullable=False, default=False)
    completed_num = Column(Integer, nullable=False, default=0)


class HabitWeek(Base):
    """
    HabitWeeks define the habit_weeks table, which contains
    summary data about the habits for a week.
    """

    __tablename__ = "habit_weeks"

    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    habit = relationship("Habit", backref=backref("habit_weeks", order_by=id))
    week_start = Column(Date, nullable=False)
    completed_days = Column(Integer, nullable=False)
    modified_date = Column(Date, nullable=False, default=datetime.datetime.utcnow)


class HabitMonth(Base):
    """
    HabitMonths define the habit_months table, which contains
    summary data about the habits for a month.
    """

    __tablename__ = "habit_months"

    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    habit = relationship("Habit", backref=backref("habit_months", order_by=id))
    month_start = Column(Date, nullable=False)
    completed_days = Column(Integer, nullable=False)
    modified_date = Column(Date, nullable=False, default=datetime.datetime.utcnow)
