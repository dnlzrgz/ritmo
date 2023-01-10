import datetime

from ritmo.commands.add_habit import add_habit
from ritmo.commands.done_habit import mark_as_done, mark_as_undone
from ritmo.models import Habit, HabitDay
from ritmo.sessions import create_memory_session


def test_mark_habit_as_done():
    """
    Test marking a habit as done.
    """

    mem_session = create_memory_session()
    with mem_session() as sess:
        add_habit(sess, "Test habit", None, None, None, None)

        habit = sess.query(Habit).filter(Habit.name == "Test habit").first()
        assert habit is not None
        assert habit.name == "Test habit"

        mark_as_done(sess, "Test habit")
        habit_day = sess.query(HabitDay).filter(HabitDay.habit_id == habit.id).first()
        assert habit_day is not None
        assert habit_day.completed is True
        assert habit_day.completed_num == 1


def test_mark_habit_as_undone():
    """
    Test marking a habit as done.
    """

    mem_session = create_memory_session()
    with mem_session() as sess:
        add_habit(sess, "Test habit", None, None, None, None)

        habit = sess.query(Habit).filter(Habit.name == "Test habit").first()
        assert habit is not None
        assert habit.name == "Test habit"

        mark_as_done(sess, "Test habit")
        habit_day = sess.query(HabitDay).filter(HabitDay.habit_id == habit.id).first()
        assert habit_day is not None
        assert habit_day.completed is True
        assert habit_day.completed_num == 1

        mark_as_undone(sess, "Test habit")
        habit_day = sess.query(HabitDay).filter(HabitDay.habit_id == habit.id).first()
        assert habit_day is None


def test_mark_numerical_habit_done_multiples_times():
    """
    Test marking a numerical habit as done multiple times.
    """
    mem_session = create_memory_session()
    with mem_session() as sess:
        add_habit(sess, "Test habit", None, "numerical", None, None)

        habit = sess.query(Habit).filter(Habit.name == "Test habit").first()
        assert habit is not None
        assert habit.name == "Test habit"

        times_done = 3
        for i in range(times_done):
            mark_as_done(sess, "Test habit")

        habit_day = sess.query(HabitDay).filter(HabitDay.habit_id == habit.id).first()
        assert habit_day is not None
        assert habit_day.completed is True
        assert habit_day.completed_num == times_done
