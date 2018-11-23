#! /usr/bin/python
import cgi
import sys
import graph
import dbconn
import base64
import os
form = cgi.FieldStorage()
if 'menu' in form:
  menu = form.getvalue('menu')
else:
  menu = 'events'
body=''
# GRAPH
if menu == 'graph':
  conn,cur = dbconn.getDbConn()
  if 'byserver' in form:
    byserver=form.getvalue('byserver')
    #fname2,fname = graph.graph_actives(conn, cur, 'ddnsftth1', 'png')
    fname2,fname = graph.graph_actives(conn, cur, byserver, 'png', True)
    f = open(fname,'rb')
    #body = '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
    body = f.read()
    f.close()
    os.unlink(fname)
    f = open(fname2,'rb')
    #body += f.read()
    #body += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
    f.close()
    os.unlink(fname2)
    headers = 'Content-Type: image/png; charset=utf-8\r\n'
    headers += "Content-Length: "+str(len(body))+"\r\n\r\n"
    sys.stdout.write(headers+body)
  elif 'byolt' in form:
    byolt=form.getvalue('byolt')
    if 'attr' in form:
      attr = form.getvalue('attr')
      if attr == 'concurrent':
	fname = graph.graph_routername(conn, cur, byolt, 'png', stdout=True)
	if fname:
	  import os
	  os.unlink(fname)
      elif attr == 'dhcpdiscover':
	fname = graph.graph_routernameDhcpdiscover(conn, cur, byolt, 'png', stdout=True)
	if fname:
	  import os
	  os.unlink(fname)
      elif attr == 'dhcprequest':
	fname = graph.graph_routernameDhcprequest(conn, cur, byolt, 'png', stdout=True)
	if fname:
	  import os
	  os.unlink(fname)
  elif 'byuserseg' in form:
    userseg=form.getvalue('byuserseg')
    graph.graph_usersegment(conn, cur, userseg, 'png', stdout=True)
  elif 'byipblock' in form:
    ipblock=form.getvalue('byipblock')
    graph.graph_ipblock(conn, cur, ipblock, 'png', stdout=True)
  quit()
  

body = '''<!DOCTYPE html>
<html>
  <head>
   <meta http-equiv="refresh" content="600">
    <title>DHCPDSTAT</title>
    <link rel="shortcut icon" type="image/x-icon" href="favicon.ico" />
    <script>
      function selectsubg(){
    document.forms["formsubg"].submit();
      }
      function submitformid(id){
        var form = document.getElementById(id);
    form.submit();
      }
      function newWindow(url){
    //document.forms["formsubg"].elements["subg"].value="all";
    //document.forms["formsubg"].submit();
      window.open(url, '_blank','menubar=no,status=no,titlebar=no,width=600px');
      }
      function togleDisplay(divid){
        var div = document.getElementById(divid);
	if(div.style.display == 'none')
	{
	  div.style.display = 'block';
	}
	else
	{
	  div.style.display = 'none';
	}
      }
      window.name = '';
      console.log(window.name);
    </script>
    <style type="text/css">
      table, table.tecspec {
	border-collapse: collapse;
	font-size: 100%;
	font-family: verdana,helvetica,arial,sans-serif;
	text-align: start;
	border-spacing: 2px;
	border-color: grey;
      }
      table.reference tr:nth-child(odd) {
	background-color: #F6F4F0;
      }
      table.reference th {
          color: #ffffff;
          background-color: #555555;
          border: 1px solid #555555;
          font-size: 12px;
          padding: 3px;
          vertical-align: top;
          text-align: left;
      }
      table.reference td {
	border: 1px solid #d4d4d4;
	padding: 5px;
	padding-top: 7px;
	padding-bottom: 7px;
	vertical-align: top;
      }
      div.popupdiv {
	left: 0px;
	top: 0px;
	height: 100%;
	width: 100%;
	color: rgb(0, 0, 0);
	background-color: rgba(0, 0, 0, 0.4);
	z-index: 4;
	position: fixed;
	overflow: auto;
	padding-top: 0px;
      }
      div.insidepopup {
	padding: 0px;
	box-sizing: border-box;
	background-color: #FFF;
	position: relative;
	margin: auto;
	width: fit-content;
	width: -moz-fit-content;
	margin-top: 120px
      }
    </style>
  </head>
  <body style="margin:0;">
  <form id="formsubg" method="get" action="?" target="_top"></form>
  <div style="top:0;width:100%;height:100px;position:fixed">
    <!-- TOP NAV -->
    <div style="text-align:center;background-color:#42f44b;height:70px">
      <h style="font-size:300%;text-align:center;">DHCP server statistics</h>
    </div>
    <!-- MENU -->
    <div style="background-color:#5f5f5f;height:30px">
    <style>
    
    ul.menu {
      height: 30px
      float: left;
      display: block;
      padding: 0px 0px 0px 0px;
      text-decoration: none;
      letter-spacing: 1px;
      font-size: 17px;
      color: #f1f1f1;
      border: none;
      background-color:#5f5f5f;
    }
    a.menu {
      float: left;
      display: block;
      padding: 5px 15px 5px 15px;
      text-decoration: none;
      letter-spacing: 1px;
      font-size: 17px;
      color: #f1f1f1;
      border: none;
      background-color:#5f5f5f;
    }
    /*
    ul.ulist li {
      width:100px
      height:30px;
      float: left;
      display: block;
      padding: 5px 15px 5px 15px;
      text-decoration: none;
      letter-spacing: 1px;
      font-size: 17px;
      color: #f1f1f1;
      border: none;
      background-color:#5f5f5f;
    }*/
    a.menu:hover, option:hover{
      background-color:black;
    }
    a.submenu:hover {
      background-color:white;
    }
    #id_charts:hover div {
      display: block;
    }
    </style>
    '''
