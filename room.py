# a class that holds the information for each of the rooms
# the info is the room number, the building it is in, 
# the capacity of the room and the cost of booking
import requests
from bs4 import BeautifulSoup as bs
import json

class room(object):
    
    # constructs a room object which stores the info stored on above
    # dict_ specifies whether or not to fetch the info from the server 
    # or to use a dict that would have been generated from a json file
    # the file is used to cache the results
    def __init__(self, building_code = None, room_number = None, dict_ = None):
        # depending on whether or not a dict is specified
        # update from the server or from a dict if a dict is given
        if dict_ is None:
            self.building_code = building_code
            self.room_number = room_number
            self.fetch_info_from_server()
            # when you fetch from the server, in order to allow the room_list
            # class to store the results
            self.create_dict_from_room()
        elif building_code is None and room_number is None:
            # if the dict is specified, use it to generate the neccessary fields
            # for the struct
            self.room_dict = dict_
            self.building_code = dict_['building_code']
            self.capacity = dict_['capacity']
            self.cost = dict_['cost']
            self.room_number = dict_['room_number']
        else:
            # this should never occur
            # should probably raise an exception
            print 'This is not good'


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

    # convert the fields into a dict for use when writing to a json file
    def create_dict_from_room(self):
        # we just brute force it for now, there may be a more elegant solution
        self.room_dict = {}
        self.room_dict['building_code'] = self.building_code
        self.room_dict['room_number'] = self.room_number
        self.room_dict['capacity'] = self.capacity
        self.room_dict['cost'] = self.cost
        return self.room_dict

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