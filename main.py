import requests
import sys
import room
import room_list
import time
import threading
import argparse

# the goal is to get it so that you can imput a 
# room capacity requirement and a time and get a list of 
# suitable rooms to book and their associated costs 
# from the ace website at the university of toronto
def main():
    # create a parser for the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--capacity', type=int, help='specify the minimum capcity desired')
    # not implemented yet
    #parser.add_argument('-p', '--cost', type=int, help='specify the maximum hourly rate')
    parser.add_argument('-r', '--refresh', help='refresh the list of building info from the json file', action='store_true')
    parser.add_argument('date', help='the date of your booking, formatted YYYYMMDD')
    parser.add_argument('starttime', help='the start time of your booking, formatted HH:MM, 24h time')
    parser.add_argument('endtime', help='the end time of your booking, formatted HH:MM, 24h time')
    args = parser.parse_args()
    # set up the room list depending on whether you want to refresh the json or not
    rl = []
    if args.refresh is True:
        rl = room_list.room_list()
    else:
        rl = room_list.room_list('room_info.json')
    # set the capacity to 0 by default if no capacity is selected
    if args.capacity is None:
        args.capacity = 0
    # find the eligible rooms 
    eligible_rooms = rl.multithreaded_get_eligible_rooms(capacity=args.capacity ,date=args.date, start_time=args.starttime, end_time=args.endtime)
    # print the eligible rooms
    for room_ in eligible_rooms:
        print("{} {} is vacant at a cost of {}, the url is {}".format(room_.building_code, room_.room_number, room_.cost, room_.url))
    if len(eligible_rooms) == 0:
        print("No rooms available to satisfy those conditions, sorry.")
    #print args.date

# used for debugging and testing 
def test_main():

    t1 = time.time()
    rl = room_list.room_list('room_info.json')
    rl.sort_by_capacity(ascending=False)
    t2 = time.time()

    print("{} seconds elapsed".format(t2 - t1))

    eligible_rooms = rl.multithreaded_get_eligible_rooms(capacity=200 ,date='20190211', start_time='13:30', end_time='14:00')
    for r in eligible_rooms:
        print("{} {} is vacant".format(r.building_code, r.room_number))



if __name__ == "__main__":
    main()