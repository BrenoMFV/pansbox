#! /home/bverissimo/projetos/_python-studies/panbox/venv/bin/python3
import os
import re
import sys
import time

import click
from sqlalchemy import and_

# from auth import login, logout
from auth import Auth
from vault import Vault
from models import User, Session, session_factory
from console_interaction import ConsoleInteraction


def main():
    session_manager = Auth()
    ci = ConsoleInteraction()
    vault = Vault()
    try:
        # cleaning possible opened sessions to prevent  persistent authentication
        session_manager.clear_session()

        # authentication cycle
        while True:
            if not session_manager.is_authenticated():
                selected = ci.greetings()
                if re.match(selected, r'q(uit)?', re.IGNORECASE):
                    session_manager.leave()
                elif selected == '1':
                    vault.key = session_manager.login()
                elif selected == '2':
                    session_manager.create_user()
    except KeyboardInterrupt:
        session_manager.leave()


if __name__ == '__main__':
    main()
