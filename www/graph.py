import tempfile
import os
import sys
from pychart import *
theme.use_color = True
theme.reinitialize()
body = ''
altura = 250
alturaAcum = 0

def format_data_label(x,y):
  global body
  res = ''
  if x.minute == 0 :
    res = '/C/15/a90{}'+str(y)
  return res

def format_tic_interval(tst):
  global body
  tstList = []
  if tst.minute==0 and tst.hour==0:
    tst = "/a90{}"+tst.strftime('%Y-%m-%d')+' '
  elif tst.minute==0:
    tst = "/a90{}"+str(tst.hour)+' : '+str(tst.minute).zfill(2)+' '
  else:
    tst = ''
  return tst

def getusersegments(conn,cur):
  sql = 'SELECT usersegment FROM ipblock GROUP BY usersegment ORDER BY usersegment;'
  cur.execute(sql)
  conn.commit()
  ipblocks = cur.fetchall()
  return ipblocks

def graph_usersegment(conn, cur, userseg, fileFormat, stdout=False):
  sql = "SELECT tst,sum(active_count)::integer FROM ipblock_stat WHERE ipblock IN (SELECT ipblock_net FROM ipblock WHERE usersegment='"+userseg+"') AND tst > (CURRENT_TIMESTAMP - interval '24 hours') GROUP BY tst ORDER BY tst ASC;"
  cur.execute(sql)
  conn.commit()
  dataSerie = cur.fetchall()
  if len(dataSerie) == 0:
    import datetime
    dataSerie = ((datetime.datetime.now(),0),)
  if stdout:
    import sys
    fname = None
    can = canvas.init(fname=None,format=fileFormat)
    headers = 'Content-Type: image/png; charset=utf-8\r\n\r\n'
    sys.stdout.write(headers)
  else:
    f, fname = tempfile.mkstemp()
    can = canvas.init(fname,format=fileFormat)
  maxS = ('',0)
  for t in dataSerie:
    if t[1] > maxS[1]:
      maxS = t
  can.show(0, 150, "/25/H"+str('User segment: '+userseg))
  #l = legend.T(loc=(104,10),nr_rows=1)
  ar = area.T(legend = None,
	      size = (360,140),
	      x_coord = category_coord.T(dataSerie, 0),
	      #y_range = (0, maxS[1]+maxS[1]/4),
	      y_range = (0, None),
	      y_grid_interval = maxS[1]/5,
	      x_axis = axis.X(label = "/15Time", format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Leases".decode('utf8')))
  plot1 = line_plot.T(data = dataSerie, ycol=1, line_style = line_style.T(color=color.green,width=4.0),label=" /15Current", data_label_format = format_data_label, data_label_offset = (0,3))
  ar.add_plot(plot1)
  ar.draw(can)
  can.close()
  if stdout==False:
    os.close(f)
  return fname

def getrouternames(conn,cur):
  sql = 'SELECT routername FROM ipblock GROUP BY routername ORDER BY routername;'
  cur.execute(sql)
  conn.commit()
  ipblocks = cur.fetchall()
  return ipblocks

def graph_routername(conn, cur, routername, fileFormat, stdout=False):
  body = ''
  if not routername=='Unknown':
    sql = "SELECT tst,sum(active_count)::integer FROM ipblock_stat WHERE ipblock IN (SELECT ipblock_net FROM ipblock WHERE routername='"+routername+"') AND tst > (CURRENT_TIMESTAMP - interval '24 hours') GROUP BY tst ORDER BY tst ASC;"
  else:
    sql = "SELECT tst,sum(active_count)::integer FROM ipblock_stat WHERE ipblock IN (SELECT ipblock_net FROM ipblock WHERE routername IS NULL) AND tst > (CURRENT_TIMESTAMP - interval '24 hours') GROUP BY tst ORDER BY tst ASC;"
  cur.execute(sql)
  conn.commit()
  dataSerie = cur.fetchall()
  if len(dataSerie) == 0:
    if stdout==False:
      return None
    import datetime
    dataSerie = ((datetime.datetime.now(),0),)
    #return None

  if stdout:
    fname=None
    import sys
    headers = 'Content-Type: image/png; charset=utf-8\r\n\r\n'
    sys.stdout.write(headers)
    can = canvas.init(fname=None,format=fileFormat)
  else:
    f, fname = tempfile.mkstemp()
    can = canvas.init(fname,format=fileFormat)
  maxS = ('',0)
  for t in dataSerie:
    if t[1] > maxS[1]:
      maxS = t
  can.show(0, 150, "/25/H"+str('OLT: '+routername)+' /15Actual:'+str(t[1]))
  l = legend.T(loc=(104,10),nr_rows=1)
  ar = area.T(legend = l,
	      size = (360,140),
	      x_coord = category_coord.T(dataSerie, 0),
	      #y_range = (0, maxS[1]+maxS[1]/4),
	      y_range = (0, None),
	      y_grid_interval = maxS[1]/5,
	      x_axis = axis.X(label = "/15Time", format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Leases".decode('utf8')))
  plot1 = line_plot.T(data = dataSerie, ycol=1, line_style = line_style.T(color=color.green,width=4.0),label=" /15Current", data_label_format = format_data_label, data_label_offset = (0,20))
  ar.add_plot(plot1)
  ar.draw(can)
  can.close()
  if stdout==False:
    os.close(f)
  return fname

def graph_routernameDhcprequest(conn, cur, routername, fileFormat, stdout=False):
  body = ''
  if not routername=='Unknown':
    sql = "SELECT tst,sum(dhcprequest)::integer,sum(dhcpack)::integer FROM ipblock_stat WHERE ipblock IN (SELECT ipblock_net FROM ipblock WHERE routername='"+routername+"') AND tst > (CURRENT_TIMESTAMP - interval '24 hours') GROUP BY tst ORDER BY tst ASC;"
  else:
    sql = "SELECT tst,sum(dhcprequest)::integer,sum(dhcpack)::integer FROM ipblock_stat WHERE ipblock IN (SELECT ipblock_net FROM ipblock WHERE routername IS NULL) AND tst > (CURRENT_TIMESTAMP - interval '24 hours') GROUP BY tst ORDER BY tst ASC;"
  cur.execute(sql)
  conn.commit()
  dataSerie = cur.fetchall()
  if len(dataSerie) == 0:
    if stdout==False:
      return None
    import datetime
    dataSerie = ((datetime.datetime.now(),0),)
    #return None

  if stdout:
    fname=None
    import sys
    headers = 'Content-Type: image/png; charset=utf-8\r\n\r\n'
    sys.stdout.write(headers)
    can = canvas.init(fname=None,format=fileFormat)
  else:
    f, fname = tempfile.mkstemp()
    can = canvas.init(fname,format=fileFormat)
  maxS = ('',0)
  for t in dataSerie:
    if t[1] > maxS[1]:
      maxS = t
  can.show(0, 150, "/25/H"+str('OLT: '+routername)+' /15Actual:'+str(t[1]))
  l = legend.T(loc=(104,10),nr_rows=2)
  ar = area.T(legend = l,
	      size = (360,140),
	      x_coord = category_coord.T(dataSerie, 0),
	      #y_range = (0, maxS[1]+maxS[1]/4),
	      y_range = (0, None),
	      y_grid_interval = maxS[1]/5,
	      x_axis = axis.X(label = "/15Time", format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Times".decode('utf8')))
  plot1 = line_plot.T(data = dataSerie, ycol=1, line_style = line_style.T(color=color.green,width=4.0),label=" /15DHCPREQUEST", data_label_format = format_data_label, data_label_offset = (0,20))
  plot2 = line_plot.T(data = dataSerie, ycol=2, line_style = line_style.T(color=color.blue,width=4.0),label=" /15DHCPACK", data_label_format = format_data_label, data_label_offset = (0,20))
  ar.add_plot(plot1)
  ar.add_plot(plot2)
  ar.draw(can)
  can.close()
  if stdout==False:
    os.close(f)
  return fname

def graph_routernameDhcpdiscover(conn, cur, routername, fileFormat, stdout=False):
  body = ''
  if not routername=='Unknown':
    sql = "SELECT tst,sum(dhcpdiscover)::integer,sum(dhcpoffer)::integer FROM ipblock_stat WHERE ipblock IN (SELECT ipblock_net FROM ipblock WHERE routername='"+routername+"') AND tst > (CURRENT_TIMESTAMP - interval '24 hours') GROUP BY tst ORDER BY tst ASC;"
  else:
    sql = "SELECT tst,sum(dhcpdiscover)::integer,sum(dhcpoffer)::integer FROM ipblock_stat WHERE ipblock IN (SELECT ipblock_net FROM ipblock WHERE routername IS NULL) AND tst > (CURRENT_TIMESTAMP - interval '24 hours') GROUP BY tst ORDER BY tst ASC;"
  cur.execute(sql)
  conn.commit()
  dataSerie = cur.fetchall()
  if len(dataSerie) == 0:
    if stdout==False:
      return None
    import datetime
    dataSerie = ((datetime.datetime.now(),0),)
    #return None

  if stdout:
    fname=None
    import sys
    headers = 'Content-Type: image/png; charset=utf-8\r\n\r\n'
    sys.stdout.write(headers)
    can = canvas.init(fname=None,format=fileFormat)
  else:
    f, fname = tempfile.mkstemp()
    can = canvas.init(fname,format=fileFormat)
  maxS = ('',0)
  for t in dataSerie:
    if t[1] > maxS[1]:
      maxS = t
  can.show(0, 150, "/25/H"+str('OLT: '+routername)+' /15Actual:'+str(t[1]))
  l = legend.T(loc=(104,10),nr_rows=2)
  ar = area.T(legend = l,
	      size = (360,140),
	      x_coord = category_coord.T(dataSerie, 0),
	      y_range = (0, None),
	      y_grid_interval = maxS[1]/5,
	      x_axis = axis.X(label = "/15Time", format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Times".decode('utf8')))
  plot1 = line_plot.T(data = dataSerie, ycol=1, line_style = line_style.T(color=color.green,width=4.0),label=" /15DHCPDISCOVER", data_label_format = format_data_label, data_label_offset = (0,20))
  plot2 = line_plot.T(data = dataSerie, ycol=2, line_style = line_style.T(color=color.blue,width=4.0),label=" /15DHCPOFFER", data_label_format = format_data_label, data_label_offset = (0,20))
  ar.add_plot(plot1)
  ar.add_plot(plot2)
  ar.draw(can)
  can.close()
  if stdout==False:
    os.close(f)
  return fname

def getcpemac(conn,cur):
  sql = 'SELECT mac_prefix,vendor_name,model_name,release,eol,eos FROM cpe_mac ORDER BY mac_prefix;'
  cur.execute(sql)
  conn.commit()
  ipblocks = cur.fetchall()
  return ipblocks

def graph_cpemac(conn, cur, cpemac, fileFormat, stdout=False):
  global body
  global alturaAcum
  body = ''
  sql = "SELECT tst,active_count FROM cpe_stat WHERE cpevendormodel='"+cpemac[0]+"' AND tst > (CURRENT_TIMESTAMP - interval '24 hours') ORDER BY tst ASC"
  #return sql
  cur.execute(sql)
  conn.commit()
  dataSerie = cur.fetchall()
  if len(dataSerie) == 0:
    if stdout==False:
      return None
    import datetime
    dataSerie = ((datetime.datetime.now(),0),)
  maxS = ('',0)
  for t in dataSerie:
    if t[1] > maxS[1]:
      maxS = t
  if stdout:
    fname = None
    can = canvas.init(fname=None,format=fileFormat)
    import sys
    headers = 'Content-Type: image/png; charset=utf-8\r\n\r\n'
    sys.stdout.write(headers)
  else:
    f, fname = tempfile.mkstemp()
    can = canvas.init(fname,format=fileFormat)
  can.show(0, 150, "/25/H"+str('MAC prefix: '+cpemac[0]))
  #l = legend.T(loc=(360,140),nr_rows=1)
  ar = area.T(legend = None,
	      size = (300,140),
	      x_coord = category_coord.T(dataSerie, 0),
	      y_range = (0, None),
	      y_grid_interval =maxS[1]/5,
	      x_axis = axis.X(label = "/15Time", format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Leases".decode('utf8')))
  plot1 = line_plot.T(data = dataSerie, ycol=1, line_style = line_style.T(color=color.green,width=4.0),label=" /15Current", data_label_format = format_data_label, data_label_offset = (0,3))
  ar.add_plot(plot1)
  ar.draw(can)
  can.close()
  if stdout==False:
    os.close(f)
  return fname

def getipblocks(conn,cur):
  sql = 'SELECT id,ipblock_net,ipblock_prefix,att,usersegment,userlocation,vlanname,routername FROM ipblock ORDER BY ipblock_net;'
  cur.execute(sql)
  conn.commit()
  ipblocks = cur.fetchall()
  return ipblocks

def getipblock(conn,cur,i):
  sql = 'SELECT ipblock_net,ipblock_prefix,att,usersegment,userlocation,vlanname,routername FROM ipblock WHERE id='+str(i)+' ORDER BY ipblock_net;'
  cur.execute(sql)
  conn.commit()
  ipblocks = cur.fetchall()
  return ipblocks

def graph_ipblock(conn, cur, i, fileFormat, stdout=False):
  ipblockT = getipblock(conn,cur,i)
  ipblock = ipblockT[0]
  import ipcalc
  ipnetwork = ipcalc.Network(ipblock[0],ipblock[1])
  #sql = "SELECT tst,active_count,"+str(ipnetwork.size()-3)+" FROM ipblock_stat WHERE ipblock='"+ipblock[0]+"' AND tst > (CURRENT_TIMESTAMP - interval '24 hours') ORDER BY tst ASC"
  sql = "SELECT ipblock_stat.tst,active_count,ipblock.ipblock_maxleases FROM ipblock_stat JOIN ipblock ON ipblock.ipblock_net='"+ipblock[0]+"' WHERE  ipblock_stat.ipblock='"+ipblock[0]+"' AND ipblock_stat.tst > (CURRENT_TIMESTAMP - interval '24 hours') ORDER BY ipblock_stat.tst ASC;"
  cur.execute(sql)
  conn.commit()
  dataSerie = cur.fetchall()
  if len(dataSerie) == 0:
    if stdout == False:
      return None
    import datetime
    dataSerie = ((datetime.datetime.now(),0,0),)
    maxS = dataSerie[0]
    t = dataSerie[0]
  else:
    maxS = ('',0,0)
    for t in dataSerie:
      if t[1] > maxS[1]:
	maxS = t
  if stdout:
    import sys
    fname = None
    can = canvas.init(fname=None,format=fileFormat)
    headers = 'Content-Type: image/png; charset=utf-8\r\n\r\n'
    sys.stdout.write(headers)
  else:
    f, fname = tempfile.mkstemp()
    can = canvas.init(fname,format=fileFormat)
  can.show(0, 150, '/15/HIP block: '+ipblock[0]+'//'+str(ipblock[1])+'. Leases limit: '+str(t[2])+'\nUser segment: '+str(ipblock[3])+'\nOLT: '+str(ipblock[6])+'. Max lease: '+str(maxS[1])+' at '+str(maxS[0].hour)+":"+str(maxS[0].minute).zfill(2)+'hs')
  l = legend.T(loc=(104,10),nr_rows=1)
  ar = area.T(legend = l,
	      size = (360,140),
	      x_coord = category_coord.T(dataSerie, 0),
	      y_range = (0, maxS[1]*1.25),
	      y_grid_interval =maxS[1]/5,
	      x_axis = axis.X(label = "/15Time", format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Leases".decode('utf8')))
  plot1 = line_plot.T(data = dataSerie, ycol=1, line_style = line_style.T(color=color.green,width=4.0),label=" /15Current", data_label_format = format_data_label, data_label_offset = (0,3))
  plot2 = line_plot.T(data = dataSerie, ycol=2, line_style = line_style.T(color=color.red,width=4.0),label=" /15Limit" )
  ar.add_plot(plot2)
  ar.add_plot(plot1)
  ar.draw(can)
  can.close()
  if stdout==False:
    os.close(f)
  return fname

def graph_format(formato):
  theme.output_format = formato
  theme.reinitialize()

def graph_actives(conn, cur, name, fileFormat):
  global body
  global alturaAcum
  body = ''
  f, fname = tempfile.mkstemp()
  can = canvas.init(fname,format=fileFormat)
  # Historico
  sql = "SELECT tst,active_count_max,active_count_min,active_count_avg FROM active_stat_history WHERE dhcpdhn='"+name+"' AND tst >= (CURRENT_TIMESTAMP - interval '33 days') ORDER BY tst ASC"
  cur.execute(sql)
  conn.commit()
  dataSerie = cur.fetchall()
  if len(dataSerie) == 0:
    import datetime
    dataSerie = ((datetime.datetime.today(),0),)
  maxS = ('',0)
  for t in dataSerie:
    if t[1] > maxS[1]:
      maxS = t
  can.show(5, 150, "/25/H"+str('History')+'-/15/H'+name)
  #l = legend.T(loc=(0,-80),nr_rows=1)
  ar = area.T( size = (450,140),
  		legend = None,
	      x_coord = category_coord.T(dataSerie, 0),
	      y_range = (0, None),
	      y_grid_interval = maxS[1]/5,
	      x_axis = axis.X(label = "/15Time", format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Leases".decode('utf8')))
  plot1 = bar_plot.T(data = dataSerie, hcol=1, fill_style = fill_style.green, data_label_format = format_data_label)
  ar.add_plot(plot1)
  ar.draw(can)
  can.close()
  os.close(f)
  # Total conexiones simultaneas
  sql = "SELECT tst,active_count FROM active_stat WHERE dhcpdhn='"+name+"' AND tst > (CURRENT_TIMESTAMP - interval '24 hours') ORDER BY tst ASC"
  cur.execute(sql)
  conn.commit()
  dataSerie = cur.fetchall()
  if len(dataSerie) == 0:
    import datetime
    dataSerie = ((datetime.datetime.today(),0),)
  maxS = ('',0)
  for t in dataSerie:
    if t[1] > maxS[1]:
      maxS = t
  currText = "/H/15{}Current: "+str(t[1])+" at "+str(t[0].hour)+":"+str(t[0].minute).zfill(2)
  maxText = "/H/15{}Max: "+str(maxS[1])+" at "+str(maxS[0].hour)+":"+str(maxS[0].minute).zfill(2)
  f, fname2 = tempfile.mkstemp()
  can = canvas.init(fname2,format=fileFormat)
  can.show(5, 150, "/H/15Server: "+name+'\n'+currText+'\n'+maxText)
  #can.show(5, 10, currText+'. '+maxText)
  l = legend.T(loc=(0,-80),nr_rows=1)
  ar = area.T(legend = None,
	      #loc=(0,230),
	      size = (450,140),
	      x_coord = category_coord.T(dataSerie, 0),
	      y_range = (0, None),
	      y_grid_interval = maxS[1]/5,
	      x_axis = axis.X(label = "/15Time", label_offset = (170,0), format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Leases".decode('utf8')))
  plot2 = line_plot.T(data = dataSerie, ycol=1, line_style = line_style.T(color=color.green,width=4.0),label=" /15"+name, data_label_format = format_data_label)
  ar.add_plot(plot2)
  ar.draw(can)
  can.close()
  os.close(f)
  return (fname,fname2)

def graph_requests(conn, cur, name, fileFormat):
  global body
  global alturaAcum
  body = ''
  # Total conexiones simultaneas
  sql = "SELECT tst,dhcpdiscover,dhcpoffer,dhcprequest,dhcpack FROM active_stat WHERE dhcpdhn='"+name+"' AND tst > (CURRENT_TIMESTAMP - interval '24 hours') ORDER BY tst ASC"
  cur.execute(sql)
  conn.commit()
  dataSerie = cur.fetchall()
  # DHCPDISCOVER/DHCPOFFER
  if len(dataSerie) == 0:
    import datetime
    dataSerie = ((datetime.datetime.today(),0),)
  maxS = ('',0)
  for t in dataSerie:
    if t[1] > maxS[1]:
      maxS = t
  l = legend.T(loc=(0,-80),nr_rows=2)
  ar = area.T(legend = l,
	      #loc=(0,230),
	      size = (450,140),
	      x_coord = category_coord.T(dataSerie, 0),
	      y_range = (0, None),
	      y_grid_interval = maxS[1]/5,
	      x_axis = axis.X(label = "/15Time", label_offset = (170,0), format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Times".decode('utf8')))
  plot1 = line_plot.T(data = dataSerie, ycol=1, line_style = line_style.T(color=color.green,width=4.0),label=" /15DHCPDISCOVER", data_label_format = format_data_label)
  ar.add_plot(plot1)
  plot2 = line_plot.T(data = dataSerie, ycol=2, line_style = line_style.T(color=color.blue,width=4.0),label=" /15DHCPOFFER", data_label_format = format_data_label)
  ar.add_plot(plot2)
  f, fname = tempfile.mkstemp()
  can = canvas.init(fname,format=fileFormat)
  ar.draw(can)
  can.close()
  os.close(f)
  # DHCPREQUEST/DHCPACK
  if len(dataSerie) == 0:
    import datetime
    dataSerie = ((datetime.datetime.today(),0),)
  maxS = ('',0)
  for t in dataSerie:
    if t[3] > maxS[1]:
      maxS = t
  l = legend.T(loc=(0,-80),nr_rows=2)
  ar = area.T(legend = l,
	      #loc=(0,230),
	      size = (450,140),
	      x_coord = category_coord.T(dataSerie, 0),
	      y_range = (0, None),
	      y_grid_interval = maxS[3]/5,
	      x_axis = axis.X(label = "/15Time", label_offset = (170,0), format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Times".decode('utf8')))
  plot1 = line_plot.T(data = dataSerie, ycol=3, line_style = line_style.T(color=color.green,width=4.0),label=" /15DHCPREQUEST", data_label_format = format_data_label)
  ar.add_plot(plot1)
  plot2 = line_plot.T(data = dataSerie, ycol=4, line_style = line_style.T(color=color.blue,width=4.0),label=" /15DHCPACK", data_label_format = format_data_label)
  ar.add_plot(plot2)
  f, fname2 = tempfile.mkstemp()
  can = canvas.init(fname2,format=fileFormat)
  ar.draw(can)
  can.close()
  os.close(f)
  return (fname,fname2)
