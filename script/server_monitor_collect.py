#!/usr/bin/python
import salt.client as sc
import MySQLdb

local = sc.LocalClient()
grains = local.cmd('*',"grains.items")
monitor_data = local.cmd('*','cmd.run',["python /var/cache/salt/minion/extmods/grains/monitor_system.py"])

try:
	for i in  monitor_data.keys():
		server_monitor_data = eval(monitor_data[i])
		ip_s = str(grains[i]["ipv4"]).replace("'127.0.0.1', ","").replace('[','').replace(']','').replace("'","")
		try:
			pj_n = grains[i]["roles"][0]
		except:
			pj_n = "Empty"
		monitor_name_s = str(grains[i]["id"]).replace('-','_')
		test_dir = (grains[i]["hwaddr_interfaces"])
		del test_dir['lo']
		server_SN = str(test_dir.values()).replace(':', '').replace('[', '').replace(']', '').replace(',', '').replace("'", "").replace(" ", "")
		monitor_load_s = server_monitor_data['monitor_load']
		monitor_work_time_s = server_monitor_data['monitor_work_time']
		monitor_cpu_s = server_monitor_data['monitor_cpu']
		monitor_cpu_s = float('%.2f'% monitor_cpu_s)
		zombie_s = server_monitor_data['zombie']
		monitor_iowait_s = server_monitor_data['monitor_iowait']
		monitor_mem_s = server_monitor_data['monitor_mem']
		monitor_mem_s = float('%.2f'% monitor_mem_s)
		monitor_swap_s = server_monitor_data['monitor_swap']
		disk_usage_s = server_monitor_data['disk_usage']
		monitor_net_traffic_s = str(server_monitor_data['monitor_net_traffic']).replace("'", "")
		sql = "INSERT INTO OA_server_monitor_data VALUES(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',NOW(),'%s','%s')" %(ip_s,monitor_name_s,monitor_cpu_s,monitor_load_s,monitor_mem_s,monitor_swap_s,disk_usage_s,monitor_iowait_s,zombie_s,monitor_net_traffic_s,monitor_work_time_s,server_SN,pj_n)
		conn=MySQLdb.connect(host='192.168.0.119',user='root',passwd='Xianhai@123',db='OA',port=3306,charset='utf8')
		cur=conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
except Exception,e:
	print "Exception:\n",e
