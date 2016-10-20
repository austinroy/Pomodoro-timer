import time
import sys
import datetime
import sqlite3
from pyfiglet import Figlet
import os
# import winsound

Freq = 2500 # Set beep Frequency To 2500 Hertz
Dur = 1000 # Set beep Duration To 1000 ms == 1 second

#creates database and cursor
conn = sqlite3.connect('pomodoro.db')
c = conn.cursor()
stop = False
#links to alarm sound file
# alarm = 'aplayAlarm-tone.wav'

def stop():
	stop = True
#set working intervals
def set_task_time():
	pomodoro_time = int(input("Enter task interval time :"))
	if type(pomodoro_time) != int:
		print("please enter an integer")
		set_task_time()
	else:
		return pomodoro_time

#set short rest intervals
def set_short_rest_time():
	short_rest_time = int(input("Enter short break time :"))
	if type(short_rest_time) != int:
		print("please enter an integer")
		set_short_rest_time()
	else:
		return short_rest_time

#set long rest intervals
def set_long_rest_time():
	long_rest_time = int(input("Enter long break time :"))
	if type(long_rest_time) != int:
		print("please enter an integer")
		set_long_rest_time()
	else:
		return long_rest_time

#counts down working time
def run_task (pomodoro_time):
	minute = 60
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
		try:
			time.sleep(1)
			break_status = 'not broken'
		except KeyboardInterrupt:
			return 'stopped'
	print("Take a break")
	# if sound == True:
	# 	winsound.Beep(Freq,Dur)


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
	# if sound == True:
	# 	winsound.Beep(Freq,Dur)

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
	# if sound == True:
	# 	winsound.Beep(Freq,Dur)

#set alarm on or off
def sound_config ():
	sound = True
	print("""Choose a sound setting(case sensitive)
		off
		on

		""")
	choice = input("Enter sound setting :")
	if choice == 'off':
		sound = False
		return sound
	if choice == 'on':
		sound = True
		return sound
	else:
		print("Invalid choice please use on/off")
		sound_config()
	return sound

#starts a new task
def new_task(task_name):
	c.execute("CREATE TABLE IF NOT EXISTS Tasks(taskname TEXT, taskdate TEXT, intervals INT, cycles REAL,rating INT )")

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
		sound = sound_config()

	unix = time.time()
	task = {}
	task_date = str(datetime.datetime.fromtimestamp(unix).strftime('%d:%m:%Y'))
	task_name = task_name
	task_length = int(input("Enter expected total task duration in minutes:"))
	if task_length < pomodoro_time:
		task_cycles = 1		
	else:
		task_cycles = task_length//pomodoro_time
		
	print("Counter started, press ctrl + c to stop")
	x = 0

	break_status=''
	while task_cycles > x:
		count = 3
		while count >0 and task_cycles > x:
			x += 1
			status = run_task(pomodoro_time)
			if status == 'stopped':
				break_status = 'stopped'
				break
			else:
				pass
			short_rest(short_rest_time)
			count -= 1
		if break_status == 'stopped':
			break
		else:
			pass
		run_task(pomodoro_time)
		long_rest(long_rest_time)
		x +=1

	print("Time is up!!!")
	rating = input("On a scale of 1 to 5 how would you rate your experience using this timer?")

	c.execute("INSERT INTO Tasks (taskname , taskdate, cycles , intervals , rating) VALUES (?,?,?,?,?)",
		(task_name,task_date,task_cycles,pomodoro_time,rating))
	conn.commit()

def delete_all():
	confirm = input("Are you sure you want to delete all tasks? Action cannot be reversed y/n ")
	if confirm == 'y':
		c.execute("""DELETE from Tasks""")
		conn.commit()
		print("Files deleted...")
	elif confirm == 'n':
		print("Deletion cancelled")
	else:
		print("Invalid choice press y for yes or n for no")


#returns a list of tasks on a certain day
def list_tasks(entered_date):
	#entered_date = input("Enter date to view (Formart is Y:m:d):")
	c.execute("""SELECT * FROM Tasks WHERE taskdate = ?;""", (entered_date,))
	data = c.fetchall()
	print("""
	===========================================================================================
	Task name 	| Task Date 	| Cycles taken 	| Working Interval(minutes) 	| Rating
	==========================================================================================="""
	)
	for row in data:
		print("""	"""+str(row[0])+"		| "+str(row[1])+"	| "+str(row[2])+"		| "+str(row[3])+"				| "+str(row[4]))

#lists all tasks ever done		
def list_all_tasks():
	print("List of all tasks")
	c.execute("""SELECT * FROM Tasks""",)
	data = c.fetchall()
	print("""
	=============================================================================================
	Task name 	| Task Date 	| Cycles taken 	| Working Interval(minutes) 	| Rating
	============================================================================================="""
	)
	for row in data:
		print("""	"""+str(row[0])+"		| "+str(row[1])+"	| "+str(row[2])+"		| "+str(row[3])+"				| "+str(row[4]))


#stops an ongoing tasks
def stop_task():
	stop = True

#main program which provides the menu the user first interacts with and choses next action
# def main():
#     f = Figlet(font = 'roman')
#     print (f.renderText("Pomo Timer"))

#     print("""
#     Pomodoro Task Timer
		
#     Choose an action to continue:

#     pomodoro start - Start a new task
#     pomodoro list - List tasks done today
#     close - Exit

#     """)

#     action = input("What would you want to do today? ")

#     if action == 'pomodoro start':
#         new_task()
#     elif action == 'pomodoro list':
#         list_tasks()
#     elif action == 'close':
#     	print ("Closing Application ...")
#     	c.close()
#     	conn.close()
#     	exit()
#     else:
#         print('No valid choice was given, try again')
#         main()

# if __name__ == '__main__':
# 	main()