import requests
import sys
import room
import room_list
import time
import threading

# the goal is to get it so that you can imput a 
# room capacity requirement and a time and get a list of 
# suitable rooms to book and their associated costs 
# from the ace website at the university of toronto
def main(args):
    pass

# used for debugging and testing 
def test_main():
    # r = room.room('BA', '1160')
    # print r.capacity 
    # print r.cost
    # t1 and t2 are meant to profile
    t1 = time.time()
    rl = room_list.room_list('hehe.json')
    rl.sort_by_capacity(ascending=False)
    t2 = time.time()
    for r in rl.elements:
        print '{} {} capacity: {}'.format(r.building_code, r.room_number, r.capacity)
    print "{} seconds elapsed".format(t2 - t1)
    # for element in rl.elements:
    #     print element.building_code, element.room_number, element.cost, element.capacity
    # for element in rl.elements:
    #     element.get_booking_vacancy('20190211', start_time='13:30', end_time='14:00')
    #     print " "

    # a very crude implementation of multithreading
    # thread_list = []
    # t1 = time.time()
    # for i in range(len(rl.elements)):
    #     thread_list.append(threading.Thread(target=get_booking_mt, kwargs={'index': i, 'rl': rl, 'date': '20190211', 'start_time': '13:30', 'end_time' : '14:00'}))

    # for i in range(len(thread_list)):
    #     thread_list[i].start()

    # for i in range(len(thread_list)):
    #     thread_list[i].join()
    # t2 = time.time()
    # print "{} seconds elapsed".format(t2 - t1)
    eligible_rooms = rl.multithreaded_get_eligible_rooms(capacity=400 ,date='20190211', start_time='13:30', end_time='14:00')
    for r in eligible_rooms:
        print "{} {} is vacant".format(r.building_code, r.room_number)


if __name__ == "__main__":
    test_main()