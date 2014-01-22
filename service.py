# -*- coding: utf-8 -*-
#! /usr/bin/env python
import win32serviceutil
import win32service
import win32event
import servicemanager
import logging
import os
import conf
from run import main as run_main

PROJECT_DIR = os.path.dirname(__file__)

logging.basicConfig(
            filename=os.path.join(PROJECT_DIR, 'export_pg.log'), 
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
 
class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "PostJSONService"
    _svc_display_name_ = "PostJSON Service"
    _svc_description_ = "PostJSON Service. For send data from PostgreSQL to WebServer"
 
    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        self.hWaitResume = win32event.CreateEvent(None, 0, 0, None)
        self.timeout = getattr(conf, 'SERVICE_TIMEOUT', 900000) #Пауза между выполнением основного цикла службы в миллисекундах
        self.resumeTimeout = 1000
        self._paused = False
 
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              (self._svc_name_, ''))
       
    def SvcPause(self):
        self.ReportServiceStatus(win32service.SERVICE_PAUSE_PENDING)
        self._paused = True
        self.ReportServiceStatus(win32service.SERVICE_PAUSED)
        servicemanager.LogInfoMsg("The %s service has paused." % (self._svc_name_, ))
   
    def SvcContinue(self):
        self.ReportServiceStatus(win32service.SERVICE_CONTINUE_PENDING)
        win32event.SetEvent(self.hWaitResume)
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogInfoMsg("The %s service has resumed." % (self._svc_name_, ))
               
 
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()  
   
    #В этом методе реализовываем нашу службу    
    def main(self):
        #Здесь выполняем необходимые действия при старте службы
        servicemanager.LogInfoMsg("Hello! I'm a Dummy Service.")
        while True:
            #Здесь должен находиться основной код сервиса
            servicemanager.LogInfoMsg("I'm still here.")
            try:
                run_main([])
            except: pass
           
            #Проверяем не поступила ли команда завершения работы службы
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            if rc == win32event.WAIT_OBJECT_0:
                #Здесь выполняем необходимые действия при остановке службы
                servicemanager.LogInfoMsg("Bye!")
                break
 
            #Здесь выполняем необходимые действия при приостановке службы
            if self._paused:
                servicemanager.LogInfoMsg("I'm paused... Keep waiting...")
            #Приостановка работы службы                
            while self._paused:
                #Проверям не поступила ли команда возобновления работы службы
                rc = win32event.WaitForSingleObject(self.hWaitResume, self.resumeTimeout)
                if rc == win32event.WAIT_OBJECT_0:
                    self._paused = False
                    #Здесь выполняем необходимые действия при возобновлении работы службы
                    servicemanager.LogInfoMsg("Yeah! Let's continue!")
                    break                  
 
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
