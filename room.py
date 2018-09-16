# a class that holds the information for each of the rooms
# the info is the room number, the building it is in, 
# the capacity of the room and the cost of booking
import requests
from bs4 import BeautifulSoup as bs

class room(object):
    
    # constructs a room object which stores the info stored on above
    # fetch_from_server specifies whether or not to fetch the info from the server 
    # or to use a file 
    # the file is used to cache the results
    def __init__(self, building_code, room_number, file_name = None):
        self.building_code = building_code
        self.room_number = room_number
        # depending on whether or not a file name is specified
        # update from the server or from a file if a file is provided
        if file_name is None:
            self.fetch_info_from_server()
        else:
            self.fetch_info_from_file(file_name)

    # fetch the info for the building in particular using 
    # a request to ace.utoronto.ca
    def fetch_info_from_server(self):  
        # this is the server page that has the information about the room
        request_str = "https://ace.utoronto.ca/ws/f?p=210:1:::::P1_BLDG,P1_ROOM:{},{}".format(self.building_code, self.room_number)
        request = requests.get(request_str)
        # use beautiful soup to parse the resultant html to gather 
        # information about the room 
        soup = bs(request.text, features="html.parser")
        self.capacity = int(fetch_parameter_from_html(soup, 'Capacity'))
        self.cost = fetch_parameter_from_html(soup, 'External Rental Rate')

    # fetch the info for the building using a specified file
    # should probably be formatted as a json
    def fetch_info_from_file(self, file_name):
        pass

    # store the results to the file for use later
    # helps to cache performance and not overload the uoft
    # servers lol
    def store_info_to_file(self, file_name):
        pass

# given a parameter, fetches a parameter from a given soup
# this utilizes the manner in which parameters are
# stored in the html for ace.utoronto.ca
# this might not work in the future lmao
def fetch_parameter_from_html(soup, param):
    for tag in soup.descendants:
        for sibling_tag in tag.previous_siblings:
            if param in sibling_tag:
                return str(tag.contents[0])