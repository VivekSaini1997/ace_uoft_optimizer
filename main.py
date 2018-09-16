import requests
import sys
import room

# the goal is to get it so that you can imput a 
# room capacity requirement and a time and get a list of 
# suitable rooms to book and their associated costs 
# from the ace website at the university of toronto
def main(args):
    pass

# used for debugging and testing 
def test_main():
    r = room.room('BA', '1160')
    print r.capacity 
    print r.cost

if __name__ == "__main__":
    test_main()