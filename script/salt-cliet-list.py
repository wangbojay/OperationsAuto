# -*- coding: utf-8 -*-
#!/usr/bin/python
import salt.client as sc
import json
import urllib2
import os


if os.path.exists('/root/mysite/script/server_info_collect.log'):
    os.remove('/root/mysite/script/server_info_collect.log')
local = sc.LocalClient()
grains = local.cmd('*',"grains.items")
diskusage = local.cmd('*','cmd.run',["df -hl | grep '^/dev/' | sort |awk -F ' ' '{printf(\"\133\"$1\"\054\"$2\"\054\"$5\"\135\"\"\054\")}'|sed 's/,$//'"])
memoryusage = local.cmd('*','cmd.run',["free -m | sed -n '2p' | awk '{printf \"%.0f%\",($3/$2)*100}'"])


def info_commit(url):
    try: 
        return_result = urllib2.urlopen(url).read()
        file_log = open('/root/mysite/script/server_info_collect.log','a')
        file_log.write(url+return_result+"  \n")
        file_log.close()
    except:
        pass

try:
    for i in grains.keys():
        print "hostname" + ":" , grains[i]["id"]
        try:
            pj_n = grains[i]["roles"][0]
            print "project" + ":" , grains[i]["roles"][0]
        except:
            pj_n = "Empty"
        print "ipv4" + ":" ,str(grains[i]["ipv4"]).replace("'127.0.0.1', ","").replace('[','').replace(']','').replace("'","")
        print "mem_total" + ":" , str(grains[i]["mem_total"] / 1024 + 1) + "G" + "  " + memoryusage[i]
        ip = str(grains[i]["ipv4"]).replace("'127.0.0.1', ","").replace('[','').replace(']','').replace("'","")
        test_dir = (grains[i]["hwaddr_interfaces"])
        del test_dir['lo']
        server_SN = str(test_dir.values()).replace(':','').replace('[','').replace(']','').replace(',','').replace("'","").replace(" ","")
        print server_SN
        print "num_cpus" + ":" , str(grains[i]["cpu_model"]).replace(' ','-') + "X" + str(grains[i]["num_cpus"])
        print "disk_usage" + ":" , diskusage[i]
        print "osfullname" + ":" , str(grains[i]["osfullname"]).replace(' ','-')
        url = "http://192.168.0.119:8000/info_collect?server_project_name=" + pj_n + "&server_SN=" + server_SN +"&server_ip=" + ip + "&server_name_id=" + str(grains[i]["id"]).replace('-','_') + "&server_cpu=" + str(grains[i]["cpu_model"]).replace(' ','-') + "X" + str(grains[i]["num_cpus"]) + "&server_memory="+str(grains[i]["mem_total"] / 1024 + 1) + "G" + "&disk_info="+ diskusage[i] +"&server_system=" + str(grains[i]["osfullname"]).replace(' ','-') + grains[i]["osrelease"]
        info_commit(url)
        print url
except Exception,e:
    print "Exception:\n",e

client_list = local.cmd("*","grains.item",["id"])
print client_list
