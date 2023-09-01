# Recall that DNS translates a human readable name to an IP address. 
# Typically, before opening a connection, a DNS request is generated to get the correct IP address. 
# By looking at these requests we get an idea of the types of connections being generated by our system.
# Aggregating log records allows us to look for patterns in the traffic. 
# We can determine the most frequently (or infrequently) visited domain names. 
# This information can help identify if some unexpected behaviour is occuring. 
# Further, we can look at the domain names to see if any are similar to an expected domain name. 
# Sometimes typos can cause users to access a domain different than the one they intended. 
# Attacks can register these domain names and use them as entry points to a network.

import re
from datetime import datetime as dt
from collections import Counter
from operator import itemgetter
from difflib import SequenceMatcher
from log_analyzer import openLogFile

def parseZeekDns(log_entry):
    log_data = re.split("\t", log_entry.rstrip())
    r = {}
    r["ts"] = dt.fromtimestamp(float(log_data[0]))
    r["uid"] = log_data[1]
    r["src_ip"] = log_data[2]
    r["src_port"] = log_data[3]
    r["dst_ip"] = log_data[4]
    r["dst_port"] = log_data[5]
    r["proto"] = log_data[6]
    r["trans_id"] = log_data[7]
    r["rtt"] = log_data[8]
    r["query"] = log_data[9]
    r["qclass"] = log_data[10]
    r["qclass_name"] = log_data[11]
    r["qtype"] = log_data[12]
    r["qtype_name"] = log_data[13]
    r["rcode"] = log_data[14]
    r["rcode_name"] = log_data[15]
    r["AA"] = log_data[16]
    r["TC"] = log_data[17]
    r["RD"] = log_data[18]
    r["RA"] = log_data[19]
    r["Z"] = log_data[20]
    r["answers"] = log_data[21]
    r["TTLs"] = log_data[22]
    r["rejected"] = log_data[23]
    return r

def getDnsAnomalies(path, similar_domain="globomantics.com"):
    log_file = openLogFile(path)
    domains = Counter()
    for log_entry in log_file:
        try:
            log_data = parseZeekDns(log_entry)
            dns_query = ".".join(log_data['query'].split(".")[-2:])
            domains.update([dns_query])
        except:
            pass

    least_common = domains.most_common()[-10:]
    domain_anomalies = []
    for domain in least_common:
        anomaly = {
            "domain": domain[0],
            "occurence": domain[1],
            "similarity" : round(SequenceMatcher(None, domain[0], similar_domain).ratio() * 100)
        }
        domain_anomalies.append(anomaly)

    domain_anomalies.sort(key=itemgetter("similarity"), reverse=True)
    return domain_anomalies

def printDnsAnomalies(path):
    domains = getDnsAnomalies(path)
    print("{:20}\t{}\t{}".format("Domain", "Occurence", "Similarity"))
    print("-" * 60)
    for domain in domains:
        print("{:20}\t{}\t{}".format(domain['domain'], domain['occurence'], domain['similarity']))

printDnsAnomalies("log_file_analysis\logs\dns.log")

# We can check the DNS queries of the domains we retrieved in our analysis to get the corresponding IP addresses

def printDnsQueries(path, domain):
    log_file = openLogFile(path)
    for log_entry in log_file:
        try:
            log_data = parseZeekDns(log_entry)
            if domain in log_data['query']:
                print("{}\t{}".format(log_data["query"], log_data["answers"]))
        except:
            pass

printDnsQueries("log_file_analysis\logs\dns.log", "globonamtics.com")