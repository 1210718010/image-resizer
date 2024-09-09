import os
import time
import datetime

while True:
        dirToBeEmptied = './static/'
 
        ds = list(os.walk(dirToBeEmptied))
        delta = datetime.timedelta(days=7)
        now = datetime.datetime.now()
 
        for d in ds:
            os.chdir(d[0])
            if d[2] != []:
                for x in d[2]:
                    ctime = datetime.datetime.fromtimestamp(os.path.getmtime(x))
                    if ctime < (now-delta):
                        os.remove(x)
        time.sleep(3600)