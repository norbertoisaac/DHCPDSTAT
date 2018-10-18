import tempfile
import os
import sys
from pychart import *
theme.use_color = True
theme.reinitialize()
body = ''
altura = 250
alturaAcum = 0

def getcpemac(conn,cur):
  sql = 'SELECT mac_prefix,vendor_name,model_name,release,eol,eos FROM cpe_mac ORDER BY mac_prefix;'
  cur.execute(sql)
  conn.commit()
  ipblocks = cur.fetchall()
  return ipblocks

def graph_cpemac(conn, cur, cpemac, fileFormat):
  global body
  global alturaAcum
  body = ''
  f, fname = tempfile.mkstemp()
  can = canvas.init(fname,format=fileFormat)
  sql = "SELECT tst,active_count FROM cpe_stat WHERE cpevendormodel='"+cpemac[0]+"' AND tst > (CURRENT_TIMESTAMP - interval '24 hours') ORDER BY tst ASC"
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
  can.show(5, 250, "/25/H"+str('MAC prefix: '+cpemac[0]))
  l = legend.T(loc=(104,10),nr_rows=1)
  ar = area.T(legend = l,
	      size = (800,243),
	      x_coord = category_coord.T(dataSerie, 0),
	      y_range = (0, maxS[1]+maxS[1]/4),
	      y_grid_interval =maxS[1]/4,
	      x_axis = axis.X(label = "/15Time", format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Connected clients".decode('utf8'),tic_interval = maxS[1]/4))
  plot1 = line_plot.T(data = dataSerie, ycol=1, line_style = line_style.T(color=color.green,width=4.0),label=" /15Current", data_label_format = format_data_label, data_label_offset = (0,3))
  ar.add_plot(plot1)
  ar.draw(can)
  try:
    can.close()
  except AttributeError as e:
    body += str(e)
  lenOfF = os.path.getsize(fname)
  os.lseek(f,0,os.SEEK_SET)
  body += os.read(f,lenOfF)

  os.close(f)
  return fname

def getipblocks(conn,cur):
  sql = 'SELECT ipblock_net,ipblock_prefix,usersegment,userlocation FROM ipblock ORDER BY ipblock_net;'
  cur.execute(sql)
  conn.commit()
  ipblocks = cur.fetchall()
  return ipblocks

def graph_ipblock(conn, cur, ipblock, fileFormat):
  global body
  global alturaAcum
  body = ''
  f, fname = tempfile.mkstemp()
  can = canvas.init(fname,format=fileFormat)
  sql = "SELECT tst,active_count FROM ipblock_stat WHERE ipblock='"+ipblock[0]+"' AND tst > (CURRENT_TIMESTAMP - interval '24 hours') ORDER BY tst ASC"
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
  can.show(5, 250, "/25/H"+str('IP segment: '+ipblock[0]))
  l = legend.T(loc=(104,10),nr_rows=1)
  ar = area.T(legend = l,
	      size = (800,243),
	      x_coord = category_coord.T(dataSerie, 0),
	      y_range = (0, maxS[1]+maxS[1]/4),
	      y_grid_interval =maxS[1]/4,
	      x_axis = axis.X(label = "/15Time", format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Connected clients".decode('utf8'),tic_interval = maxS[1]/4))
  plot1 = line_plot.T(data = dataSerie, ycol=1, line_style = line_style.T(color=color.green,width=4.0),label=" /15Current", data_label_format = format_data_label, data_label_offset = (0,3))
  ar.add_plot(plot1)
  ar.draw(can)
  try:
    can.close()
  except AttributeError as e:
    body += str(e)
  lenOfF = os.path.getsize(fname)
  os.lseek(f,0,os.SEEK_SET)
  body += os.read(f,lenOfF)

  os.close(f)
  return fname

def graph_format(formato):
  theme.output_format = formato
  theme.reinitialize()

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

def graph_actives(conn, cur, name, fileFormat):
  global body
  global alturaAcum
  body = ''
  f, fname = tempfile.mkstemp()
  can = canvas.init(fname,format=fileFormat)
  sql = "SELECT tst,active_count_max,active_count_min,active_count_avg FROM active_stat_history WHERE dhcpdhn='"+name+"' AND tst > (CURRENT_TIMESTAMP - interval '31 days') ORDER BY tst ASC"
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
  can.show(5, 250, "/25/H"+str('History'))
  l = legend.T(loc=(104,10),nr_rows=1)
  ar = area.T(legend = l,
	      size = (800,243),
	      x_coord = category_coord.T(dataSerie, 0),
	      y_range = (0, maxS[1]+1000.0),
	      y_grid_interval =1000,
	      x_axis = axis.X(label = "/15Time", format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Connected clients".decode('utf8'),tic_interval = 1000))
  plot1 = line_plot.T(data = dataSerie, ycol=1, line_style = line_style.T(color=color.green,width=4.0),label=" /15Max", data_label_format = format_data_label, data_label_offset = (0,3))
  ar.add_plot(plot1)
  ar.draw(can)
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
  maxText = "/H/15{} Max: "+str(maxS[1])+" at "+str(maxS[0].hour)+":"+str(maxS[0].minute).zfill(2)
  tb = text_box.T(loc=(0,280), text=maxText.decode('utf8'), fill_style=None, top_fudge=1, bottom_fudge=1, right_fudge=1, left_fudge=1, shadow=None)
  tb.draw()
  can.show(5, 600, "/25/H"+str('DHCP server: '+name+'\nTotal concurrent clients'))
  l = legend.T(loc=(104,360),nr_rows=1)
  ar = area.T(legend = l,
	      loc=(0,350),
	      size = (800,243),
	      x_coord = category_coord.T(dataSerie, 0),
	      y_range = (0, maxS[1]+1000.0),
	      y_grid_interval =1000,
	      x_axis = axis.X(label = "/15Time", label_offset = (170,0), format = format_tic_interval, tic_len=0),
	      y_axis = axis.Y(label="/15Connected clients".decode('utf8'),tic_interval = 1000))
  plot2 = line_plot.T(data = dataSerie, ycol=1, line_style = line_style.T(color=color.green,width=4.0),label=" /15"+name, data_label_format = format_data_label, data_label_offset = (0,3))
  ar.add_plot(plot2)
  try:
    ar.draw(can)
  except UnicodeDecodeError as e:
    body += str(e)
  except TypeError as e:
    body += str(e)
  except AttributeError as e:
    body += str(e)

  try:
    can.close()
  except AttributeError as e:
    body += str(e)
  lenOfF = os.path.getsize(fname)
  os.lseek(f,0,os.SEEK_SET)
  body += os.read(f,lenOfF)

  os.close(f)
  return fname
