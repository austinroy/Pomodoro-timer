import time
import sys
import datetime
import sqlite3
from pyfiglet import Figlet
import os


#creates database and cursor
conn = sqlite3.connect('pomodoro.db')
c = conn.cursor()

#links to alarm sound file
alarm = 'aplayAlarm-tone.wav'

#set working intervals
def set_task_time():
	pomodoro_time = input("Enter task interval time :")
	return pomodoro_time

#set short rest intervals
def set_short_rest_time():
	short_rest_time = input("Enter short break time :")
	return short_rest_time

#set long rest intervals
def set_long_rest_time():
	long_rest_time = input("Enter long break time :")
	return long_rest_time

#counts down working time
def run_task (pomodoro_time):
	minute = 60
	sound_config = 'on'
	for remainingtime in range (pomodoro_time*minute,0,-1):
		sys.stdout.write("\r")
		minute -=1
		if minute <= 0:
			pomodoro_time -=1
			minute =60
		elif minute <=9:
			sys.stdout.write("[{:2} :0{:1d}] remaining ".format(pomodoro_time-1, minute))
		else:
			sys.stdout.write("[{:2} :{:1d}] remaining ".format(pomodoro_time-1, minute))
		sys.stdout.flush()
		time.sleep(1)
	sys.stdout.write("Take a break 	\n")
	# if sound_config == 'on':
	# 	playASound(alarm)


#counts down short rest time
def short_rest (short_rest_time):
	minute = 60

	for remainingtime in range (short_rest_time*minute,0,-1):
		sys.stdout.write("\r")
		minute -=1
		if minute <= 0:
			short_rest_time -=1
			minute =60
		elif minute <=9:
			sys.stdout.write("[{:2} :0{:1d}] remaining ".format(short_rest_time-1, minute))
		else:
			sys.stdout.write("[{:2} :{:1d}] remaining ".format(short_rest_time-1, minute))
		sys.stdout.flush()
		time.sleep(1)
	sys.stdout.write("Back to work 	\n")

#count down long rest time
def long_rest (long_rest_time):
	minute = 60

	for remainingtime in range (long_rest_time*minute,0,-1):
		sys.stdout.write("\r")
		minute -=1
		if minute <= 0:
			long_rest_time -=1
			minute =60
		elif minute <=9:
			sys.stdout.write("[{:2} :0{:1d}] remaining ".format(long_rest_time-1, minute))
		else:
			sys.stdout.write("[{:2} :{:1d}] remaining ".format(long_rest_time-1, minute))
		sys.stdout.flush()
		time.sleep(1)
	sys.stdout.write("Back to work 	\n")

#set alarm on or off
def sound_config ():
	sound = True
	print("""Choose a sound setting
		Off
		On

		""")
	choice = input("Enter sound setting :")
	if choice == 'off':
		sound = False
	if choice == 'on':
		sound = True
	return sound

#starts a new task
def new_task(task_name):
	c.execute("CREATE TABLE IF NOT EXISTS Tasks(taskname TEXT, taskdate TEXT, intervals INT, cycles REAL )")

	choice = input ("Choose settings to use. For default press 1 or to make your own press any button :")

	if choice == '1':
		pomodoro_time = 25
		short_rest_time = 5
		long_rest_time = 15
		sound = True
	else:
		pomodoro_time = int(set_task_time())
		short_rest_time = int(set_short_rest_time())
		long_rest_time = int(set_long_rest_time())
		sound = int(sound_config())

	unix = time.time()
	date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m -%d'))

	task = {}
	task_date = str(datetime.datetime.fromtimestamp(unix).strftime('%d:%m:%Y'))
	task_name = task_name
	task_length = int(input("Enter expected total task duration in minutes:"))
	if task_length < pomodoro_time:
		task_cycles = 1		
	else:
		task_cycles = task_length//pomodoro_time
		

	x = 0

	while task_cycles > x:
		count = 3
		while count >0 and task_cycles > x:
			x += 1
			run_task(pomodoro_time)
			short_rest(short_rest_time)
			count -= 1
		run_task(pomodoro_time)
		long_rest(long_rest_time)
		x +=1

	print("Time is up!!!")
	rating = input("Rate your timing from 1 to 5")

	c.execute("INSERT INTO Tasks (taskname , taskdate, cycles , intervals ) VALUES (?,?,?,?)",
		(task_name,task_date,task_cycles,pomodoro_time))
	conn.commit()


#returns a list of tasks on a certain day
def list_tasks(entered_date):
	#entered_date = input("Enter date to view (Formart is Y-m-d):")
	c.execute("""SELECT * FROM Tasks WHERE taskdate = ?;""", (entered_date,))
	data = c.fetchall()
	print("""
	==================================================================================
	Task name 	| Task Date 	| Cycles taken 	| Working Interval(minutes) 
	=================================================================================="""
	)
	for row in data:
		print("""	"""+str(row[0])+"		| "+str(row[1])+"	| "+str(row[2])+"		| "+str(row[3]))

#lists all tasks ever done		
def list_all_tasks():
	print("List of all tasks")
	c.execute("""SELECT * FROM Tasks""",)
	data = c.fetchall()
	print("""
	==================================================================================
	Task name 	| Task Date 	| Cycles taken 	| Working Interval(minutes) 
	=================================================================================="""
	)
	for row in data:
		print("""	"""+str(row[0])+"		| "+str(row[1])+"	| "+str(row[2])+"		| "+str(row[3]))


#stops an ongoing tasks
def stop_task():
	stop = True

#main program which provides the menu the user first interacts with and choses next action
def main():
    f = Figlet(font = 'roman')
    print (f.renderText("Pomo Timer"))

    print("""
    Pomodoro Task Timer
		
    Choose an action to continue:

    pomodoro start - Start a new task
    pomodoro list - List tasks done today
    close - Exit

    """)

    action = input("What would you want to do today? ")

    if action == 'pomodoro start':
        new_task()
    elif action == 'pomodoro list':
        list_tasks()
    elif action == 'close':
    	print ("Closing Application ...")
    	c.close()
    	conn.close()
    	exit()
    else:
        print('No valid choice was given, try again')
        main()

if __name__ == '__main__':
	main()