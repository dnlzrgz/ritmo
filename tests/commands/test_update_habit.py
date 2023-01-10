import datetime

from ritmo.commands.add_habit import add_habit
from ritmo.commands.update_habit import update_habit
from ritmo.models import Habit
from ritmo.sessions import create_memory_session


def test_update_habit_name():
    """
    Test updating a habit's name.
    """

    mem_session = create_memory_session()
    with mem_session() as sess:
        add_habit(sess, "Tesxt habit", None, None, None, None)

        habit = sess.query(Habit).filter(Habit.name == "Tesxt habit").first()
        assert habit is not None
        assert habit.name == "Tesxt habit"

        update_habit(sess, "Tesxt habit", "Test habit", None, None, None, None)

        habit = sess.query(Habit).filter(Habit.name == "Test habit").first()
        assert habit is not None
        assert habit.name == "Test habit"


def test_update_habit_start_date():
    """
    Test updating a habit's start date.
    """

    yesterday_date = datetime.datetime.utcnow() - datetime.timedelta(days=1)

    mem_session = create_memory_session()
    with mem_session() as sess:
        add_habit(sess, "Test habit", None, None, None, None)

        habit = sess.query(Habit).filter(Habit.name == "Test habit").first()
        assert habit is not None
        assert habit.name == "Test habit"
        assert habit.start_date is not None

        update_habit(sess, "Test habit", None, None, None, yesterday_date, None)

        habit = sess.query(Habit).filter(Habit.name == "Test habit").first()
        assert habit is not None
        assert habit.start_date.strftime("%Y-%m-%d") == yesterday_date.strftime(
            "%Y-%m-%d"
        )
