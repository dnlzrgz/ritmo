import datetime

from ritmo.commands.add_habit import add_habit
from ritmo.commands.delete_habit import delete_habit
from ritmo.commands.done_habit import mark_as_done
from ritmo.models import Habit, HabitDay
from ritmo.sessions import create_memory_session


def test_delete_habit_without_logs():
    """
    Test deleting a habit without logs.
    """

    mem_session = create_memory_session()
    with mem_session() as sess:
        add_habit(sess, "Test habit", None, None, None, None)

        habit = sess.query(Habit).filter(Habit.name == "Test habit").first()
        assert habit is not None
        assert habit.name == "Test habit"

        delete_habit(sess, "Test habit")

        habit = sess.query(Habit).filter(Habit.name == "Test habit").first()
        assert habit is None


def test_delete_habit_with_logs():
    """
    Test deleting a habit with logs.
    """

    mem_session = create_memory_session()
    with mem_session() as sess:
        add_habit(sess, "Test habit", None, None, None, None)

        habit = sess.query(Habit).filter(Habit.name == "Test habit").first()
        habit_id = habit.id

        assert habit is not None
        assert habit.name == "Test habit"

        mark_as_done(sess, "Test habit")
        habit_day = (
            sess.query(HabitDay)
            .filter(
                HabitDay.habit_id == habit.id
                and HabitDay.date == datetime.datetime.now()
            )
            .first()
        )
        assert habit_day is not None
        assert habit_day.completed is True

        delete_habit(sess, "Test habit")

        habit = sess.query(Habit).filter(Habit.name == "Test habit").first()
        assert habit is None

        habit_day = sess.query(HabitDay).filter(HabitDay.habit_id == habit_id).first()
        assert habit_day is None