topMenu = ('events','charts','ipblocks','servers')
topMenuS = ('EVENTS','CHARTS','IP blocks','SERVERS')
for n in range(len(topMenu)):
  body += '<a class="menu" id="id_'+topMenu[n]+'" href="?menu='+topMenu[n]+'" '
  if menu==topMenu[n]:
    pass
    body += 'style="background-color:black;"'
  body += '>'+topMenuS[n]+'</a>'
body += '  <a class="menu" href="mailto:" style="float:right;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;">Soporte: </a>'
body += '</div>'
body += '</div>'
# Menu
# SERVERS
if menu == 'events':
  import common
  conn,cur = dbconn.getDbConnDict()
  body += '<div style="background-color:#d4d6d5;position:fixed;top:100px;bottom:0px;;width:100%;overflow:auto"><table class="reference notranslate"><tr><th>Raise time</th><th>Clear time</th><th>Object</th><th>Severity</th><th>Active</th><th>Alarm description</th><th>Actions</th></tr>'
  if 'ackEvent' in form:
    eventlog_id = form.getvalue('eventLogId')
    common.ackEventlog(conn,cur,eventlog_id)
    body += "<script>window.alert('The event has been acknowledged')</script>"
  events = common.getAlarms(conn,cur)
  for event in events:
    if event['clear_time']:
      clear_time = event['clear_time'].ctime()
    else:
      clear_time = ''
    if event['obj_type'] == 'server':
      objParts = common.getServerById(conn,cur,event['obj_orig_id'])
      objName = objParts['hostname']+'<br>'+objParts['remarks']
    elif event['obj_type'] == 'ipblock':
      objParts = common.getIpblockById(conn,cur,event['obj_orig_id'])
      objName = objParts['ipblock_net']+'/'+str(objParts['ipblock_prefix'])+'<br>'+objParts['others']
    else:
      objName = ''
    body += '<tr><td>'+event['raise_time'].ctime()+'</td><td>'+clear_time+'</td><td>'+event['event_obj_type']+'<br>'+objName+'</td><td>'+common.severity[event['event_severity']]+'</td><td>'+str(event['eventlog_active'])+'</td><td>'+event['event_description']+'</td><td><form method="post" action="?menu=events">'
    if event['acknowledged'] == False:
      body += '<button type="submit" name="ackEvent" value="ackevent">Ack</button>'
    body += '<input type="hidden" name="eventLogId" value="'+str(event['eventlog_id'])+'"></form></td></tr>'
  body += '</table></div>'
