import sqlite3

#creates database and cursor
conn = sqlite3.connect('pomodoro.db')
c = conn.cursor()

def set_task_time():
	pomodoro_time = input("Enter task time :")
	return pomodoro_time

#set short rest intervals
def set_short_rest_time(short_rest_time):
	short_rest_time = input("Enter short rest time :")
	return short_rest_time

#set long rest intervals
def set_long_rest_time():
	long_rest_time = input("Enter long rest time :")
	return long_rest_time