# -*- coding: UTF-8 -*-

import questionary


def question(message, choices):
    choice = questionary.select(
        message,
        choices=choices
    ).ask()
    return choice
