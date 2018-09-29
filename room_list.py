# this is the class that stores the list of rooms
# maybe shouldn't be it's own class idk
import room
import requests
import json
from bs4 import BeautifulSoup as bs
import threading

class room_list(object):

    # the constructor for the room list class which handles operations on multiple rooms
    # file_name is the name of a file that has room information formatted as a json
    # exclude_list is a list of buildings to exclude from search (probably because that room isn't bookable)
    def __init__(self, file_name = None, exclude_list = []):
        self.elements = []
        # if you have a filename, just fetch the room list from the file
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

                # this is just for testing purposes, will be removed soon enough
                # break

            # now we write the results we fetched to a json for caching reasons
            self.store_info_to_file("room_info.json")

        # this is the else, it's a bit easier to follow logically
        else:
            self.load_info_from_file(file_name)
        # sort it before you leave to save yourself some trouble
        self.sort_by_capacity(ascending=False)

    
    # store the results to the file for use later
    # helps to cache performance and not overload the uoft
    # servers lol
    def store_info_to_file(self, file_name):
        # store all the parameters into a dict then convert that to a json and write it to a file
        # do this for all of the rooms
        # this is the dict construction
        element_dict = [ room_.room_dict for room_ in self.elements ]
        # this is the file writing
        # perhaps this should be a member of roomlist along 
        # with the below so the entire json is written at once
        with open(file_name, 'w') as f:
            f.write(json.dumps(element_dict, indent=4))

    # loads the information about the rooms for room bookings from a json file
    # this is done to minimize server traffic and reduce time to increase performance
    # seriously, the time to fetch all the data from server is a few minutes whereas to fetch
    # from file is a few milliseconds
    def load_info_from_file(self, file_name):
        with open(file_name, 'r') as f:
            self.elements = [ room.room(dict_=dict_) for dict_ in json.load(f) ] 

    # sorts the room list by capacity in place
    # ascending or descending order sort depending on if 
    # the ascending flag is set to true 
    def sort_by_capacity(self, ascending=True):
        if ascending == True:
            self.elements.sort(key=lambda x : x.capacity)
        else:
            self.elements.sort(key=lambda x : x.capacity, reverse=True)

    # given a capacity required, a date, and a start and end time,
    # find all rooms that can be booked during those times that satisfy the capacity requirement 
    def get_eligible_rooms(self, capacity, date, start_time, end_time):
        # a list of the eligible roooms to be returned 
        eligible_rooms = []
        # go through all the rooms
        for element in self.elements:
            # if the capacity isn't met, break as the list is sorted so nothing
            # further will meet the requirements either
            if element.capacity < capacity:
                break
            # if this function returns true, the room is vacant
            if element.get_booking_vacancy(date=date, start_time=start_time, end_time=end_time):
                eligible_rooms.append(element)

        return eligible_rooms

    # does the above function but using threads
    # works well because network requests and responses are VERY I/O bound
    # as a result shaves a lot of time
    def multithreaded_get_eligible_rooms(self, capacity, date, start_time, end_time):
        # the list of threads to execute
        thread_list = []
        # go through the list of rooms and only create threads for those who could possibly 
        # be valid room bookings, i.e. have enough capacity
        for idx in range(len(self.elements)):
            if self.elements[idx].capacity < capacity:
                break
            thread_list.append(threading.Thread(target=self.target_get_booking_vacancy, args=(idx, date, start_time, end_time)))
        # then start all the threads and wait for them to finish
        # the actual starting process
        for thread in thread_list:
            thread.start()
        # the loop where the threads all come to die
        for thread in thread_list:
            thread.join()
        # the list of the eligible rooms
        eligible_rooms = []
        # now go through all of the threads and check which ones have been found to be vacant
        # yes this can be done before the threads join by introducing a lock
        # no i don't feel like doing that right now
        for element in self.elements:
            if element.capacity < capacity:
                break
            if element.vacant == True:
                eligible_rooms.append(element)

        return eligible_rooms



    # a function whose only purpose is to be called several times in parallel
    # by multiple threads, returns the booking vacancy of a particular room in the room list
    def target_get_booking_vacancy(self, index, date, start_time, end_time):
        self.elements[index].get_booking_vacancy(date=date, start_time=start_time, end_time=end_time)