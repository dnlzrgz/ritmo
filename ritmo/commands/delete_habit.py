import click
from sqlalchemy.orm import Session

from ritmo.decorators import with_sqlalchemy_error_handling
from ritmo.models import Habit, HabitLog
from ritmo.sessions import create_local_session


def delete_habit(sess: Session, name: str) -> None:
    """
    Delete a habit.

    Args:
        sess: The database session.
        name: The name of the habit.
    """

    habit = sess.query(Habit).filter(Habit.name == name).first()

    if habit:
        sess.query(HabitLog).filter(HabitLog.habit_id == habit.id).delete()
        sess.delete(habit)
        sess.commit()


@click.command(name="delete", help="Delete a habit.")
@click.argument("name", nargs=1, type=str, required=True)
@with_sqlalchemy_error_handling
def delete_habit_cmd(name: str):
    local_session = create_local_session()
    with local_session.begin() as sess:
        delete_habit(sess, name)
