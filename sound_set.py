def sound_config ():
	sound = True
	print("""Choose a sound setting(case sensitive)
		off
		on

		""")
	choice = input("Enter sound setting :")
	if choice == 'off':
		sound = False
	if choice == 'on':
		sound = True
	else:
		print("Invalid choice please use on/off")
	return sound

if __name__ = '__main__':
	sound_config()