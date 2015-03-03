#!/usr/bin/python3

from queue import Queue
from threading import Thread

import time

def worker():
    while not q.empty():
        item = q.get()
        print(item)
        time.sleep(2)
        q.task_done()

q = Queue()
for i in range(30):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for item in range(100):
    q.put(item)

q.join() 
