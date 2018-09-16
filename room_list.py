# this is the class that stores the list of rooms
# maybe shouldn't be it's own class idk
import room
import requests
from bs4 import BeautifulSoup as bs

class room_list(object):
    def __init__(self, file_name = None):
        self.elements = []
        # if you have a filenaame, just fetch the room list from the file
        # else go to the server to fetch it
        if file_name is None:
            # this is the url that is used to figure out the rooms for each of the buildings
            # you may not like it, but this is what peak performance looks like lmao
            # (it's really not peak performance)
            building_search_url = "https://ace.utoronto.ca/ws/f?p=210:1"
            building_request = requests.get(building_search_url)
            
            # now we have to parse the html 
            building_soup = bs(building_request.text, features="html.parser")
            # this list generation compiles all of the building codes to be used to determine the rooms
            building_list = [ building['value'] for building in building_soup.find_all('option') if 'null' not in building['value'] ]

            # given all of the building codes, we can determine all of the rooms for a particular building
            # and store every room number and building code combination as a room
            for building in building_list:
                # fetch the rooms for each building from the url
                room_search_url = "https://ace.utoronto.ca/ws/f?p=210:1:::::P1_BLDG:{}".format(building)
                room_number_request = requests.get(room_search_url)
                room_number_soup = bs(room_number_request.text, features="html.parser")
                # a slightly inefficient way of gathering all of the rooms for a given building
                # should probably be reworked as well to run faster
                room_number_list = [ room_number['value'] for room_number in room_number_soup.find_all('option') if 'null' not in room_number['value'] and room_number['value'] not in building_list ]
                # print room_number_list
                # this constructs the rooms from the numbers and adds them to the elements
                for room_number in room_number_list:
                    self.elements.append(room.room(building, room_number))

        else:
            pass