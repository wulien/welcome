import threading
import subprocess
import iptc
import re
import models
import time
from time import sleep, ctime
from publicfun import log
from iptables import iptable
from dboperation import db


class PingTread(threading.Thread):

    def __init__(self, lock):
        super(PingTread, self).__init__()
        self.lock = lock

    def run(self):
        self.lock.acquire()
        offline = []
        while 1:
            log("thread is running")
            all_ip = models.OnLine.objects.all()
            for ip in all_ip:
                if not self.ping(ip.ip):
                    i = 0
                    for one_ip in offline:
                        # strLog = "one_ip = %s, ip.ip = %s" % (one_ip[0], ip.ip)
                        # log(ip.ip)
                        if one_ip[0] == ip.ip:
                            log('ip in list, ip = %s' % ip.ip)
                            time_now = time.time()
                            past_time = time_now - one_ip[1]
                            if past_time > 300:
                                # delete iptable and this ip
                                table = iptc.Table.FILTER
                                rule = iptable(table)
                                rule.delete_rule(ip)
                                stDB = db()
                                stDB.Delete_OnLine_Phone(ip)
                                offline.remove(one_ip)
                                strLog = 'remove ip:' + ip.ip
                                log(strLog)
                        else:
                            i += 1
                    if i == len(offline):
                        # add a new ip
                        one_off_line = []
                        one_off_line.append(ip.ip)
                        one_off_line.append(time.time())  # begin time
                        offline.append(one_off_line)
                        strLog = 'add a new ip = ' + ip.ip
                        log(strLog)

            # ping per 2 minutes
            sleep(120)
            log('-------------------------------------------------------------------------------------------------------------------------')
        self.lock.release()

    def ping(self, ip):
        strPing = 'ping -c 2 ' + ip
        log(strPing)
        p = subprocess.Popen([strPing],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        p.wait()
        out = p.stdout.read()
        # log(out)
        # print out
        regex = re.compile("time=\d*", re.IGNORECASE | re.MULTILINE)
        if len(regex.findall(out)) > 0:
            return True
        return False
