#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
    Author: Tyler Chen ( tyler@lastline.com / alphaone.tw@gmail.com )
    Date: 2014 Dec 28
    Version: 1.0
    This script is used to do counting for JSON data exported from Lastline, and save it to a CSV formatted file.
    It intends to do Top-N for items shown in web/email events from Lastline.
    This script will show items that has score/impact greater than 0.
    
    For example:
    
    $python count_event.py -i incident_c2c_infection.json -o top_c2c_src_host.txt -k "src_host" -n 10
    $cat top_c2c_src_host.txt
    SRC_HOST	COUNT
    163.14.175.55	6
    163.14.200.244	4
    163.14.229.23	4
    163.14.26.153	3
    163.14.232.102	3
    163.14.232.101	3
    163.14.232.104	3
    163.14.232.95	3
    163.14.232.88	3
    163.14.192.63	2

    From the above example, file "top_c2c_src_host.txt" will show top 10 for src_host element from file "incident_c2c_infection.json", which was exported from Lastline.
    Use M$ excel to open that Top-N txt file, copy paste to what ever application you need, my case is ppt.

    '''

import json
import csv
import sys
from collections import Counter
# Is there argparse to use?
try:
    import argparse
except ImportError:
    print "Please install the argparse python module\non Debian systems you can use:\napt-get install python-argparse"
    sys.exit()

parser = argparse.ArgumentParser(
                                 description = "This is a tool to extract IP addresses from an Lastline Enterprise exported event file in JSON format.",     # text displayed on top of --help
                                 epilog = 'Use it at your own risk!') # last text displayed
parser.add_argument('-i','--input_file',action="store",default='events.json',dest='in_file',help='Lastline event file in JSON format')
parser.add_argument('-o','--output_file',action="store",default='top_n.txt',dest='out_file',help='Exported Top-N list')
parser.add_argument('-k','--key',action="store",default='src_host',dest='keyvalue',help='The key value that we are going to count for Top-N, default to "src_host"')
parser.add_argument('-n','--n',action="store",default=10,dest='topn',type=int,help='Number of Top-N, default to 10')
arguments = parser.parse_args()

in_file = arguments.in_file
out_file = arguments.out_file
keyvalue = arguments.keyvalue
topn = arguments.topn
keyvalue_upper = keyvalue.upper()

try:
    data = json.load(open(in_file, 'r')) # Open our JSON file and parse it, store it into a variable called data.
except (ValueError, IOError):
    print "X"*80
    print "[-]Error! No JSON object could be decoded"
    print "[-]Maybe you have specified the wrong JSON file?"
    print "[-]Please check your JSON file followed by -i paramater"
    print "[-]Exiting program......"
    print "X"*80
    sys.exit()

a = data["data"] # Retrieve value for key "data" inside variable data then store in a. This a is a list.
c = []  # Empty list

try:
    a[0][keyvalue]
except KeyError:
    print "X"*80
    print "[-]Error! Wrong key value!"
    print "[-]Please use the correct key value to count for Top N with -k paramater"
    print "[-]Exiting program......"
    print "X"*80
    sys.exit()

if "score" in a[0].keys():
    for i in range(len(a)):
        if a[i]["score"] >= 0:
            c.append(a[i][keyvalue])
elif "impact" in a[0].keys():
    for i in range(len(a)):
        if a[i]["impact"] >= 0:
            c.append(a[i][keyvalue])
else:
    print "X"*80
    print "[-]Error! There is no 'score' nor 'impact' inside JSON data"
    print "[-]Please check your JSON data followed by -i paramater"
    print "[-]Exiting program......"
    print "X"*80
    sys.exit()

utf8encoded = [s.encode('utf8') for s in c]

d = Counter(utf8encoded).most_common(topn)

try:
    with open(out_file, 'wb') as fo:
        writer = csv.writer(fo, dialect='excel', delimiter='\t')
        writer.writerow( ( keyvalue_upper, 'COUNT' ))
        writer.writerows(d)
    fo.close()
except IOError:
    print "X"*80
    print "[-]Error! Permission denied: '%s'" % out_file
    print "[-]Please check if you have the write permission for destination directory or file"
    print "[-]Exiting program......"
    print "X"*80
    sys.exit()

print "-"*80
print "[+]Successfully exported Top-N result to '%s'" % out_file
print "-"*80