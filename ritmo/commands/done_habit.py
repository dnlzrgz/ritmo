import datetime

import click
from sqlalchemy.orm import Session

from ritmo.decorators import with_sqlalchemy_error_handling
from ritmo.models import Habit, HabitLog
from ritmo.sessions import create_local_session


def mark_as_done(sess: Session, name: str) -> None:
    """
    Mark a habit as done.
    If the habit is of type 'numerical', the number of completed days will be incremented.

    Args:
        sess: The database session.
        name: The name of the habit to mark as done. If the habit does not exist, it will not be created.
    """

    habit = sess.query(Habit).filter(Habit.name == name).first()

    if not habit:
        click.echo(f"Habit '{name}' not found.")

    habit_log = sess.query(HabitLog).filter(HabitLog.habit_id == habit.id)
    if habit_log.count() == 0 or habit.type == "numerical":
        habit_day = HabitLog(habit_id=habit.id)
        sess.add(habit_day)
        sess.commit()


@click.command(name="done", help="Mark a habit as done.")
@click.argument("name", nargs=1, type=str)
@with_sqlalchemy_error_handling
def mark_as_done_cmd(name: str):
    local_session = create_local_session()
    with local_session.begin() as sess:
        mark_as_done(sess, name)


def mark_as_undone(sess: Session, name: str) -> None:
    """
    Mark a habit as undone.
    If the habit is of type 'numerical', the number of times completed will be decremented. If the number of times completed
    reaches 0, the habit_day will be deleted.

    Args:
        sess: The database session.
        name: The name of the habit to mark as undone.
    """

    habit = sess.query(Habit).filter(Habit.name == name).first()

    if not habit:
        click.echo(f"Habit '{name}' not found.")
        return

    habit_log = (
        sess.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit.id
            and habit.completed_at == datetime.datetime.today()
        )
        .order_by(HabitLog.completed_at)
    )

    if habit_log.count() == 0:
        click.echo(f"Habit '{name}' has not been done today.")
        return
    else:
        habit_log = habit_log.first()
        sess.delete(habit_log)
        sess.commit()


@click.command(name="undo", help="Mark a habit as undone.")
@click.argument("name", nargs=1, type=str)
@with_sqlalchemy_error_handling
def mark_as_undone_cmd(name: str):
    local_session = create_local_session()
    with local_session.begin() as sess:
        mark_as_undone(sess, name)
