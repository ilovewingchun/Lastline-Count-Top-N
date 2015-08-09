#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
    Author: Tyler Chen ( tyler@lastline.com / alphaone.tw@gmail.com )
    Date: 2015 07 12
    Version: 1.10
    This script is used to do counting for JSON data exported from Lastline, and save it to a CSV formatted file.
    It intends to do Top-N for items shown in web/email events from Lastline.
    This script will only count items that has score/impact greater than 70.
    
    For example:
    
    $python count_top_n.py -i incident_c2c_infection.json -o top10_c2c_src_host.txt -k "src_host" -n 10
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

    This script can also do counting based on certain email recpient domain names.
    For example, if customer has 4 domain names:
    
    abc,xyz,123,567

    To count data only for those 4 domain names, do the following:

    $python count_top_n.py -i emails.json -o top10_sender.txt -k "recipient" -n 10 -r abc -r xyz -r 123 -r 567

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
                                 description = "This script is used to do counting for JSON data exported from Lastline, and save it to a CSV formatted file. It intends to do Top-N for items shown in web/email events from Lastline. This script will only count items that has score/impact greater than 70.",     # text displayed on top of --help
                                 )
parser.add_argument('-i','--input_file',action="store",default='events.json',dest='in_file',help='Lastline event file in JSON format')
parser.add_argument('-o','--output_file',action="store",default='top_n.txt',dest='out_file',help='Exported Top-N list')
parser.add_argument('-k','--key',action="store",default='src_host',dest='keyvalue',help='The key value that we are going to count for Top-N, default to "src_host"')
parser.add_argument('-n','--n',action="store",default=10,dest='topn',type=int,help='Number of Top-N, default to 10')
parser.add_argument('-r', '--recipient_domain', action='append', nargs='?',dest='recipient_domain',help='Email recipient domain')

arguments = parser.parse_args()

in_file = arguments.in_file
out_file = arguments.out_file
keyvalue = arguments.keyvalue
topn = arguments.topn
recipient_domain = arguments.recipient_domain
keyvalue_upper = keyvalue.upper()

# Can we open that json data?
try:
    data = json.load(open(in_file, 'r'))    # Open our JSON file and parse it, store it into a variable called data.
except (ValueError, IOError):
    print "X"*80
    print "[-]Error! No JSON object could be decoded"
    print "[-]Maybe you have specified the wrong JSON file?"
    print "[-]Please check your JSON file followed by -i paramater"
    print "[-]Exiting program......"
    print "X"*80
    sys.exit()

temp_list = data["data"]    # Retrieve value for key "data" inside variable data then store in temp_list. This is a list.
temp2_list = []  # Creating an empty list.

try:
    temp_list[0][keyvalue]
except KeyError:
    print "X"*80
    print "[-]Error! Wrong key value!"
    print "[-]Please use the correct key value to count for Top N with -k paramater"
    print "[-]Exiting program......"
    print "X"*80
    sys.exit()

#To do: try to combine score and impact if else statement into fewer codes
if "score" in temp_list[0].keys():
    for i in range(len(temp_list)):
        if temp_list[i]["score"] >= 70:
            if recipient_domain:
                for dns in recipient_domain:
                    if dns in unicode.lower(temp_list[i]["recipient"]):
                        temp2_list.append(temp_list[i][keyvalue])
                    else:
                        continue
            else:
                temp2_list.append(temp_list[i][keyvalue])
elif "impact" in temp_list[0].keys():
    for i in range(len(temp_list)):
        if temp_list[i]["impact"] >= 70:
            if recipient_domain:
                for dns in recipient_domain:
                    if dns in unicode.lower(temp_list[i]["recipient"]):
                        temp2_list.append(temp_list[i][keyvalue])
                    else:
                        continue
            else:
                temp2_list.append(temp_list[i][keyvalue])
else:
    print "X"*80
    print "[-]Error! There is no 'score' nor 'impact' inside JSON data"
    print "[-]Please check your JSON data followed by -i paramater"
    print "[-]Exiting program......"
    print "X"*80
    sys.exit()


#New version code but not working well :(
#if "score" in temp_list[0].keys() or "impact" in temp_list[0].keys():   # Check if we can find score or impact value. Show error if we can't.
#    for i in range(len(temp_list)): # Iterating through the list.
#        if temp_list[i]["score"] >= 70 or temp_list[i]["impact"] >= 70: # Only check for items that has score or impact greater or equal to 70.
#            if recipient_domain:    # Check if we need to filter out data based on email recipient domain supplied by -r.
#                for dns in recipient_domain:    # Iterating through recipient domain names.
#                    if dns in unicode.lower(temp_list[i]["recipient"]):    # Check if recipient domain names match.
#                        temp2_list.append(temp_list[i][keyvalue])    # Append matching data into list c.
#                    else:
#                        continue
#            else:   # If there is no need to filter out recipient domain names, go ahead to append item to list c.
#                temp2_list.append(temp_list[i][keyvalue])
#        else:
#            print "\n"
#            print "X"*80
#            print "[-]Error! Your JSON data doesn't contain score or impact that greater than 70."
#            print "[-]This script only counts for items that has score or impact greater than 70."
#            print "[-]Exiting program......"
#            print "X"*80
#            print "\n"
#            sys.exit()
#
#else:
#    print "\n"
#    print "X"*80
#    print "[-]Error! There is no 'score' nor 'impact' inside JSON data"
#    print "[-]Please check your JSON data followed by -i paramater"
#    print "[-]Exiting program......"
#    print "X"*80
#    print "\n"
#    sys.exit()

utf8encoded = [s.encode('utf8') for s in temp2_list]

topn_result = Counter(utf8encoded).most_common(topn)

try:
    with open(out_file, 'wb') as fo:
        writer = csv.writer(fo, dialect='excel', delimiter='\t')
        writer.writerow( ( keyvalue_upper, 'COUNT' ))
        writer.writerows(topn_result)
    fo.close()
except IOError:
    print "\n"
    print "X"*80
    print "[-]Error! Permission denied: '%s'" % out_file
    print "[-]Please check if you have the write permission for destination directory or file"
    print "[-]Exiting program......"
    print "X"*80
    print "\n"
    sys.exit()

print "-"*80
print "[+]Successfully exported Top-N result to '%s'" % out_file
print "-"*80