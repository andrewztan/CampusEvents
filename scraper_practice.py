import requests
from bs4 import BeautifulSoup

url = "http://www.yellowpages.com/los-angeles-ca/coffee-shops"
url_page_2 = url + '?page=' + str(2)

def get_data_from_url(url, n=10):


r = requests.get(url)

soup = BeautifulSoup(r.content)

links = soup.find_all("a") # Find all the links using a tag

for link in links:
	# if "http" in link.get("href"): # Checks that there actually is a link, use try or except
		print ("<a href='%s'>%s</a>" %(link.get("href"), link.text)) # String substitution


g_data = soup.find_all("div", {"class": "info"}) # General data, class to find ids, even if there is 2 classes

for item in g_data:
    print (item.contents[0].find_all("a", {"class": "business-name"})[0].text)
    try: 
        # print (item.contents[1].find_all("p", {"class": "adr"})[0].text)
        print (item.contents[1].find_all("span", {"itemprop": "streetAddress"})[0].text)
    except IndexError:
        pass
    try: 
        print (item.contents[1].find_all("span", {"itemprop": "addressLocality"})[0].text.replace(',', ''))
    except IndexError:
        pass
    try: 
        print (item.contents[1].find_all("span", {"itemprop": "addressRegion"})[0].text)
    except IndexError:
        pass
    try: 
        print (item.contents[1].find_all("span", {"itemprop": "postalCode"})[0].text)
    except IndexError:
        pass
    try:    
        print (item.contents[1].find_all("div", {"class": "primary"})[0].text)
    except IndexError:
        pass


