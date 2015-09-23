This script is used to do counting for JSON data exported from Lastline, and save it to a CSV formatted file.</p>
It intends to do Top-N for items shown in web/email events from Lastline.</p>
This script will only count items that has score/impact greater than 70.</p>

For example:<code><pre>
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
</code></pre>
From the above example, file "top_c2c_src_host.txt" will show top 10 for src_host element from file "incident_c2c_infection.json".</p>
Use M$ excel to open that Top-N txt file, copy paste to what ever application you need, my case is ppt.</p>

This script can also do counting based on certain email recpient domain names.</p>
For example, if customer has 4 domain names:</p>
abc,xyz,123,567</p>
To count data only for those 4 domain names, do the following:
<code><pre>$python count_top_n.py -i emails.json -o top10_sender.txt -k "recipient" -n 10 -r abc -r xyz -r 123 -r 567
</code></pre>
