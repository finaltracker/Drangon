import json
import requests
import time

def register(index):
    data = {
            'mobile': str(index),
            'password': "123456",
            'confirmpass': "123456",
            'imsi': 12345993+index,
            'nick_name': str(index)
    }

    r = requests.post("http://localhost:8000/user/register2/", data)
    print r.text

def unRegister(index):
    data = {
            'mobile': str(index),
            'password': "123456",
    }

    r = requests.post("http://localhost:8000/user/delete_user/", data)
    print r.text

def fixPosition(index, lat, lng):
    e = 0.016
    data = {
            'mobile': str(index),
            'lat': lat+(e*index),
            'lng': lng+(e*index),
    }

    r = requests.post("http://localhost:8000/feed/locate_upload/", data)
    print r.text

def getAllPosition():
    r = requests.get("http://localhost:8000/feed/all_position/")
    print r.text

    data = []
    response = json.loads(r.text)
    if response['status'] == 0:
        data = response['feeds']
    return data

'''
1. get all register users
2. batch to register robot to system according to real uses' position
'''
if __name__ == '__main__':
    print 'robot start'
    print 'input 1 for creating robot, 2 for deleting robot'

    prestore = getAllPosition()
    robot_num = len(prestore)
    cmd_opt = input("enter:")
    if cmd_opt == 1:
        for i in range(robot_num):
            print i
            register(i)
            fixPosition(i,prestore[i]['lat'], prestore[i]['lng'])

            time.sleep(3)

    if cmd_opt == 2:
        for i in range(robot_num):
            unRegister(i)
            time.sleep(3)

    print 'success!'
