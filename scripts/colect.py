import datetime

def getBlocks(dhcpdPath):
  blocks = {}
  dhcpdConfF = open(dhcpdPath,'r')
  lines = dhcpdConfF.readlines()
  dhcpdConfF.close()
  for line in lines:
    if line[0:6] in 'subnet':
      ls = line.split(' ')
      blocks[ls[1]] = {'nm':ls[3],'count':0}
  return blocks

def getDateTime(dateS,timeS):
  #print dateS,timeS
  yyyy,mm,dd = dateS.split('/')
  hh,MM,ss = timeS.split(':')
  d = datetime.datetime(int(yyyy),int(mm),int(dd),int(hh),int(MM),int(ss[0:2]))
  return d

def getLeaseActive(lease):
  dtN = datetime.datetime.utcnow()
  if dtN > lease['ends']:
    return False
  else:
    return True

def getLeases(leasesPath):
  leasesF = open(leasesPath,'r')
  lines = leasesF.readlines()
  leasesF.close()
  leases = []
  for line in lines:
    if line[0:5] == 'lease':
      lease = {'ip':None,'starts':None,'ends':None,'cltt':None,'hardware':{'type':None,'address':None},'active':False}
      l,ip,p = line.split(' ')
      lease['ip'] = ip
    elif line.strip()[0:6] == 'starts':
      starts,dow,dateS,timeS = line.strip().split(' ')
      lease['starts'] = getDateTime(dateS,timeS)
    elif line.strip()[0:4] == 'ends':
      starts,dow,dateS,timeS = line.strip().split(' ')
      lease['ends'] = getDateTime(dateS,timeS)
    elif line.strip()[0:4] == 'cltt':
      starts,dow,dateS,timeS = line.strip().split(' ')
      lease['cltt'] = getDateTime(dateS,timeS)
    elif line.strip()[0:8] == 'hardware':
      hw,hwtype,hwaddress = line.strip().split(' ')
      lease['hardware']['type'] = hwtype
      lease['hardware']['address'] = hwaddress[0:-1]
    elif line[0:1] == '}':
      lease['active'] = getLeaseActive(lease)
      leases.append(lease)
  return leases

def getStats(leases,subnets):
  import ipcalc
  stats = {'actives':0,'hwAddress':{},'ipAddress':{}}
  for lease in leases:
    if lease['active']:
      # Actives
      stats['actives'] += 1
      # CPEs
      if lease['hardware']['address'][0:8] in stats['hwAddress']:
	stats['hwAddress'][lease['hardware']['address'][0:8]] += 1
      else:
	stats['hwAddress'][lease['hardware']['address'][0:8]] = 1
      # Subnets
      for subnet in subnets:
        if lease['ip'] in ipcalc.Network(subnet,subnets[subnet]['nm']):
	  if subnet in stats['ipAddress']:
	    stats['ipAddress'][subnet] += 1
	  else:
	    stats['ipAddress'][subnet] = 1
	  break
  return stats

import sys
sys.path.insert(0, '/var/lib/dhcpdstat/conf/')
import conf
now = datetime.datetime.now()
subnets = getBlocks(conf.dhcpdConf)
leases = getLeases(conf.leasesDb)
stats = getStats(leases,subnets)
import socket
hn = socket.gethostname()
post = {'hn':hn,'tst':now.isoformat(),'stats':stats}
print post
