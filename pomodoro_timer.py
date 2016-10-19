import time
import sys
import datetime
import sqlite3

#creates database and cursor
conn = sqlite3.connect('pomodoro.db')
c = conn.cursor()
#links to alarm sound file
sound = ""

#set working intervals
def set_task_time():
	pomodoro_time = input("Enter task time :")
	return pomodoro_time

#set short rest intervals
def set_short_rest_time():
	short_rest_time = input("Enter short rest time :")
	return short_rest_time

#set long rest intervals
def set_long_rest_time():
	long_rest_time = input("Enter long rest time :")
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
		time.sleep(1)
	sys.stdout.write("Take a break \n")

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
	sys.stdout.write("Back to work \n")

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
	sys.stdout.write("Back to work \n")

#set alarm on or off
def sound_config ():
	sound = True
	print("""Choose a sound setting
		[0] - Off
		[1] - On

		""")
	choice = input("Enter sound setting :")
	if choice == 0:
		sound = False
	if choice == 1:
		sound = True
	return sound

#starts a new task
def new_task():
	c.execute("CREATE TABLE IF NOT EXISTS Tasks(taskname TEXT, taskdate TEXT, cycles REAL)")

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
	date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y - %m - %d'))

	task = {}
	task_date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y - %m - %d'))
	task_name = input ("Enter task name :")
	task_cycles = 0
	stop = False

	while stop == False:
		count = 3
		while count >0:
			task_cycles += 1
			run_task(pomodoro_time)
			short_rest(short_rest_time)
			count -= 1
			stop = True
		run_task(pomodoro_time)
		long_rest(long_rest_time)
		task_cycles +=1

	c.execute("INSERT INTO Tasks (taskname , taskdate, cycles ) VALUES (?,?,?)",
		(task_name,task_date,task_cycles))
	conn.commit()


#returns a list of tasks on a certain day
def list_tasks():
	entered_date = input("Enter date to view (Formart is Y - m - d):")
	c.execute("""SELECT * FROM Tasks WHERE taskdate = ?;""", (entered_date,))
	data = c.fetchall()
	# print(data)
	for row in data:
		print(row)

	input("Press enter to return to home")
	main()

#stops an ongoing tasks
def stop_task():
	stop = True

#main program which provides the menu the user first interacts with and choses next action
def main():
    print("""
    Pomodoro Task Timer
		
    Choose an action to continue:
    
    start task - Start a new task
    list tasks - List tasks done today
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
	main().run(debug = True)