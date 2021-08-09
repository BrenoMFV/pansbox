#! /home/bverissimo/projetos/_python-studies/panbox/venv/bin/python3
import os
import re
import sys
import time

import click
from sqlalchemy import and_

from db_manager import session_factory
# from auth import login, logout
from models import User, UserSession


@click.group()
def panbox():
    pass


@panbox.command()
@click.argument('username')
def login():
    session = session_factory()

    username = click.prompt('Username')
    user_query = session.query(User) \
        .filter(User.username == username) \
        .first()

    # in case there isn't such username
    if not user_query:
        sys.exit(click.echo("There is no such username. Please, use '$ panbox --create-user' to sign up first."))

    # shutdowns operation if user is already logged in
    if session.query(UserSession) \
            .filter(and_(UserSession.user_id == user_query.id, UserSession.end.is_(None), UserSession.terminal_pid == str(os.getpid()))) \
            .first():
        sys.exit(click.echo("You're already logged in. Please check '$ panbox --help' if you have any doubts about usage"))

    # prompts for user password without showing the input
    for count in range(0, 6):
        input_password = click.prompt('Password', hide_input=True, type=click.STRING)
        if not user_query.validate_password(password=input_password):
            click.echo("Wrong password. Try again.")
            time.sleep(2)
            continue
        else:
            new_user_session = UserSession(user_id=user_query.id)
            session.add(new_user_session)
            session.commit()
            return click.echo(f'Logged in as {new_user_session.user.username}')
    return click.echo("Too many attempts.")


def check_valid_email(email):
    """TODO"""
    return True


@panbox.command()
def create_user():
    session = session_factory()
    while True:
        username = click.prompt("Choose your username (only letters, numbers, '_'s or '.'s)")
        if session.query(User).filter(User.username == username).count() >= 1:
            click.echo('Username already exists.')
            continue
        if not re.match(r'[A-Za-z0-9_.]+', username):
            click.echo('Username invalid. Try again please.')
            continue
        break

    while True:
        password = click.prompt("Insert your password (at least 8 digits)", hide_input=True)
        if len(password) < 8:
            continue
        confirm = click.prompt("Confirm your password", hide_input=True)
        if password != confirm:
            click.echo('The passwords do not match.')
            continue
        break

    while True:
        email = click.prompt("Email")
        if not check_valid_email(email):
            continue
        break
    new_user = User(
        username=username,
        password=password,
        email=email
    )
    try:
        session.add(new_user)
        session.commit()
    except Exception:
        click.prompt("Error.")
        with open('log.txt', mode='a') as log:
            tb = sys.exc_info()[2]
            log.write(with_traceback(tb))
        sys.exit()
    click.echo('Your account has been successfully created!')


@panbox.command()
def whoami():
    session = session_factory()
    if current_session := session.query(UserSession) \
            .filter(and_(UserSession.end.is_(None))).first():
        return click.echo(f"You're logged as {current_session.user.username}.")
    return click.echo("You're not logged in.")


@panbox.command()
def logout():
    session = session_factory()
    if user_session := session.query(UserSession) \
            .filter(and_(UserSession.terminal_pid == str(os.getpid()),
                         UserSession.end.is_(None))) \
            .first():
        user_session.end = datetime.datetime.now()
        session.add(user_session)
        session.commit()
        return click.echo('Logged out')
    return click.echo("You're not logged in.")


if __name__ == '__main__':
    panbox()
