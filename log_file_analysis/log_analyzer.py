import re, json
import Evtx.Evtx as evtx
from datetime import datetime as dt

def openLogFile(path):
    with open(path) as log_file:
        for log_entry in log_file:
            yield log_entry

def openEvtxFile(path):
    with evtx.Evtx(path) as log_file:
        for log_entry in log_file:
            yield log_entry

def parseZeekConn(log_entry):
    log_data = re.split("\t", log_entry.rstrip())
    r = {}
    r["ts"] = dt.fromtimestamp(float(log_data[0]))
    r["uid"] = log_data[1]
    r["src_ip"] = log_data[2]
    r["src_port"] = log_data[3]
    r["dst_ip"] = log_data[4]
    r["dst_port"] = log_data[5]
    r["proto"] = log_data[6]
    r["service"] = log_data[7]
    return r

def parseEvtx(event):
    sys_tag = event.find("System", event.nsmap)
    event_id = sys_tag.find("EventID", event.nsmap)
    event_ts = sys_tag.find("TimeCreated", event.nsmap)
    event_data = event.find("EventData", event.nsmap)
    r = {}
    r["ts"] = event_ts.values()[0]
    r["eid"] = event_id.text
    for data in event_data.getchildren():
        r[data.attrib["Name"]] = data.text
    return r

def detectRundll32(path):
    log_file = openEvtxFile(path)
    for log_entry in log_file:
        try:
            log_data = parseEvtx(log_entry)
            if log_data['eid'] == "4688" and log_data["CommandLine"]:
                if "rundll32" in log_data["NewProcessName"] and re.search("powershell|cmd", log_data["ParentProcessName"]):
                    print(log_data["CommandLine"])
        except:
            pass