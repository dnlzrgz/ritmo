import click
import sqlalchemy.exc

from ritmo.session import session


def with_database(command):
    """
    Decorator that creates a database session and passes it to the command.

    Args:
        command: The command to decorate.
    """

    def wrapper(*args, **kwargs):
        Session = session.create_local_session()
        with Session.begin() as sess:
            command(sess, *args, **kwargs)

    return wrapper


def with_sqlalchemy_error_handling(command):
    """
    Decorator that catches SQLAlchemy errors and prints them to the console.

    Args:
        command: The command to decorate.
    """

    def wrapper(*args, **kwargs):
        try:
            command(*args, **kwargs)
        except sqlalchemy.exc.SQLAlchemyError as e:
            click.echo(f"Error: {e}")

    return wrapper
