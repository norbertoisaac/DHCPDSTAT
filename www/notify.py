import listenDbChannel
import smtplib
import common
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

def sendEmail(emailFrom,emailTo,body):
  host = '10.129.5.179'
  port = 25
  smtp = smtplib.SMTP()
  smtp.connect(host,port)
  smtp.sendmail(emailFrom,emailTo.split(','),body)
  smtp.quit()
  return

def callbackProcessFunction(conn,cur,payload):
  #global emailFrom
  #global emailTo
  sendNotify = False
  sql = "SELECT event_log.active as event_log_active,event_log.id AS event_log_id,event_log.*,events.*,objects.* FROM event_log JOIN events ON events.id=event_log.event_id JOIN objects ON objects.id=event_log.obj_id  WHERE notified='f'"
  cur.execute(sql)
  event_logs = cur.fetchall()
  for event_log in event_logs:
    #print event_log
    mailBodyHtml = '<html><head></head><body><style>table, table.tecspec { border-collapse: collapse; font-size: 100%; font-family: verdana,helvetica,arial,sans-serif; text-align: start; border-spacing: 2px; border-color: grey; } table.reference tr:nth-child(odd) { background-color: #F6F4F0; } table.reference th { color: #ffffff; background-color: #555555; border: 1px solid #555555; font-size: 12px; padding: 3px; vertical-align: top; text-align: left; } table.reference td { border: 1px solid #d4d4d4; padding: 5px; padding-top: 7px; padding-bottom: 7px; vertical-align: top; }</style>'
    # Severity
    event_severity = common.severity[event_log['event_severity']]
    if event_log['event_log_active']:
      event_state = event_severity
    else:
      event_state = 'Recovery'
    objName = ''
    # Raise/Clear time
    raise_time = event_log['raise_time'].ctime()
    if event_log['clear_time']:
      clear_time = event_log['clear_time'].ctime()
    else:
      clear_time = ''
    if event_log['acknowledged'] == False:
      ackStr = '<br>Acknowledge the alarm on http://'+common.uiserver['ip']+':'+str(common.uiserver['port'])+common.uiserver['script']+'?menu=events&ackEvent=True&eventLogId='+str(event_log['event_log_id'])
    else:
      ackStr = ''
    # SERVER
    if event_log['event_obj_type'] == 'server':
      server = common.getServerById(conn,cur,event_log['obj_orig_id'])
      if server:
	if server['alarms'] and server['eventrcp']:
          sendNotify = True
        objName = server['hostname']
	emailFrom = server['emailfrom']
	emailTo = server['eventrcp']
      mailBodyHtml += 'Server name: '+str(objName)+'<br>Description: '+str(server['remarks'])+'<br>Alarm description: '+event_log['event_description']+'<br>Severity: '+event_severity+'<br>Raise time: '+raise_time+'<br>Recovery time: '+clear_time+ackStr+'<br>Last collected data:<br><table class="reference"><tr><th>Time</th><th>Active clients</th><th>Inactive clients</th><th>DHCPDISCOVER</th><th>DHCPOFFER</th><th>DHCPREQUEST</th><th>DHCPACK</th></tr>'
      lastDatas = common.getServerLastHourStat(conn,cur,server['hostname'])
      for lastData in lastDatas:
        mailBodyHtml += '<tr><td>'+lastData['tst'].ctime()+'</td><td>'+str(lastData['active_count'])+'</td><td>'+str(lastData['inactive_count'])+'</td><td>'+str(lastData['dhcpdiscover'])+'</td><td>'+str(lastData['dhcpoffer'])+'</td><td>'+str(lastData['dhcprequest'])+'</td><td>'+str(lastData['dhcpack'])+'</td></tr>'
      mailBodyHtml += '</table>'
    # IP BLOCK
    elif event_log['event_obj_type'] == 'ipblock':
      ipblock = common.getIpblockById(conn,cur,event_log['obj_orig_id'])
      serverObj = common.getObjById(conn,cur,event_log['obj_parent'])
      server = None
      if serverObj:
        server = common.getServerById(conn,cur,serverObj['obj_orig_id'])
      if server['alarms'] and server['eventrcp']:
	sendNotify = True
      emailFrom = server['emailfrom']
      emailTo = server['eventrcp']
      if ipblock:
        objName = ipblock['ipblock_net']+'/'+str(ipblock['ipblock_prefix'])
      mailBodyHtml += 'IP block: '+str(objName)+'<br>Description: '+str(ipblock['others'])+'<br>Alarm description: '+event_log['event_description']+'<br>Severity: '+event_severity+'<br>Raise time: '+raise_time+'<br>Recovery time: '+clear_time+'<br>Last collected data:<br><table class="reference"><tr><th>Time</th><th>Active clients</th><th>Inactive clients</th><th>DHCPDISCOVER</th><th>DHCPOFFER</th><th>DHCPREQUEST</th><th>DHCPACK</th></tr>'
      lastDatas = common.getIPblockLastHourStat(conn,cur,ipblock['ipblock_net'])
      for lastData in lastDatas:
        mailBodyHtml += '<tr><td>'+lastData['tst'].ctime()+'</td><td>'+str(lastData['active_count'])+'</td><td>'+str(lastData['inactive_count'])+'</td><td>'+str(lastData['dhcpdiscover'])+'</td><td>'+str(lastData['dhcpoffer'])+'</td><td>'+str(lastData['dhcprequest'])+'</td><td>'+str(lastData['dhcpack'])+'</td></tr>'
      mailBodyHtml += '</table>'
    mailBodyHtml += '</body></html>'
    msgRoot = MIMEMultipart('mixed')
    msgRoot['X-Priority'] = '2'
    msgRoot['Subject'] = event_state+' '+event_log['event_obj_type']+' '+str(objName)+'. '+event_log['event_description']
    print time.ctime(),event_log['event_log_active'],msgRoot['Subject']
    msgRoot['From'] = emailFrom
    msgRoot['To'] = emailTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    msgText = MIMEText(mailBodyHtml, 'html')
    msgRoot.attach(msgText)
    #msgImage = MIMEText(attachHtml,_subtype="html")
    #msgImage.add_header('Content-Disposition', 'attachment', filename='conectedPerDHCPServer.html')
    #msgRoot.attach(msgImage)
    if sendNotify:
      sendEmail(emailFrom,emailTo,msgRoot.as_string())
    else:
      print 'Not notify this event'
    # Notified
    sql =  "UPDATE event_log SET notified='t' WHERE id="+str(event_log['event_log_id'])
    cur.execute(sql)
  conn.commit()
  return

import dbconn
conn,cur = dbconn.getDbConnDict()
callbackProcessFunction(conn,cur,'')
conn.close()
listenDbChannel.notifyMain('send_notify',callbackProcessFunction)
