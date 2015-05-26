This script is used to do counting for JSON data exported from Lastline, and save it to a CSV formatted file.
It intends to do Top-N for items shown in web/email events from Lastline.

There are two versions of this script:
count_top_n.py = show items that has score/impact greater than 70.
count_top_n_allscore.py = show items that has score/impact greater than 0.

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