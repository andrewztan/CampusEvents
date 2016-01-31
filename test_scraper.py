import requests
import html
from bs4 import BeautifulSoup
from google_calendar_parse import *

url = "http://events.berkeley.edu/?view=summary&timeframe=month&date=2015-12-24&tab=all_events"
event_url = "http://events.berkeley.edu/?event_ID="
# url_page_2 = url + '?page=' + str(2)

# def get_data_from_url(url, n=10):

### Event Class ###
class Event():
    def __init__(self, name, id, link):
        self.name = name
        self.id = id
        self.link = link

list_of_event_objects = []
list_of_event_info = []

r = requests.get(url)

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

for entry in g_data:
    event_name = convert_char(entry.find("h3").text)
    event_id = get_id(entry.find("h3").find("a").get("href"))
    try:
        link = entry.find("p", {"class": "appointmentThis"}).find("a")
        if 'google.com/calendar' in link.get("href"):
            google_cal_link = link.get("href")
            list_of_event_objects.append(Event(event_name, event_id, google_cal_link)) # Adding each event as an Event object into the list_of_event_objects
            # print (event_name)
            # print (google_cal_link)
            # print (event_id)
            # print()
    except AttributeError:
        pass


"""
### Putting all events in list_of_event_objects into list of dictionaries. Dictionary contains event information pulled from google cal link ###
info_title = ["event_location", "event_description", "date", "event_time", "end_time", "epoch", "link"]
for event in list_of_event_objects:
    dict_info = dict([("event_name", event.name), ('event_id', str(event.id))])
    print('event_name' + ": " + event.name)
    print('event_id' + ": " + event.id)
    for info in info_title:
        val = str(get_event_info(event.link, info))
        print(info + ": " + val)
        dict_info[info] = val
    list_of_event_info.append(dict_info)
    print()

print (list_of_event_info[0])
"""
