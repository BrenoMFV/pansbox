from datetime import datetime
import time
import os
import sys
import re

from pbkdf2 import PBKDF2

from rich import print
from rich.panel import Panel
from rich.text import Text

from sqlalchemy import and_

from console_interaction import ConsoleInteraction
from models import User, Session, BlockedUsername, session_factory



class Auth(ConsoleInteraction):

    def __init__(self, user=None):
        super().__init__()
        self.conn = session_factory()

    def generate_vault_key(self, user, password):
        return

    def login(self):
        for count in range(5, 0, -1):
            username = self.prompt.ask('Enter [bold]Username[/bold]')
            password = self.prompt.ask('Enter [bold]Password[/bold]', password=True)

            if blocked := self.conn.query(BlockedUsername).filter(
                    and_(BlockedUsername.username == username, BlockedUsername.end_block > datetime.now())).first():
                print(
                    f'This username has been [red]blocked[/red] for too many attempts until [bold]{blocked.end.strftime("%H:%M:%S")}[/bold].')
                sys.exit()

            valid_account = self.conn.query(User).filter(
                User.username == username
            ).first()

            if valid_account and valid_account.validate_password(password):
                self.register_session(valid_account)
                print(f"You're logged in as [bold green]{valid_account.username}[/bold green]")
                return self.generate_vault_key(password)

            time.sleep(2)
            print(
                f'Wrong username or password. You have [bold red]{count}[/bold red] attempts left.\n Please Try again.')
        if self.conn.query(User).filter(User.username == username).first():
            self.conn.add(BlockedUsername(username=username))
            self.conn.commit()
        print('Too many attempts. This user account is blocked for [bold]5 minutes[/bold]. Try Again latter.')

    # ends session if the program hasn't closed the last one and start a new one
    def clear_session(self):
        if open_session := self.conn.query(Session).filter(Session.end.is_(None)).first():
            open_session.end = datetime.now()
            self.conn.commit()
            print(open_session.end)

    # register a new session if user hasn't closed the program properly
    # after the user has logged in
    def register_session(self, user_obj):
        new_session = Session(user=user_obj)
        self.conn.add(new_session)
        self.conn.commit()

    def leave(self):
        self.clear_session()
        print('[bold red]Exiting...')
        sys.exit()

    def create_user(self):
        while True:
            username = self.prompt.ask("Choose your username [bold cyan](only letters, numbers, '_'s or '.'s)")
            if self.conn.query(User).filter(User.username == username).count() == 1:
                print('Username already exists. Try another one.')
                continue
            if not re.match(r'[A-Za-z0-9_.]+', username):
                print('Username invalid. Try again please.')
                continue
            break

        while True:
            password = self.prompt.ask("Insert your password [cyan](at least 8 digits)",
                                       password=True)
            if len(password) < 8:
                print("Password too short!")
                continue
            confirm = self.prompt.ask("Confirm your password", password=True)
            if password != confirm:
                print('[prompt.invalid]1These passwords do not match!')
                continue
            break

        new_user = User(
            username=username,
            password=password,
        )

        try:
            self.conn.add(new_user)
            self.conn.commit()
        except Exception as e:
            print("[bold black on red] Error ")
            self.console.print_exception()
            with open('log.txt', mode='a') as log:
                tb = sys.exc_info()[2]
                log.write(with_traceback(tb))
            sys.exit()
        print('[green]Your account has been successfully created!')
        return

    def is_authenticated(self):
        return True if self.conn.query(Session).filter(Session.end.is_(None)).first() else False
