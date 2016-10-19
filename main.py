#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.

Usage:
    pomodoro_timer start <task-title>
    pomodoro_timer config time <duration-in-minutes>
    pomodoro_timer config short_break <duration-in-minutes>
    pomodoro_timer config long_break <duration-in-minutes>
    pomodoro_timer config sound <off/on>
    pomodoro_timer list <date>
    pomodoro_timer (-i | --interactive)
    pomodoro_timer (-h | --help | --version)

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --baud=<n>  Baudrate [default: 9600]
"""
from pomodoro_timer import *
import sys
import cmd
from docopt import docopt, DocoptExit
import datetime
import sqlite3
import time
from pyfiglet import Figlet

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
    intro = 'Welcome to my interactive program!' \
        + ' (type help for a list of commands.)'
    prompt = 'pomodoro_timer '
    file = None
    # f = Figlet(font = 'roman')
    # print (f.renderText('pomodoro timer'))

#     @docopt_cmd
#     def do_tcp(self, arg):
#         """Usage: tcp <host> <port> [--timeout=<seconds>]"""

#         print(arg)

#     @docopt_cmd
#     def do_serial(self, arg):
#         """Usage: serial <port> [--baud=<n>] [--timeout=<seconds>]

# Options:
#     --baud=<n>  Baudrate [default: 9600]
#         """

#         print(arg)

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
        """Usage: pomodoro list <date>"""
        list_tasks(arg['<date>'])

    @docopt_cmd
    def do_set_short_break(self, arg):
        """Usage: pomodoro config short_break <duration-in-minutes>"""
        set_short_rest_time(arg['<duration-in-minutes>'])

    @docopt_cmd
    def do_set_long_break(self, arg):
        """Usage: pomodoro long_break <duration-in-minutes>"""
        set_long_rest_time(arg['<duration-in-minutes>'])


    @docopt_cmd
    def do_set_time(self, arg):
        """Usage: pomodoro config_time <duration-in-minutes>"""
        set_task_time(arg['<duration-in-minutes>'])

    @docopt_cmd
    def do_set_time(self, arg):
        """Usage: pomodoro config_sound <duration-in-minutes>"""
        set_task_time(arg['<duration-in-minutes>'])

    @docopt_cmd
    def do_stop_counter(self,arg):
        """Usage: pomodoro stop"""
        stop_task()







opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)
