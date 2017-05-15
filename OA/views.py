# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from models import *
from django.db import connection
import datetime
from django.utils import timezone
import json
# Create your views here.

def info_collect(request):
    server_project_name = str(request.GET['server_project_name'])
    server_ip = request.GET['server_ip']
    server_id_name = request.GET['server_name_id']
    server_SN = request.GET['server_SN']
    server_cpu = request.GET['server_cpu']
    server_memory = request.GET['server_memory']
    server_disk_info = request.GET['disk_info']
    server_system = request.GET['server_system']
    obj = Server.objects.filter(server_SN = server_SN)
    if len(obj) == 0:
        add_server = Server(server_ip=server_ip,server_name=server_id_name,server_SN=server_SN,server_system=server_system,server_project_name_id=server_project_name,server_cpu=server_cpu,server_memory=server_memory,server_disk=server_disk_info)
        add_server.save()
    else:
        obj = Server.objects.get(server_SN=server_SN)
        obj.server_ip = server_ip
        obj.server_SN = server_SN
        obj.server_system = server_system
        obj.server_project_name_id = server_project_name
        obj.server_cpu = server_cpu
        obj.server_memory = server_memory
        obj.server_disk = server_disk_info
        obj.save()
    return HttpResponse('Commit Success!')

@login_required()
def index(request):
    uname = request.user.first_name
    project_name  = Project.objects.exclude(name='Empty')
    online_server_count = Server.objects.exclude(server_project_name="Empty").count()
    offline_server_count = Server.objects.filter(server_project_name="Empty").count()
    online_project_count = Project.objects.exclude(name='Empty').count()
    return render(request,'index.html',locals())

@login_required()
def pj(request):
    uname = request.user.first_name
    project_name  = Project.objects.exclude(name='Empty')
    project_name_r = request.GET['projectname']
    p_id = Project.objects.all()
    for p in p_id:
        if project_name_r == p.name:
            project_name_r = p.id
            project_name_n = p.name
    server_list = Server.objects.filter(server_project_name_id=project_name_r)
    server_status = Project.objects.get(id=1)
    return render(request,'pj.html',locals())

@login_required()
def server(request):
    uname = request.user.first_name
    project_name  = Project.objects.exclude(name='Empty')
    server_status = Project.objects.get(id=1)
    server_list = Server.objects.filter(server_project_name_id=1)
    return render(request,'server.html',locals())

@login_required()
def database(request):
    uname = request.user.first_name
    project_name = Project.objects.exclude(name='Empty')
    server_status = Project.objects.get(id=1)
    server_list = Server.objects.filter(server_name__contains="database")
    return render(request,'database.html',locals())

@login_required()
def quick_task(request):
    uname = request.user.first_name
    project_name = Project.objects.exclude(name='Empty')
    server_status = Project.objects.get(id=1)
    server_list = Server.objects.filter(server_name__contains="database")
    return render(request,'quick_task.html',locals())

@login_required()
def custom_task(request):
    uname = request.user.first_name
    project_name = Project.objects.exclude(name='Empty')
    server_status = Project.objects.get(id=1)
    server_list = Server.objects.filter(server_name__contains="database")
    return render(request,'custom_task.html',locals())

