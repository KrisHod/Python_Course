# Often it is easier to observer the patterns and characteristics of log infomation by charting the log information. 
# Python has tools to help plot data. 
# These tools are widely used to visualize all sorts of information.

import re
from datetime import datetime as dt
import matplotlib.pyplot as plt
from collections import Counter
from log_analyzer import openLogFile

def parseSmb(log_entry):
    pattern = r"^(?P<ts>[0-9]{2}:[0-9]{2}:[0-9]{2})\s:\s(?P<client_hostname>[a-zA-Z0-9\-]+)\|(?P<client_ip>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\|(?P<share>[a-zA-Z0-9\-]+)\|(?P<operation>[a-zA-Z]+)\|ok\|(?P<path>.*)$"

    log_data = re.search(pattern, log_entry) #Match the regex with the log entry

    r = log_data.groupdict() #Create a dictionary from the regex match
    r['ts'] = dt.strptime(r['ts'], "%H:%M:%S") #Convert the time

    #Handle cases with multiple filenames
    if r['operation'] == 'rename':
        r['path'] = r['path'].split("|")[-1]
    return r

def plotBarChart(events, users):
    plt.subplot(211)
    plt.bar(range(len(events)), list(events.values()), align="center")
    plt.xticks(range(len(events)), list(events.keys()))
    plt.subplot(212)
    plt.bar(range(len(users)), list(users.values()), align="center")
    plt.xticks(range(len(users)), list(users.keys()))
    plt.show()

def getBaseTs(ts, interval):
    # divide an hour into the interval number of sections
    interval = int(60 / interval)

    hours = ts.time().hour
    minutes = ts.time().minute

    base_minutes = int(minutes / interval) * interval
    return "{}:{}".format(hours,base_minutes)

def plotSmbActivity(path):
    log_file = openLogFile(path)
    users = Counter()
    events = Counter()
    for log_entry in log_file:
        try:
            log_data = parseSmb(log_entry)
            users.update([log_data['client_hostname']])
            ts = getBaseTs(log_data['ts'], 4)
            events.update([ts])
        except:
            pass
    plotBarChart(events, users)

plotSmbActivity("log_file_analysis\logs\smb.log")