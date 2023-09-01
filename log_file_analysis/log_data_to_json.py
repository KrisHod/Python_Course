#We will procees the log data, convert it to JSON objects and store it in a file. 
#This process allows us to achieve persistent storage, and is in an easy format to be stored in a database at a later date.

import json
import re
from datetime import datetime as dt
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

def writeJSONToFile(alerts, filename="alerts.json"):
    with open(filename, 'w') as json_file:
        for alert in alerts:

          #Handle date/time
          alert['ts'] = alert['ts'].isoformat()
          alert['ts_added'] = alert['ts_added'].isoformat()
          json.dump(alert, json_file)

def ransomwareAlert(path="logs/smb.log"):

    # pattern to detect common ransomware extensions in file paths
    ext_re = r"\.encrypted|\.locked|\.wncry"

    smb_log = openLogFile(path)

    alert_list = []
    for log_entry in smb_log:
        try:
            log_data = parseSmb(log_entry)
            if re.search(ext_re, log_data['path']):
                log_data['ts_added'] = dt.utcnow()
                alert_list.append(log_data)
        except:
            pass
    return alert_list;

alerts = ransomwareAlert("log_file_analysis\logs\smb.log")
writeJSONToFile(alerts)