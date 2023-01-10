import datetime

from ritmo.commands.add_habit import add_habit
from ritmo.models import Habit
from ritmo.sessions import create_memory_session


def test_add_habit_with_only_name():
    """
    Test adding a habit with only a name specified.
    """

    mem_session = create_memory_session()
    with mem_session() as sess:
        add_habit(sess, "Test habit", None, None, None, None)

        habit = sess.query(Habit).filter(Habit.name == "Test habit").first()
        assert habit is not None
        assert habit.name == "Test habit"


def test_add_habit_without_valid_name():
    """
    Test adding a habit without a name specified.
    """

    mem_session = create_memory_session()
    with mem_session() as sess:
        add_habit(sess, "", None, None, None, None)

        habit = sess.query(Habit).first()
        assert habit is None

    with mem_session() as sess:
        add_habit(sess, " ", None, None, None, None)

        habit = sess.query(Habit).first()
        assert habit is None


def test_add_habit_with_invalid_dates():
    """
    Test adding a habit with an end date before the start date.
    """

    today_date = datetime.datetime.utcnow()
    yesterday_date = today_date - datetime.timedelta(days=1)

    mem_session = create_memory_session()
    with mem_session() as sess:
        add_habit(sess, "test", None, None, yesterday_date, today_date)
