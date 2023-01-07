import click
import sqlalchemy.exc


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
