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
except:
  pass
httpConn.close()
