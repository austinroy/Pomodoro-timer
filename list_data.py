import sqlite3

#creates database and cursor
conn = sqlite3.connect('pomodoro.db')
c = conn.cursor()


def list_all_tasks():
	# entered_date = input("Enter date to view (Formart is Y-m-d):")
	c.execute("""SELECT * FROM Tasks""",)
	data = c.fetchall()
	print("""
	==================================================================================
	Task name 	| Task Date 	| Cycles taken 	| Working Interval(minutes) 
	=================================================================================="""
	)
	for row in data:
		print("""	"""+str(row[0])+"		| "+str(row[1])+"	| "+str(row[2])+"		| "+str(row[3]))


def list_tasks():
	entered_date = input("Enter date to view (Formart is Y-m-d):")
	c.execute("""SELECT * FROM Tasks WHERE taskdate = ?;""", (entered_date,))
	data = c.fetchall()
	print("""
	==================================================================================
	Task name 	| Task Date 	| Cycles taken 	| Working Interval(minutes) 
	=================================================================================="""
	)
	for row in data:
		print("""	"""+str(row[0])+"		| "+str(row[1])+"	| "+str(row[2])+"		| "+str(row[3]))		

if __name__ == '__main__':
	list_tasks()