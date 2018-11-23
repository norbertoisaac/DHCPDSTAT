severity = {0:'Emergency',1:'Alert',2:'Critical',3:'Error',4:'Warning',5:'Notice',6:'Informational',7:'Debug'}
uiserver = {'ip':'10.1.1.8','port':80,'script':'/dhcpdstat/index.py'}

def updateIpblocks(conn,cur):
  sql = "INSERT INTO ipblock(ipblock_net,ipblock_prefix,ipblock_maxleases) SELECT ipblock,ipblock_prefix,ipblock_maxleases FROM ipblock_stat WHERE tst>=(CURRENT_TIMESTAMP - interval '10 min') AND (ipblock,ipblock_prefix,ipblock_maxleases) NOT IN (SELECT ipblock_net,ipblock_prefix,ipblock_maxleases FROM ipblock) GROUP BY ipblock,ipblock_prefix,ipblock_maxleases;"
  cur.execute(sql)
  conn.commit()
  return

def getIpblocks(conn,cur):
  ipblocks = None
  sql = 'SELECT id,ipblock_net,ipblock_prefix,ipblock_maxleases,usersegment,att,userlocation,routername,vlanname,others FROM ipblock ORDER BY ipblock_net;'
  cur.execute(sql)
  ipblocks = cur.fetchall()
  return ipblocks

def modIpblock(conn,cur,ipblocparams):
  sql = "UPDATE ipblock SET (usersegment,routername,vlanname,others) = (%(usersegment)s,%(routername)s,%(vlanname)s,%(others)s) WHERE id=%(id)s"
  cur.execute(sql,ipblocparams)
  conn.commit()
  return

def getServers(conn,cur):
  sql = "SELECT * FROM servers ORDER by hostname"
  cur.execute(sql)
  servers = cur.fetchall()
  return servers

def getServersNames(conn,cur):
  sql = "SELECT hostname FROM servers ORDER by hostname"
  cur.execute(sql)
  servers = cur.fetchall()
  return servers

def modServers(conn,cur,server):
  sql = "UPDATE servers SET (active,report,alarms,emailfrom,emailrcp,eventrcp,smtpserveraddress,smtpserverport,remarks) = (%(active)s,%(report)s,%(alarms)s,%(emailfrom)s,%(emailrcp)s,%(eventrcp)s,%(smtpserveraddress)s,%(smtpserverport)s,%(remarks)s) WHERE hostname=%(hostname)s"
  cur.execute(sql,server)
  conn.commit()
  return 

def getServerEmailParams(conn,cur,server):
  sql = "SELECT emailfrom,emailrcp,smtpserveraddress,smtpserverport FROM servers WHERE active='t' AND report='t' AND hostname='"+server+"'"
  cur.execute(sql)
  servers = cur.fetchall()
  if cur.rowcount:
    return servers[0]
  else:
    return None

def getServerById(conn,cur,objId):
  sql = "SELECT * FROM servers WHERE id="+str(objId)
  cur.execute(sql)
  server = None
  if cur.rowcount:
    server = cur.fetchone()
  return server

def getIpblockById(conn,cur,objId):
  sql = "SELECT * FROM ipblock WHERE id="+str(objId)
  cur.execute(sql)
  ipblock = None
  if cur.rowcount:
    ipblock = cur.fetchone()
  return ipblock

def getObjById(conn,cur,objId):
  sql = "SELECT * FROM objects WHERE id="+str(objId)
  cur.execute(sql)
  obj = None
  if cur.rowcount:
    obj = cur.fetchone()
  return obj

def getServerLastHourStat(conn,cur,dhcpdhn):
  lastData = []
  sql = "SELECT * FROM active_stat WHERE dhcpdhn='"+dhcpdhn+"' AND tst >= (CURRENT_TIMESTAMP - interval '1 hour') ORDER BY tst DESC"
  cur.execute(sql)
  lastData = cur.fetchall()
  return lastData

def getIPblockLastHourStat(conn,cur,ipblock):
  lastData = []
  sql = "SELECT * FROM ipblock_stat WHERE ipblock='"+ipblock+"' AND tst >= (CURRENT_TIMESTAMP - interval '1 hour') ORDER BY tst DESC"
  cur.execute(sql)
  lastData = cur.fetchall()
  return lastData

def getAlarms(conn,cur,count=20):
  alarms = []
  sql = "SELECT event_log.*,event_log.id AS eventlog_id,event_log.active AS eventlog_active,events.*,objects.* FROM event_log JOIN events ON events.id=event_log.event_id JOIN objects ON objects.id=event_log.obj_id ORDER BY raise_time DESC LIMIT "+str(count)
  cur.execute(sql)
  if cur.rowcount:
    alarms = cur.fetchall()
  return alarms

def ackEventlog(conn,cur,eventlog_id):
  sql = "UPDATE event_log SET acknowledged='t' WHERE id="+str(eventlog_id)
  cur.execute(sql)
  conn.commit()
  return
