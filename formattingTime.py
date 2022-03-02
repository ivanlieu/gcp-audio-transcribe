
"""This function takes timeInSeconds as an integer and greaterThanOneHour as a boolean 
for the input and returns as a string the time format in MMSS if greaterThanOneHour = False
or in HHMMSS if greaterThanOneHour = True."""

def formatTime(timeInSeconds):

	timeInSeconds = int(timeInSeconds)

	if timeInSeconds < 3600:
		minutes = timeInSeconds // 60
		timeInSeconds %= 60
		seconds = timeInSeconds

		if minutes < 10:
			minutes = "0" + str(minutes) + "m"
		else:
			minutes = str(minutes) + "m"
		
		if seconds < 10:
			seconds = "0" + str(seconds) + "s"
		else:
			seconds = str(seconds) + "s"


		timeInMMSS = minutes + " " + seconds

		return timeInMMSS
	else:
		hours = timeInSeconds // 3600
		timeInSeconds %= 3600
		minutes = timeInSeconds // 60
		timeInSeconds %= 60
		seconds = timeInSeconds

		if hours < 10:
			hours = "0" + str(hours) + "h"	
		else:
			hours = str(hours) + "h"

		if minutes < 10:
			minutes = "0" + str(minutes) + "m"
		else:
			minutes = str(minutes) + "m"

		if seconds < 10:
			seconds = "0" + str(seconds) + "s"
		else:
			seconds = str(seconds) + "s"

		timeInHHMMSS = hours + " " + minutes + " " + seconds

		return timeInHHMMSS
