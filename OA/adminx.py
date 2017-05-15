#coding:utf-8
from OA.models import *
import xadmin as admin
#Register your models here.
class Project_list(object):
    list_display = ('name','operation_user')

class Server_list(object):
    list_display = ('server_project_name','server_ip','server_name','server_SN','server_cpu','server_memory','server_disk','server_system')
    search_fields = ('server_ip',)

class Server_monitor_list(object):
    list_display = ('server_project_name','server_SN','server_ip','server_name','server_cpu_load','server_system_load','server_memory_usage','server_swap','server_disk_usage','server_iowait','server_zombie','server_net_traffic','server_work_time','monitor_update_time')
    search_fields = ('server_ip','server_name','server_project_name')


admin.site.register(Project,Project_list)
admin.site.register(Server,Server_list)
admin.site.register(Server_Monitor_Data,Server_monitor_list)