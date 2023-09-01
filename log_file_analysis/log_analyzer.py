import re, json
from datetime import datetime as dt
from samples import samples

def openLogFile(path):
    with open(path) as log_file:
        for log_entry in log_file:
            yield log_entry

log_file = openLogFile(r"C:\Users\Kris\Desktop\PythonCourse\log_file_analysis\logs\smb.log")
print(type(log_file))
print(next(log_file))


# Log files contain structured data, i.e., the information is arrangedin a meaningful way. 
# Parsing allows us to interpret the raw text using this structure. 
# In this example the we use snippets of a Zeek logfile. Zeek is a network monitoring tool.
def parseZeekConn(log_entry):
    log_data = re.split("\t", log_entry.rstrip())
    print(log_data)
    r = {}
    r["ts"] = log_data[0]
    r["uid"] = log_data[1]
    r["src_ip"] = log_data[2]
    r["src_port"] = log_data[3]
    r["dst_ip"] = log_data[4]
    r["dst_port"] = log_data[5]
    r["proto"] = log_data[6]
    r["service"] = log_data[7]
    r["duration"] = log_data[8]
    r["src_bytes"] = log_data[9]
    r["dst_bytes"] = log_data[10]
    r["conn_state"] = log_data[11]
    r["local_src"] = log_data[12]
    r["local_rsp"] = log_data[13]
    r["missed_bytes"] = log_data[14]
    r["history"] = log_data[15]
    r["srk_pkts"] = log_data[16]
    r["src_ip_bytes"] = log_data[17]
    r["dst_pkts"] = log_data[18]
    r["dst_ip_bytes"] = log_data[19]
    r["tunnel_parents"] = log_data[20]
    return r

print(parseZeekConn(samples.zeek_conn))


# Computers often store time information in the form of a timestamp. 
# This timestamp represents the number of seconds (or milliseconds, microseconds, etc.) elapsed since a specific reference point, known as the "epoch".
# The Unix epoch, for example, is midnight on January 1, 1970 (UTC). The system clock keeps track of the elapsed time from the epoch. To interpret the timestamp into something more useful to humans we can use a Date-Time object. 
# These objects offer high-level manipulation and formatting of date and time values.

print(samples.zeek_ts)
print(dt.fromtimestamp(float(samples.zeek_ts)))

# Using Regular Expressions to Parse Log Files
# Sometimes log data is not nicely structured with a consistent delimeter. 
# In these cases we can use regular expressions to help parse the data into meaningful field. 
# In PluralSight, a tool called CyberChef is usef to help generate the regular expression.

# The log entry being analzyed is an SMB log which is created by the Server Message Block (SMB) protocol. 
# SMB is a network communication protocol that enables applications and devices to request and share files and services from other network devices, primarily in Windows-based environments.
def parseSmb(log_entry):
    pattern = r"^(?P<ts>[0-9]{2}:[0-9]{2}:[0-9]{2})\s:\s(?P<client_hostname>[a-zA-Z0-9\-]+)\|(?P<client_ip>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\|(?P<share>[a-zA-Z0-9\-]+)\|(?P<operation>[a-zA-Z]+)\|ok\|(?P<path>.*)$"

    log_data = re.search(pattern, log_entry) #Match the regex with the log entry

    r = log_data.groupdict() #Create a dictionary from the regex match
    r['ts'] = dt.strptime(r['ts'], "%H:%M:%S") #Convert the time

    #Handle cases with multiple filenames
    if r['operation'] == 'rename':
        r['path'] = r['path'].split("|")[-1]
    return r

smb_log = parseSmb(samples.smb2)
print(smb_log)
print(type(smb_log))
print(type(smb_log['ts']))