elif menu == 'servers':
  import common
  conn,cur = dbconn.getDbConnDict()
  if 'servers_mod' in form:
     s = {}
     s['hostname'] = form.getvalue('server_name')
     if form.getvalue('server_active') == None:
       s['active'] = False
     else:
       s['active'] = True
     if form.getvalue('server_report') == None:
       s['report'] = False
     else:
       s['report'] = True
     if form.getvalue('server_alarms') == None:
       s['alarms'] = False
     else:
       s['alarms'] = True
     s['emailfrom'] = form.getvalue('server_emailfrom')
     s['eventrcp'] = form.getvalue('server_eventrcp')
     s['emailrcp'] = form.getvalue('server_emailrcp')
     s['smtpserveraddress'] = form.getvalue('server_smtpaddress')
     s['smtpserverport'] = int(form.getvalue('server_smtpport'))
     s['remarks'] = form.getvalue('server_remarks')
     common.modServers(conn,cur,s)
  body += '<div style="background-color:#d4d6d5;position:fixed;top:100px;bottom:0px;;width:100%;overflow:auto"><table class="reference notranslate"><tr><th>Server name</th><th>Active</th><th>Report</th><th>Events notification</th><th>Email from</th><th>Report recipients</th><th>Event recipients</th><th>SMTP server address</th><th>SMTP server port</th><th>Remarks</th><th>Actions</th></tr>'
  servers = common.getServers(conn,cur)
  for server in servers:
    if server['emailrcp'] == None:
      server['emailrcp'] = ''
    if server['eventrcp'] == None:
      server['eventrcp'] = ''
    if server['remarks'] == None:
      server['remarks'] = ''
    body += '<tr><form method="post" action="index.py?menu=servers"><input type="hidden" name="server_name" value="'+server['hostname']+'"><td>'+server['hostname']+'</td><td><input type="checkbox" name="server_active" '
    if server['active']:
      body += 'checked'
    body += '></td><td><input type="checkbox" name="server_report" '
    if server['report']:
      body += 'checked'
    body += '></td><td><input type="checkbox" name="server_alarms" '
    if server['alarms']:
      body += 'checked'
    body += '></td><td><input type="email" name="server_emailfrom" value="'+server['emailfrom']+'" required></td><td><input type="text" name="server_emailrcp" value="'+server['emailrcp']+'"></td><td><input type="text" name="server_eventrcp" value="'+server['eventrcp']+'"></td><td><input style="width:100px" type="text" name="server_smtpaddress" value="'+server['smtpserveraddress']+'" required></td><td><input style="width:50px" type="number" name="server_smtpport" value="'+str(server['smtpserverport'])+'" required></td><td><input type="text" name="server_remarks" value="'+server['remarks']+'"></td><td><input type="submit" name="servers_mod" value="Save"></td></form></tr>'
    pass
  body += '</table></div>'
# IP blocks
elif menu == 'ipblocks':
  import common
  conn,cur = dbconn.getDbConnDict()
  if 'modipblock' in form:
    ipblocparams = {}
    ipblocparams['id'] = form.getvalue('id')
    ipblocparams['vlanname'] = form.getvalue('vlanname')
    ipblocparams['routername'] = form.getvalue('routername')
    ipblocparams['usersegment'] = form.getvalue('usersegment')
    ipblocparams['others'] = form.getvalue('others')
    common.modIpblock(conn,cur,ipblocparams)
    body += str(ipblocparams)
  common.updateIpblocks(conn,cur)
  body += '<div style="background-color:#d4d6d5;position:fixed;top:100px;bottom:0px;;width:100%;overflow:auto"><table class="reference notranslate"><tr><th>Network address</th><th>Prefix</th><th>Max leases</th><th>VLAN name</th><th>NAS name</th><th>User segment</th><th>Remarks</th><th>Actions</th></tr>'
  ipblocks = common.getIpblocks(conn,cur)
  for ipblock in ipblocks:
    if ipblock['vlanname'] == None:
      ipblock['vlanname'] = ''
    if ipblock['routername'] == None:
      ipblock['routername'] = ''
    if ipblock['usersegment'] == None:
      ipblock['usersegment'] = ''
    if ipblock['others'] == None:
      ipblock['others'] = ''
    if ipblock['ipblock_maxleases'] == None:
      ipblock['ipblock_maxleases'] = ''
    body += '<tr><form method="post" action="index.py?menu=ipblocks"><input type="hidden" name="id" value="'+str(ipblock['id'])+'"><td>'+ipblock['ipblock_net']+'</td><td>'+str(ipblock['ipblock_prefix'])+'</td><td>'+str(ipblock['ipblock_maxleases'])+'</td><td><input type="text" name="vlanname" value="'+str(ipblock['vlanname'])+'"></td><td><input type="text" name="routername" value="'+str(ipblock['routername'])+'"></td><td><input type="text" name="usersegment" value="'+str(ipblock['usersegment'])+'"></td><td><input type="text" name="others" value="'+str(ipblock['others'])+'"></td><td><input type="submit" name="modipblock" value="Save"></td></form></tr>'
    #body += str(ipblock)+'<br>'
  body += '</table></div>'
