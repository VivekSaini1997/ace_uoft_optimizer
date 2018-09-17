import requests
import sys
import room
import room_list
import time

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
    print "{} seconds elapsed".format(t2 - t1)
    for element in rl.elements:
        print element.building_code, element.room_number, element.cost, element.capacity



if __name__ == "__main__":
    test_main()