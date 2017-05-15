# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(default="",max_length=30,unique=True,verbose_name="名称")
    operation_user = models.ForeignKey(User,blank=True,null=True,to_field='username',verbose_name="运维人员")
    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

class Monitor_performance(models.Model):
    mg_name = models.CharField(default="",max_length=30,verbose_name="名称")
    class Meta:
        verbose_name = '监控服务器性能'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

class Server(models.Model):
    server_project_name = models.ForeignKey(Project,blank=True,null=True,to_field='name',verbose_name="项目")
    server_ip = models.CharField(max_length=30,verbose_name="IP地址")
    server_name = models.CharField(max_length=30, verbose_name="服务器名称")
    server_SN = models.CharField(max_length=20,blank=False,unique=True,verbose_name="SN")
    server_cpu = models.CharField(default="", max_length=50, verbose_name="CPU")
    server_memory = models.CharField(default="", max_length=10, verbose_name="内存")
    server_disk = models.CharField(default="", max_length=100, verbose_name="存储")
    server_system = models.CharField(max_length=30, verbose_name="操作系统")
    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.server_SN

class Server_Monitor_Data(models.Model):
    server_project_name = models.ForeignKey(Project,null=True,to_field='name',verbose_name="项目")
    server_SN = models.ForeignKey(Server,null=True,to_field='server_SN',verbose_name="识别码")
    server_ip = models.CharField(max_length=30,verbose_name="IP地址")
    server_name = models.CharField(default="",max_length=30, verbose_name="服务器名称")
    server_cpu_load = models.DecimalField(max_digits=4,decimal_places=2, verbose_name="CPU使用率")
    server_system_load = models.DecimalField(max_digits=4,decimal_places=2, verbose_name="系统负载")
    server_memory_usage = models.DecimalField(max_digits=4,decimal_places=2, verbose_name="内存使用率")
    server_swap = models.DecimalField(max_digits=4,decimal_places=2, verbose_name="SWAP使用率")
    server_disk_usage = models.CharField(default="", max_length=100, verbose_name="磁盘使用情况")
    server_iowait = models.DecimalField(max_digits=4,decimal_places=2,verbose_name="iowait")
    server_zombie = models.IntegerField(default="0", verbose_name="僵尸进程数量")
    server_net_traffic = models.CharField(default="0", max_length=100, verbose_name="网卡流量")
    server_work_time = models.CharField(max_length=20,verbose_name="工作时间")
    monitor_update_time = models.DateTimeField(blank=True,auto_now_add=True,verbose_name='更新时间')
    class Meta:
        verbose_name = '服务器监控数据'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.server_name

