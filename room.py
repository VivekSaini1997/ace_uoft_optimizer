# a class that holds the information for each of the rooms
# the info is the room number, the building it is in, 
# the capacity of the room and the cost of booking
import requests
from bs4 import BeautifulSoup as bs
import json

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
            # when you fetch from the server, save to a file so as to not be rude
            file_name = 'lol.json'
            self.store_info_to_file(file_name)
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
    # this approach may have to be rethought up
    def fetch_info_from_file(self, file_name):
        pass

    # store the results to the file for use later
    # helps to cache performance and not overload the uoft
    # servers lol
    def store_info_to_file(self, file_name):
        # store all the parameters into a dict then convert that to a json and write it to a file
        # this is the dict construction
        room_dict = {}
        room_dict['building_code'] = self.building_code
        room_dict['room_number'] = self.room_number
        room_dict['capacity'] = self.capacity
        room_dict['cost'] = self.cost
        # this is the file writing
        # perhaps this should be a member of roomlist along 
        # with the below so the entire json is written at once
        with open(file_name, 'a') as f:
            f.write(json.dumps(room_dict))
            f.write(',\n')

# given a parameter, fetches a parameter from a given soup
# this utilizes the manner in which parameters are
# stored in the html for ace.utoronto.ca
# this might not work in the future lmao
def fetch_parameter_from_html(soup, param):
    for tag in soup.descendants:
        for sibling_tag in tag.previous_siblings:
            if param in sibling_tag:
                # if the room can't be rented, there is a janky non ascii character instead of 
                # anything meaningful, as a result, catch that character and return something else
                try:
                    return str(tag.contents[0])
                except UnicodeEncodeError:
                    return "Can't be booked"