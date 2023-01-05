import datetime

import click

from ritmo.models import models
from ritmo.session import session


@click.command(name="done", help="Mark a habit as done.")
@click.argument("name", nargs=1, type=str)
def mark_done(name: str):
    """
    Mark a habit as done.
    If the habit is of type 'numerical', the number of completed days will be incremented.

    Args:
        name: The name of the habit to mark as done. If the habit does not exist, it will not be created.
    """

    Session = session.create_local_session()
    with Session.begin() as sess:
        habit = sess.query(models.Habit).filter(models.Habit.name == name).first()

        if habit:
            habit_day = (
                sess.query(models.HabitDay)
                .filter(
                    models.HabitDay.habit_id == habit.id
                    and models.HabitDay.date == datetime.datetime.now()
                )
                .first()
            )

            if habit_day:
                habit_day.completed = True

                if habit.type == "numerical":
                    habit_day.completed_num += 1

                sess.commit()
            else:
                habit_day = models.HabitDay(habit_id=habit.id)

                sess.add(habit_day)
                sess.commit()

        else:
            click.echo(f"Habit '{name}' not found.")
            return


@click.command(name="undo", help="Mark a habit as undone.")
@click.argument("name", nargs=1, type=str)
def mark_undone(name: str):
    """
    Mark a habit as undone.
    If the habit is of type 'numerical', the number of times completed will be decremented. If the number of times completed
    reaches 0, the habit_day will be deleted.

    Args:
        name: The name of the habit to mark as undone.
    """

    Session = session.create_local_session()
    with Session.begin() as sess:
        habit = sess.query(models.Habit).filter(models.Habit.name == name).first()

        if habit:
            habit_day = (
                sess.query(models.HabitDay)
                .filter(
                    models.HabitDay.habit_id == habit.id
                    and models.HabitDay.date == datetime.datetime.now()
                )
                .first()
            )

            if habit_day:
                if habit.type == "boolean":
                    sess.delete(habit_day)

                if habit.type == "numerical":
                    if habit_day.completed_num > 0:
                        habit_day.completed_num -= 1

                    if habit_day.completed_num == 0:
                        sess.delete(habit_day)

                sess.commit()

        else:
            click.echo(f"Habit '{name}' not found.")
            return
