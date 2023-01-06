import click
import sqlalchemy.exc

from ritmo.session import session


def command_with_local_session(command):
    """
    A decorator that creates a local session and passes it to the command.
    """

    def wrapper(*args, **kwargs):
        Session = session.create_local_session()
        with Session.begin() as sess:
            command(sess, *args, **kwargs)

    return wrapper


def command_with_sqlalchemy_error_handling(command):
    """
    A decorator that handles SQLAlchemy errors and prints them to the console.
    """

    def wrapper(*args, **kwargs):
        try:
            command(*args, **kwargs)
        except sqlalchemy.exc.SQLAlchemyError as e:
            click.echo(f"SQLAlchemy error: {e}")

    return wrapper
