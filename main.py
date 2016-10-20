#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.

Usage:
    pomodoro start <task-title>
    pomodoros time <duration-in-minutes>
    pomodoro list <date>
    pomodoro list_all
    pomodoro clear
    pomodoro (-i | --interactive)
    pomodoro (-h | --help | --version)
    pomodoro quit 

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""
from pomodoro_timer import *
from termcolor import cprint
import sys
import os
import cmd
from docopt import docopt, DocoptExit
import datetime
import sqlite3
import time
from pyfiglet import Figlet,figlet_format

#creates database and cursor
conn = sqlite3.connect('pomodoro.db')
c = conn.cursor()


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive (cmd.Cmd):
    f = Figlet(font = 'block')
    print(cprint(figlet_format("My Pomo Timer", font = 'block'),'green','on_grey'))
    intro = 'Welcome to pomodoro timer!' \
        + ' (type help for a list of commands.)'+ """
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.

Usage:
    pomodoro start <task-title>
    pomodoro time <duration-in-minutes>
    pomodoro list <date>
    pomodoro list_all
    pomodoro (-i | --interactive)
    pomodoro (-h | --help | --version)

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --baud=<n>  Baudrate [default: 9600]
"""
    prompt = 'pomodoro '
    file = None

    def do_quit(self, arg):
        """Usage: quit"""

        print('Good Bye!')
        exit()

    
    @docopt_cmd
    def do_start(self, arg):
        """Usage: start <task-title>"""
        new_task(arg['<task-title>'])

    @docopt_cmd
    def do_list(self, arg):
        """Usage: list <date>"""
        list_tasks(arg['<date>'])

    @docopt_cmd
    def do_list_all(self, arg):
        """Usage: list_all"""
        list_all_tasks()

    @docopt_cmd
    def do_delete_all(self, arg):
        """Usage: delete_all"""
        delete_all()

    @docopt_cmd
    def do_set_short_break(self, arg):
        """Usage: config short_break <duration-in-minutes>"""
        set_short_rest_time(arg['<duration-in-minutes>'])


    @docopt_cmd
    def do_stop_counter(self,arg):
        """Usage: stop"""
        stop_task()







opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)