# CHARTS
elif menu == 'charts':
  conn,cur = dbconn.getDbConn()
  body += '''<!-- CHARTS Sub MENU -->
    <div style="background-color:#d4d6d5;height:20px;position:fixed;top:100px;width:100%">
      <a class="submenu" href="?menu=charts&submenu=byserver" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:10px;color:#2d2d2d;border:none;">By DHCP server</a>
      <a class="submenu" href="?menu=charts&submenu=byolt" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:10px;color:#2d2d2d;border:none;">By OLT</a>
      <a class="submenu" href="?menu=charts&submenu=byuserseg" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:10px;color:#2d2d2d;border:none;">By user segment</a>
      <a class="submenu" href="?menu=charts&submenu=byipblock" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:10px;color:#2d2d2d;border:none;">By IP block</a>
      <a class="submenu" href="?menu=charts&submenu=bycpemac" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:10px;color:#2d2d2d;border:none;">By CPE MAC address</a>
      <!-- <select style="height:100%;background-color:gray;" form="formsubg" name="menu" onchange="selectsubg()">
        <option >Charts</option>
        <option value="views">Views</option>
        <option value="sqltpl">SQL templates</option>
        <option value="counters">Counters</option>
      </select>-->
    </div>'''
  body += '<div style="position:fixed;top:120px;width:100%;bottom:0px;overflow-y:auto;">'
  if 'submenu' in form:
    submenu = form.getvalue('submenu')
  else:
    submenu = 'byserver'
  if submenu=='byserver':
    import common
    servers = common.getServersNames(conn,cur)
    for server in servers:
      hostname = server[0]
      body += '<h2>Server '+hostname+'</h2>'
      # Connected client
      fname2,fname = graph.graph_actives(conn, cur, hostname, 'png')
      f = open(fname,'rb')
      body += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
      f.close()
      os.unlink(fname)
      f = open(fname2,'rb')
      body += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
      f.close()
      os.unlink(fname2)
      # DHCP events
      fname,fname2 = graph.graph_requests(conn, cur, hostname, 'png')
      f = open(fname,'rb')
      body += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
      f.close()
      os.unlink(fname)
      f = open(fname2,'rb')
      body += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
      f.close()
      os.unlink(fname2)
  if submenu=='byipblock':
    ipblocks = graph.getipblocks(conn,cur)
    for ipblock in ipblocks:
      if ipblock[0]:
	body += '<img src="/dhcpdstat/index.py?menu=graph&byipblock='+str(ipblock[0])+'" />'
      else:
	body += '<img src="/dhcpdstat/index.py?menu=graph&byipblock=" />'
      #fname = graph.graph_ipblock(conn,cur,ipblock,'png')
      #if fname:
      #  f = open(fname,'rb')
      #  body += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
      #  f.close()
  if submenu=='bycpemac':
    cpemacs = graph.getcpemac(conn,cur)
    for cpemac in cpemacs:
      fname = graph.graph_cpemac(conn,cur,cpemac,'png')
      if fname:
	f = open(fname,'rb')
	body += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
	f.close()
  if submenu=='byolt':
    olts = graph.getrouternames(conn,cur)
    for olt in olts:
      if olt[0]:
	body += '<img src="/dhcpdstat/index.py?menu=graph&attr=concurrent&byolt='+str(olt[0])+'" />'
	body += '<img src="/dhcpdstat/index.py?menu=graph&attr=dhcpdiscover&byolt='+str(olt[0])+'" />'
	body += '<img src="/dhcpdstat/index.py?menu=graph&attr=dhcprequest&byolt='+str(olt[0])+'" />'
      else:
	body += '<img src="/dhcpdstat/index.py?menu=graph&attr=concurrent&byolt=Unknown" />'
	body += '<img src="/dhcpdstat/index.py?menu=graph&attr=dhcpdiscover&byolt=Unknown" />'
	body += '<img src="/dhcpdstat/index.py?menu=graph&attr=dhcprequest&byolt=Unknown" />'
  if submenu=='byuserseg':
    usersegs = graph.getusersegments(conn,cur)
    for userseg in usersegs:
      body += '<img src="/dhcpdstat/index.py?menu=graph&byuserseg='+userseg[0]+'" />'
  body += '</div>'
body += '</body></html>'
headers = 'Content-Type: text/html; charset=utf-8\r\n'
headers += "Content-Length: "+str(len(body))+"\r\n\r\n"
sys.stdout.write(headers+body)
