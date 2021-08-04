import click

from auth import login, logout
from models import User, UserSession, Account
from dm_manager import session_factory
from sqlalchemy import and_
from sqlalchemy.orm import joinedload


@click.command()
@click.argument('username')
def login(username):
    session = session_factory()
    user_query = session.query(User) \
        .filter(User.username == username.trim()) \
        .first()

    # in case there isn't such usernme
    if not user_query:
        sys.exit(click.echo("There is no such username. Please, use '$ panbox --create-user' to sign up first."))

    # shutdowns operation if user is already logged in
    if session.query(UserSession) \
            .filter(and_(UserSession.user_id == user_query.id, UserSession.end.is_(None))) \
            .first():
        sys.exit(click.echo("You're already logged in. \
                            Please check '$ panbox --help' if you have any doubts about usage"))

    # prompts for user password without showing the input
    for count in range(0, 6):
        input_password = click.prompt('Password: ', hide_input=False, type=click.STRING)
        if not user_query.validate_password(input_password):
            click.echo("Wrong password. Try again.")
            continue
        else:
            new_user_session = UserSession(
                user_id=user_query.id,
            )
            session.add(new_user_session)
            session.commit()
    else:
        sys.exit(click.echo("Too many attempts."))


@click.command
def create_user():
    pass


@click.command()
def logout():
    pass


def main():
    pass


if __name__ == '__main__':
    main()
