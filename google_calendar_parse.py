import datetime

link = "https://calendar.google.com/calendar/render?action=TEMPLATE&text=The+Future+of+Memory:+Jewish+Culture+in+the+Digital+Age&dates=20151203T190000Z/20151204T000000Z&location=Magnes+Collection+of+Jewish+Art+and+Life+(2121+Allston+Way),+UC+Berkeley+(Room+Main+Gallery)&sprop=website:events.berkeley.edu&pli=1&sf=true&output=xml#eventpage_6"
link1 = "https://calendar.google.com/calendar/render?action=TEMPLATE&text=Maintain+Don%E2%80%99t+Gain:+Healthy+Holiday+Challenge+(BEUHS640)&dates=20151201T080000Z/20151201T080000Z&location=UC+Berkeley+Campus,+UC+Berkeley&sprop=website:events.berkeley.edu&pli=1&sf=true&output=xml#eventpage_6"
link2 = "https://calendar.google.com/calendar/render?action=TEMPLATE&text=Design+Quest&dates=20151206T180000Z/20151207T010000Z&location=+Lawrence+Hall+of+Science&sprop=website:events.berkeley.edu&pli=1&sf=true&output=xml#eventpage_6"
link3 = "https://calendar.google.com/calendar/render?action=TEMPLATE&text=Solving+the+&&pli=1&sf=true&output=xml#eventpage_6"
link4 = "https://calendar.google.com/calendar/render?action=TEMPLATE&text=Getting+Started+in+Undergraduate+Research+and+Finding+a+Mentor+Workshop&dates=20151216T210000Z/20151216T220000Z&location=9+Durant+Hall&sprop=website:events.berkeley.edu&pli=1&sf=true&output=xml"


def get_event_info(link, data):
	if data == "event_location":
		try:
			index = link.index('&location') + 10
		except ValueError:
			return 
	elif data == "event_name":
		try:
			index = link.index('&text') + 6
		except ValueError:
			return 
	elif data == "event_description":
		try:
			index = link.index('&details') + 9
		except ValueError:
			return 
	elif data == "event_time":
		return get_event_time(link, True, False, False)
	elif data == "end_time":
		return get_event_time(link, False, False, False)
	elif data == "epoch":
		return get_event_time(link, True, True, False)
	elif data == "date":
		return get_event_time(link, True, False, True)
	if index < 0:
		return
	else:
		link = link[index:]
		end_index = link.index('&')
		link = link[:end_index]
		link = replace_characters(link)
		return link


def replace_characters(link):
	link = link.replace("%20", " ")
	link = link.replace("+", " ")
	link = link.replace("%27", "'")
	return link


def get_event_time(link, start=True, epoch=False, get_date=False):
	try:
		index = link.index('&dates') + 7
	except ValueError:
		return 
	if not start:
		index = index + link[index:].index("Z/") + 2
	year = int(link[index:index+4])
	index = index + 4
	month = int(link[index:index + 2])
	index = index + 2
	date = int(link[index: index + 2])
	index = index + 3
	time = link[index: index + 6]
	hour = convert_to_PST(time[:2])	
	minute = time[2:4]
	second = time[4:6]
	date_obj = datetime.date(year, month, date)
	time_obj = datetime.datetime.strptime(hour + ":" + minute, "%H:%M").strftime("%I:%M %p")
	epoch_obj = datetime.datetime(year, month, date, int(hour), int(minute), int(second))
	if epoch:
		return int(epoch_obj.strftime('%s'))
	elif get_date:
		return date_obj.strftime("%a") + " " + date_obj.strftime("%b") + " " + str(date_obj.day)
	else:
		return time_obj

def convert_to_PST(time):

	if int(time) - 8 < 0:
		hour = int(time[1])
		return str(24 + (hour - 8))
	else:
		hour = int(time[:2])
		return str(hour - 8)

for elem in (link, link1):
    print("NEXT EVENT")
    for info in ["event_location", "event_name", "event_description", "event_time", "end_time"]:
        val = str(get_event_info(elem, info))
        print(info + ": " + val)
    print("")
