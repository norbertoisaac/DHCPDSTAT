import datetime
import colect

import sys
sys.path.insert(0, '/var/lib/dhcpdstat/conf/')
import conf
now = datetime.datetime.now()
subnets = colect.getBlocks(conf.dhcpdConf)
leases = colect.getLeases(conf.leasesDb)
stats = colect.getStats(leases,subnets)
import socket
hn = socket.gethostname()
import json
import httplib
post = json.dumps({'hn':hn,'tst':now.isoformat(),'stats':stats})
print post
headers = {'Content-Type':'text/json'}
httpConn = httplib.HTTPConnection(conf.postServerAddress,conf.postServerPort,timeout=10)
try:
  httpConn.request('POST',conf.postServerScript,post,headers)
  response = httpConn.getresponse()
  responseData = response.read()
  if not response.status == 200:
    logF = open(conf.logDir+now.strftime("error-%Y%m%d.log"),'a')
    logF.write(now.isoformat()+','+str(response.status)+','+response.reason+'\n')
    logF.close()
except:
  pass
httpConn.close()