def data_table(project_name,server_name,start_time,end_time):
    if end_time  == 'NO':
        monitor_time_default = Server_Monitor_Data.objects.filter(monitor_update_time__gte=start_time,server_name=server_name,server_project_name=project_name)
    else:
        monitor_time_default = Server_Monitor_Data.objects.filter(monitor_update_time__gte=start_time,monitor_update_time__lt=end_time,server_name=server_name,server_project_name=project_name)
    if len(monitor_time_default) == 0:
        return monitor_time_default
    else:
        monitor_data_list  = []
        CPU_data_list = []
        memory_data_list = []
        swap_data_list = []
        io_data_list = []
        net_data_list = []
        disk_data_list = []
        load_data_list = []
        time_list = []
        for a  in monitor_time_default:
            CPU_data_list.append(float(a.server_cpu_load ))
            memory_data_list.append(int(a.server_memory_usage*100))
            swap_data_list.append(int(a.server_swap*100))
            io_data_list.append(float(a.server_iowait))
            disk_u =a.server_disk_usage
            disk_u = disk_u.encode("utf-8")
            disk_u = str(disk_u).replace("&","'").replace("%","")
            disk_u = eval(disk_u)
            disk_data_list.append(disk_u)
            net_data_temp = a.server_net_traffic
            net_data_temp = eval(net_data_temp)
            net_data_list.append(net_data_temp)
            load_data_list.append(float(a.server_system_load))
            time_list.append(a.monitor_update_time.strftime("%H:%M"))
        monitor_data_list.append(CPU_data_list)
        monitor_data_list.append(memory_data_list)
        monitor_data_list.append(swap_data_list)
        monitor_data_list.append(io_data_list)
        monitor_data_list.append(load_data_list)
        monitor_data_list.append(time_list)
        monitor_data_list.append(project_name)
        monitor_data_list.append(server_name)
        ip  = monitor_time_default[0].server_ip
        monitor_data_list.append(ip)
        temp1=[]
        for i in disk_data_list[0]:
            a= i[0]
            temp1.append([a,[]])
        for t in range(0,len(temp1)):
            for i in disk_data_list:
                a = i[t][1]
                temp1[t][1].append(a)
        monitor_data_list.append(temp1)
        temp2=[]
        if len(net_data_list[0])/2 > 1:
            for nt in range(0,len(net_data_list[0])/2-1):
                net_name = "net" +str(nt)
                temp2.append([net_name,[],[]])
        else:
            temp2.append(["net1", [], []])
            for nt_d in net_data_list:
                temp2[0][1].append(nt_d[0])
                temp2[0][2].append(nt_d[1])
        monitor_data_list.append(temp2)
        return monitor_data_list

@login_required()
def monitor_graph(request):
    uname = request.user.first_name
    mg_list = Monitor_performance.objects.all()
    project_name = Project.objects.exclude(name='Empty')
    if "project_name" in request.GET:
        server_list = request.GET['server_name']
        server_project_name = request.GET['project_name']
        server_genre = request.GET['project_genre']
        server_genre = Monitor_performance.objects.get(mg_name=server_genre).id
        date_range1 = request.GET['time1']
        date_range2 = request.GET['time2']
        data_table_monitor = []
        a = data_table(server_project_name, server_list, date_range1 , date_range2)
        data_table_monitor.append(a)
    else:
        now = timezone.now()
        start = now - datetime.timedelta(hours=1)
        server_table = Server.objects.all()
        server_list = []
        data_table_monitor = []
        for s in server_table:
            server_list.append([s.server_name,s.server_project_name])
        for k in server_list:
             a = data_table(k[1], k[0],start, "NO")
             data_table_monitor.append(a)
    return render(request,'monitor_graph.html',locals())

def monitor_graph_select(request):
    if "project_name" in request.GET:
        server_project = request.GET["project_name"]
        server_name_list = Server.objects.filter(server_project_name_id__name__exact=server_project)
        server_list = []
        for s in server_name_list:
            d = {}
            d["server_name"] = s.server_name
            server_list.append(d)
    return HttpResponse(json.dumps(server_list),content_type="application/json")

@login_required()
def monitor_table(request):
    uname = request.user.first_name
    project_name = Project.objects.exclude(name='Empty')
    sql = "select * from OA_server_monitor_data where monitor_update_time in(select max(monitor_update_time) FROM OA_server_monitor_data GROUP BY server_name,server_project_name_id);"
    cursor2 = connection.cursor()
    cursor2.execute(sql)
    monitor_data_list = cursor2.fetchall()
    return render(request,'monitor_table.html',locals())


