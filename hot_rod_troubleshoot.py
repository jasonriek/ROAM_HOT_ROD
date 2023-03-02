import json
from requests import post
import socket
import csv
from datetime import datetime
from traceback import format_exc
from math import sqrt

class Troubleshoot:
    ROAM_HOST = 'http://192.168.0.14:3000/distress'
    COLLISION_TABLE = '/home/pi/ROAM_calls/data/collisions.csv'
    def __init__(self):
        self.collision_count = 0
        self.distance_cache = []
    
    def writeToCollisionTable(self, collision_count:int):
        with open(self.COLLISION_TABLE, 'a') as ct:
            writer = csv.writer(ct)
            writer.writerow([collision_count, str(datetime.now())])

    def sendDistressToROAM(self):
        name = socket.gethostname()
        payload= {
            'message': f"ROAM, this is {name}, I'm stuck, please come get me...",
            'name': name
            }
        headers = {'content-type': 'application/json'}
        rsp = post(self.ROAM_HOST, headers=headers, data=json.dumps(payload))
        print(rsp.text)
    

    def isStuck(self):
        if len(self.distance_cache) >= 25:
            distance_average = round(sum(self.distance_cache)/len(self.distance_cache))
            variance = sum([(distance - distance_average)**2 for distance in self.distance_cache])/len(self.distance_cache)
            std_dev = round(sqrt(variance))
            print(f"std_dev: {std_dev}")
            return (std_dev <= 3)
        return False

