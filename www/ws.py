#! /usr/bin/python
#import cgi
import dbconn
import json
import sys
import datetime
bodyO = {'status':0,'message':'success'}
#form = cgi.FieldStorage()
stat = json.loads(sys.stdin.read())
body = json.dumps(bodyO)+str(stat)
# Insert total actives
sql = 'INSERT INTO active_stat(tst,dhcpdhn,active_count,inactive_count) VALUES (%(tst)s,%(hn)s,%(active)s,0)'
active = {'hn':stat['hn'],'tst':datetime.datetime.strptime(stat['tst'],"%Y-%m-%dT%H:%M:%S.%f"),'active':stat['stats']['actives']}
dbconn.cur.execute(sql,active)
# Insert netblocks stats
for nets in stat['stats']['ipAddress']:
  #body += str(nets)+':'+str()
  ipblock = {'hn':stat['hn'],'tst':datetime.datetime.strptime(stat['tst'],"%Y-%m-%dT%H:%M:%S.%f"),'ipblock':nets,'active':stat['stats']['ipAddress'][nets]}
  sql = 'INSERT INTO ipblock_stat(tst,dhcpdhn,ipblock,active_count,inactive_count) VALUES (%(tst)s,%(hn)s,%(ipblock)s,%(active)s,0)'
  dbconn.cur.execute(sql,ipblock)
# Insert CPE stats
for cpe in stat['stats']['hwAddress']:
  cpes = {'hn':stat['hn'],'tst':datetime.datetime.strptime(stat['tst'],"%Y-%m-%dT%H:%M:%S.%f"),'cpevendormodel':cpe,'active':stat['stats']['hwAddress'][cpe]}
  sql = 'INSERT INTO cpe_stat(tst,dhcpdhn,cpevendormodel,active_count,inactive_count) VALUES (%(tst)s,%(hn)s,%(cpevendormodel)s,%(active)s,0)'
  dbconn.cur.execute(sql,cpes)
dbconn.conn.commit()
headers = 'Content-Type: application/json; charset=utf-8\r\n'
headers += "Content-Length: "+str(len(body))+"\r\n\r\n"
sys.stdout.write(headers+body)
