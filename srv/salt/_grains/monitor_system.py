# -*- coding: utf-8 -*-
import os,sys
import re
import time
import subprocess

def system_load():
	grains = {}
	monitor_cpu = subprocess.Popen('uptime',shell=True,stdout=subprocess.PIPE).communicate()[0]
	load = monitor_cpu.split(',')[-3].split(' ')[-1]
	work_time = monitor_cpu.split(',')[0].split(' ')[-2]
	if work_time == 'up':
		work_time = monitor_cpu.split(',')[0].split(' ')[-1]
	elif work_time == "":
		work_time = monitor_cpu.split(',')[0].split(' ')[-1]
	#work_time = 0
	CPU_USAGE = subprocess.Popen('mpstat |tail -1',shell=True,stdout=subprocess.PIPE).communicate()[0]
	data = re.findall("\d+\.\d+",CPU_USAGE)
	cpu = 100 - float(data[-1])
	zombie_num = subprocess.Popen('ps -ef | grep defunct | grep -v grep | wc -l',shell=True,stdout=subprocess.PIPE).communicate()[0].replace('\n','')
	iowait = float(data[-7])
	mem_usage = subprocess.Popen("free -m |awk '{print $1,$2,$3}'", shell=True,  stdout=subprocess.PIPE).communicate()[0]
	mem_usage = re.findall("\d+",mem_usage)
	mem = float(mem_usage[1])/int(mem_usage[0])
	try:
		swap = float(mem_usage[-1])/int(mem_usage[-2])
	except:
		swap = 0
	disk_usage = subprocess.Popen("df -hl | grep '^/dev/' | sort |awk -F ' ' '{printf(\"\133\"\"\046\"$1\"\046\"\"\054\"\"\046\"$5\"\046\"\"\135\"\"\054\")}'|sed 's/,$//'",shell=True,stdout=subprocess.PIPE).communicate()[0]
	net_traffic = subprocess.Popen("/usr/local/bin/ifstat 1 1 | tail -1", shell=True,  stdout=subprocess.PIPE).communicate()[0]
	net_traffic =  re.findall("\d+\.\d+",net_traffic)
	grains['monitor_load'] = load
	grains['monitor_work_time'] = work_time
	grains['monitor_cpu'] = cpu
	grains['zombie'] = zombie_num
	grains['monitor_iowait'] = iowait
	grains['monitor_mem'] = mem
	grains['monitor_swap'] = swap
	grains['disk_usage'] = disk_usage
	grains['monitor_net_traffic'] = net_traffic
	print grains
	return grains

if __name__=='__main__':
	system_load()
