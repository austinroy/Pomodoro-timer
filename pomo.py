import time
import sys

minute = 60
pomodoro = 1

for remainingtime in range (pomodoro*minute,0,-1):
	sys.stdout.write("\r")
	minute -=1
	if minute <= 0:
		pomodoro -=1
		minute =60
	elif minute <=9:
		sys.stdout.write("[{:2} :0{:1d}] remaining ".format(pomodoro-1, minute))
	else:
		sys.stdout.write("[{:2} :{:1d}] remaining ".format(pomodoro-1, minute))
	sys.stdout.flush()
	time.sleep(1)
sys.stdout.write("Take a break \n")