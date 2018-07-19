# coding: utf-8

#remember to use right keyboard-pad

from evdev import InputDevice
from select import select
import os
import cv2 as cv
#right pad +
ADD_flag = 78
#right pad -
SUB_flag = 74
#save , right pad enter
ENTER_flag = 96
#key up
UP_flag = 4
#right pad.
DELETE_flag = 83
#right pad 0
Back_flag = 82

def getAgeFromName(name):
    vs = name.split('_')
    s = vs[1]
    age = int(s)
    return age


def deal_ADD():
    print 'deal_ADD'


def deal_SUB():
    print 'deal_SUB'


def deal_ENTER():
    print 'deal_save'


def deal_UP():
    print 'deal_UP'

def deal_back():
	print 'deal_back'

def deal_DELETE():
	print 'deal_delte'

def getSaveName(age , relate_name):
	vs = relate_name.split('_')
	if age < 0:
		age = 0
	new_name = vs[0] +'_'+ str(age) +'_'+ vs[2]
	return new_name

def waitUP():
    print 'waitUP'
    while 1:
        dev = InputDevice('/dev/input/event15')
        select([dev], [], [])
        for event in dev.read():
            if event.code == UP_flag:
                print 'wait UP'
                return 0


def detectInputKey(root, root_list):
    dev = InputDevice('/dev/input/event15')
    list_num = 0
    while True:
		if list_num <0 :
			list_num = 0
		if list_num == len(root_list):
			return 0
		full_read = root + '/' + root_list[list_num]
		age = getAgeFromName(root_list[list_num])
		enterd_ENTER = 1
		while enterd_ENTER:
			m = cv.imread(full_read)
			try:
				m = cv.resize(m,(400 , 400))
			except:
				enterd_ENTER = 0
				list_num += 1
				break
			cv.putText(m , str(age) , (30 ,50) , cv.FONT_HERSHEY_COMPLEX , 2 , (0,255,0) ,3)
			cv.namedWindow('labeling')
			cv.imshow('labeling', m)
			cv.waitKey(1)
			select([dev], [], [])
			for event in dev.read():
				print "code:%s value:%s" % (event.code, event.value)
				if event.code == ADD_flag and event.value == 1:
					age += 2
					deal_ADD()
					waitUP()
				elif event.code == SUB_flag and event.value == 1:
					age -=2
					deal_SUB()
					waitUP()
				elif event.code == ENTER_flag and event.value == 1:
					deal_ENTER()
					enterd_ENTER = 0
					relate_name = getSaveName(age , root_list[list_num])
					full_save = root + '/' + relate_name
					m = cv.imread(full_read) 
					os.remove(full_read)
					print full_save
					cv.imwrite(full_save , m)
					waitUP()
					list_num += 1

				elif event.code == DELETE_flag and event.value == 1:
					deal_DELETE()
					print full_read
					os.remove(full_read)
					enterd_ENTER = 0
					list_num += 1
					waitUP()
				elif event.code == Back_flag and event.value == 1:
					deal_back()
					list_num -= 1
					enterd_ENTER = 0
					waitUP()

if __name__ == '__main__':
	root = './test'
	root_list = os.listdir(root)
	detectInputKey(root, root_list)
