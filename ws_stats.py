#/usr/bin/python3
"""
TODO :
- Choose timescale (week, month, year)
- Prettify the x-axis
- Automatically detect usernames (should be easy)
- Maybe change variable names
"""

import re
import sys
from matplotlib import pyplot as plt

try:
	fichier = sys.argv[1]
except:
	print("Please give the chat history file location in parameter.")
	exit()


you = 0
friend = 0
totalMessages = 0

yourName = input("Your name on WhatsApp : ")
friendName = input("Your friend's name on WhatsApp : ")

days = []
ddays= []
hours = [i for i in range(24)]
dhours = { key : {
	'msgYH' : 0,
	'msgFH' : 0,
	'msgTH' : 0
} for key in range(24)}

with open(fichier, 'r') as file:
	data = file.readlines()
	for line in data:
		day = re.search(r"\d\d\/\d\d\/\d\d\d\d",line)
		hour = re.search(r"\d\d",line[12:14])
		if day:
			if line[0:10] not in days:
				days.append(line[0:10])
				tempDict = {"day" : line[0:10], "msgYD" : 0, "msgFD" : 0, 'msgTD' : 0}
				ddays.append(tempDict.copy())
			else:
				for day in ddays:
					if day["day"] == line[0:10]:
						if line[20] == yourName[0]:
							day['msgYD'] += 1
							day['msgTD'] += 1
						if line[20] == friendName[0]:
							day['msgFD'] += 1
							day['msgTD'] += 1
		if hour:
			if line[20] == yourName[0]:
				dhours[int(line[12:14])]['msgYH'] +=1
				you += 1
			if line[20] == friendName[0]:
				dhours[int(line[12:14])]['msgFH'] +=1
				friend += 1
			dhours[int(line[12:14])]['msgTH'] +=1
		totalMessages += 1

msgYD = [day['msgYD'] for day in ddays]
msgFD = [day['msgFD'] for day in ddays]
msgTD = [day['msgTD'] for day in ddays]

msgYH = []
msgFH = []
msgTH = []

for i in range(24):
	msgYH.append(dhours[i].get('msgYH'))
	msgFH.append(dhours[i].get('msgFH'))
	msgTH.append(dhours[i].get('msgTH'))

# Days plot
fig1,ax = plt.subplots()
barYouD = ax.bar(range(len(days)), msgYD, color='lightgreen', label=yourName)
barFriendD = ax.bar(range(len(days)), msgFD, color='pink', label=friendName, bottom=msgYD)

plt.xticks(range(len(ddays)), days)
fig1.autofmt_xdate()
plt.title('Total number of messages sent each day')
plt.legend()
plt.ylabel('Messages')

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')



# Hour plot
fig2, ax2 = plt.subplots()
barYouH = ax2.bar(range(24), msgYH, color='lightgreen', label=yourName)
barFriendH = ax2.bar(range(24), msgFH, color='pink', label=friendName, bottom=msgYH)

plt.xticks(range(24), hours)
plt.title("Total number of messages sent each hour")
plt.legend()
plt.xlabel('Hour')
plt.ylabel('Messages')

plt.show()