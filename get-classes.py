# KNOWN ISSUES:
# 1) Course title and course code are not included in the dictionary
# 2) Classes that take place in different locations or different times on different days only include the first listed
# time or place.
# 3) Code only scrapes a limited number of classes due to testing stages.
import urllib, re
from bs4 import BeautifulSoup

print("start")
htmlstring = urllib.request.urlopen("https://www.washington.edu/students/timeschd/WIN2018/").read()
soup = BeautifulSoup(htmlstring,"html.parser")

class_dict = {}

def addToDict(link):
    try:
        htmlstring = urllib.request.urlopen(link).read()
        souplocal = BeautifulSoup(htmlstring, "html.parser")
        #print(souplocal.prettify())
        for course in souplocal.find_all('pre'):
            #print(str(course).split())
            answer = str(course).split()[2]
            if (answer and answer[0:4] == "href"):
                searchObj = re.search( r'>(\d{5})</a>', str(course), re.M|re.I)
                SLN = searchObj.group()[1:-4]
                class_dict[SLN] = {}
                instructorSearch = re.search(r'\s{2}([A-Z-]{1,30})([A-Z-a-z]{0,30}|\s){0,5},([A-Z-\.]{1,30})([A-Za-z-\.]{0,30}|\s){0,5}\s{2}', str(course), re.M | re.I)
                if instructorSearch:
                    class_dict[SLN]["instructor"] = instructorSearch.group().strip()
                else:
                    class_dict[SLN]["instructor"] = "TBA"
                buildingSearch = re.search(r'cgi\?(.*)\">', str(course), re.M | re.I)
                if buildingSearch:
                    class_dict[SLN]["building"] = buildingSearch.group()[4:-2]
                else:
                    class_dict[SLN]["building"] = "TBA"
                roomSearch = re.search(r'>(.{3,4})</a>\s+.{1,5}\s+', str(course), re.M | re.I)
                if roomSearch:
                    room = roomSearch.group().split()
                    class_dict[SLN]["room"] = room[len(room)-1]
                else:
                    class_dict[SLN]["room"] = "TBA"
                daySearch = re.search(r'\s+(M|T|W|Th|F|Sa)+\s+', str(course), re.M | re.I)
                try:
                    daySearch.group(2)
                    print("ERROR!!!!!\n" , len(daySearch.groups()), SLN)
                except IndexError:
                    if daySearch:
                        class_dict[SLN]["day"] = daySearch.group().strip()
                    else:
                        print("Error?")
                        class_dict[SLN]["day"] = "TBA"
                timeSearch = re.search(r'\s+(\d{3,4}-\d{3,4})\s+', str(course), re.M | re.I)
                if timeSearch:
                    class_dict[SLN]["time"] = timeSearch.group().strip()
                else:
                    class_dict[SLN]["time"] = "TBA"
        print(class_dict)
    except urllib.error.URLError as e:
        print(e.reason)

url_list = []
for link in soup.find_all('a'):
    if str(link.get('href'))[-4:] == "html":
        url_list.append(link)
start = 5 #url_list.index('<a href="arctic.html">Arctic Studies (ARCTIC)</a>')
stop = 7 #341 #url_list.index('<a href="socwk.html">Arctic Studies (ARCTIC)</a>')
for link in url_list[start:stop]:
    baseurl = "https://www.washington.edu/students/timeschd/WIN2018/"
    babysoup = BeautifulSoup(baseurl,"html.parser")
    addToDict(baseurl + link.get('href'))

def getHTML(link):
    try:
        htmlstring = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(htmlstring, "html.parser")
        for link in soup.find_all('a'):
            print(link)
    except urllib.error.URLError as e:
            print(e.reason)

#   h c d e 3 1 0 - f i n a l 
 
 