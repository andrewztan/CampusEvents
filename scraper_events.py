import requests
import html
from bs4 import BeautifulSoup
from google_calendar_parse import *

url_feb = "http://events.berkeley.edu/?view=summary&timeframe=month&date=2016-02-01&tab=all_events"
url_jan = "http://events.berkeley.edu/?view=summary&timeframe=month&date=2016-01-01&tab=all_events"
event_url = "http://events.berkeley.edu/?event_ID="
# url_page_2 = url + '?page=' + str(2)

# def get_data_from_url(url, n=10):

### Event Class ###
class Event():
    def __init__(self, name, id, event_link, gcal_link, description=None):
        self.name = name
        self.id = id
        self.event_link = event_link
        self.gcal_link = gcal_link
        self.description = description

list_of_event_objects = []
list_of_event_info = []

r = requests.get(url_feb)

soup = BeautifulSoup(r.content, "html.parser")

links = soup.find_all("a") # Find all the links using a tag

g_data = soup.find_all("div", {"class": "event"}) # General data for all events

def get_id(str):
    l = 0
    index = 0
    start = 0
    end = str.find('&')
    while l < len(str):
        if str[index].isdigit() and start == 0:
            start = index
            break
        index += 1
        l += 1
    return str[start:end]

def convert_char(link):
    return html.unescape(link)

# Creates Event object for each event
for entry in g_data:
    event_name = convert_char(entry.find("h3").text)
    url_id = entry.find("h3").find("a").get("href")
    event_id = get_id(url_id)
    event_link = "http://events.berkeley.edu/" + url_id
    p_list = entry.find_all("p")[5:]
    for i in range(len(p_list)):
        p_list[i] = p_list[i].text
    event_description = max(p_list, key=len)
    try:
        link = entry.find("p", {"class": "appointmentThis"}).find("a")
        if 'google.com/calendar' in link.get("href"):
            google_cal_link = link.get("href")
            list_of_event_objects.append(Event(event_name, event_id, event_link, google_cal_link, event_description)) # Adding each event as an Event object into the list_of_event_objects
            # print (event_name)
            # print (event_link)
            # print (event_id)
            # print (event_description)
            # print()
    except AttributeError:
        pass


# for getting description use 7th <p> tag in each entry/event *** some events will have no 7th <p> tag - None



### Putting all events in list_of_event_objects into list of dictionaries. Dictionary contains event information pulled from google cal link ###
info_title = ["event_location", "date", "event_time", "end_time", "epoch"]
for event in list_of_event_objects:
    dict_info = dict([("event_name", event.name), ('event_id', str(event.id)), ('event_link', event.event_link), ('event_description', event.description), ('link', event.gcal_link)])
    print('event_name: ' + event.name)
    print('event_id: ' + event.id)
    for info in info_title:
        val = str(get_event_info(event.gcal_link, info))
        print(info + ": " + val)
        dict_info[info] = val
    list_of_event_info.append(dict_info)
    print()

print (list_of_event_info[0])


# For loop of payloads
for event in list_of_event_info:
    payload = event
    r = requests.post("http://kunald.me/campus_events/web/api/scape_berkeley_events.php", data=payload)










################################################### Old Stuff ###################################################


# for link in links:
#     # if "http" in link.get("href"): # Checks that there actually is a link, use try or except
#         print ("<a href='%s'>%s</a>" %(link.get("href"), link.text)) # String substitution
#         # print(soup.find_all("table", {"id": "headerTable"}))




# for entry in g_data:
#     items = entry.find_all("p", {"class": "appointmentThis"})
#     # descriptions = entry.find_all("p")
#     for item in items:
#         links = item.find_all("a")
#         for link in links:
#             if 'google.com/calendar' in link.get("href"):
#                 google_cal_link = link.get("href")
#                 print (entry.find("h3").text)
#                 print (google_cal_link)
#                 print (get_id(entry.find("h3").find("a").get("href")))
#     print()


    






