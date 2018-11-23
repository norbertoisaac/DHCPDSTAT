# EMAIL body
url = "http://10.150.31.68/dhcpdstat/index.py"
mailBodyHtml = '''
<h2>DHCP server connection statistics</h2>
'''
# EMAIL attach
attachHtml = ''
attachHtmlStart = '''
<!DOCTYPE html>
<html>
  <head>
    <title>DHCPDSTAT</title>
    <style type="text/css">
      #menubar a {padding:11px 15px 11px 15px;float:left;text-decoration:none;}
      /*#menubar a:link,a:visited {color:#f1f1f1;}*/
      #menubar a:hover,a:active {background-color:#ff4800;}
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
    a.menu:hover{
      background-color:black;
    }
    a.submenu:hover{
      background-color:#efefef;
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
      <a class="menu" href="?menu=charts" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;">CHARTS</a>
      <a class="menu" href="'''+url+'''" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;">Go ONLINE</a>
      <a class="menu" href="mailto:" style="float:right;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:17px;color:#f1f1f1;border:none;">Soporte: </a>
    </div>
  </div><!-- CHARTS Sub MENU -->
    <div style="background-color:#d4d6d5;height:20px;position:fixed;top:100px;width:100%">
      <a class="submenu" href="#byserver" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:10px;color:#2d2d2d;border:none;">By DHCP server</a>
      <a class="submenu" href="#byolt" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:10px;color:#2d2d2d;border:none;">By OLT</a>
      <a class="submenu" href="#byuserseg" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:10px;color:#2d2d2d;border:none;">By user segment</a>
      <a class="submenu" href="#byipblock" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:10px;color:#2d2d2d;border:none;">By IP block</a>
      <a class="submenu" href="#bycpemac" style="float:left;display:block;padding:5px 15px 5px 15px;text-decoration:none;letter-spacing:1px;font-size:10px;color:#2d2d2d;border:none;">By CPE MAC address</a>
    </div><div style="position:fixed;top:120px;width:100%;bottom:0px;overflow-y:auto;">'''
attachEnd = '</div></body></html>'
import graph
import dbconn
import common
import base64
import os
conn,cur = dbconn.getDbConn()
# Document Start
attachHtml = attachHtmlStart
# Document images
# BY DHCP Server
servers = common.getServersNames(conn,cur)
for server in servers:
  hostname = server[0]
  # Email params
  emaiParams = common.getServerEmailParams(conn,cur,hostname)
  if emaiParams:
    # Connected clients
    attachHtml += '<h2>Server '+hostname+'</h2>'
    fname2,fname = graph.graph_actives(conn, cur, hostname, 'png')
    f = open(fname,'rb')
    attachHtml += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
    f.close()
    os.unlink(fname)
    f = open(fname2,'rb')
    attachHtml += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
    f.close()
    os.unlink(fname2)
    # DHCP events
    fname,fname2 = graph.graph_requests(conn, cur, hostname, 'png')
    f = open(fname,'rb')
    attachHtml += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
    f.close()
    os.unlink(fname)
    f = open(fname2,'rb')
    attachHtml += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
    f.close()
    os.unlink(fname2)
    # BY user segment
    usersegs = graph.getusersegments(conn,cur)
    attachHtml += '<a id="byuserseg"></a>'
    for userseg in usersegs:
      fname = graph.graph_usersegment(conn,cur,userseg[0],'png')
      i = 0
      if fname:
	f = open(fname,'rb')
	attachHtml += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
	f.close()
	os.unlink(fname)
    # BY OLT
    olts = graph.getrouternames(conn,cur)
    attachHtml += '<a id="byolt"></a>'
    for olt in olts:
      fname = graph.graph_routername(conn,cur,olt[0],'png')
      i = 0
      if fname:
	f = open(fname,'rb')
	attachHtml += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
	f.close()
	os.unlink(fname)
    # BY IPBLOCK
    ipblocks = graph.getipblocks(conn,cur)
    attachHtml += '<a id="byipblock"></a>'
    for ipblock in ipblocks:
      fname = graph.graph_ipblock(conn,cur,ipblock[0],'png')
      if fname:
	f = open(fname,'rb')
	attachHtml += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
	f.close()
	os.unlink(fname)
    # BY CPE MAC
    cpemacs = graph.getcpemac(conn,cur)
    attachHtml += '<a id="bycpemac"></a>'
    for cpemac in cpemacs:
      fname = graph.graph_cpemac(conn,cur,cpemac,'png')
      if fname:
	f = open(fname,'rb')
	attachHtml += '<img src="data:image/png;base64,'+base64.b64encode(f.read())+'" />'
	f.close()
	os.unlink(fname)
    # Document End
    attachHtml += attachEnd
    # EMAIL
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    from email.MIMEImage import MIMEImage
    # Define these once; use them twice!
    strFrom = emaiParams[0]
    strTo = emaiParams[1]
    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('mixed')
    msgRoot['X-Priority'] = '2'
    msgRoot['Subject'] = hostname+'. DHCP server report'
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    msgText = MIMEText(mailBodyHtml, 'html')
    msgRoot.attach(msgText)
    msgImage = MIMEText(attachHtml,_subtype="html")
    msgImage.add_header('Content-Disposition', 'attachment', filename='conectedPerDHCPServer.html')
    msgRoot.attach(msgImage)
    # SMTP
    # Send the email
    import smtplib
    smtp = smtplib.SMTP()
    #smtp.connect(smtp.mydomain.com)
    smtp.connect(emaiParams[2],emaiParams[3])
    smtp.sendmail(strFrom,strTo.split(','),msgRoot.as_string())
    smtp.quit()
