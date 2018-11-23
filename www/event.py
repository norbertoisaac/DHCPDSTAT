import dbconn
import time
def existEvent(obj_id,event_id,event_actives):
  res = False
  for event_active in event_actives:
    if obj_id==event_active['obj_id'] and event_id==event_active['event_id']:
      res = event_active['id']
      break
  return res

def addEvent(cur,active_server,event,event_actives,event_value):
  res = False
  eventId = existEvent(active_server['object_id'],event['id'],event_actives)
  if eventId == False:
    values = {}
    values['obj_id'] = active_server['object_id']
    values['event_id'] = event['id']
    values['threshold_text'] = event['threshold_text']
    values['threshold_int'] = event['threshold_int']
    values['threshold_float'] = event['threshold_float']
    values['threshold_boolean'] = event['threshold_boolean']
    values['value_text'] = event_value['text']
    values['value_int'] = event_value['int']
    values['value_float'] = event_value['float']
    values['value_boolean'] = event_value['boolean']
    sql = "INSERT INTO event_log(obj_id,event_id,threshold_text,threshold_int,threshold_float,threshold_boolean,raise_value_text,raise_value_int,raise_value_float,raise_value_boolean) VALUES (%(obj_id)s,%(event_id)s,%(threshold_text)s,%(threshold_int)s,%(threshold_float)s,%(threshold_boolean)s,%(value_text)s,%(value_int)s,%(value_float)s,%(value_boolean)s)"
    cur.execute(sql,values)
    res = True
  return res

def delEvent(cur,active_server,event,event_actives,event_value):
  res = False
  eventId = existEvent(active_server['object_id'],event['id'],event_actives)
  if not eventId==False:
    values = {}
    values['id'] = eventId
    values['recovery_value_text'] = event_value['text']
    values['recovery_value_int'] = event_value['int']
    values['recovery_value_float'] = event_value['float']
    values['recovery_value_boolean'] = event_value['boolean']
    sql = "UPDATE event_log SET (notified,active,recovery_value_text,recovery_value_int,recovery_value_float,recovery_value_boolean,clear_time) = ('f','f',%(recovery_value_text)s,%(recovery_value_int)s,%(recovery_value_float)s,%(recovery_value_boolean)s,NOW()) WHERE id=%(id)s"
    cur.execute(sql,values)
    res = True
  return res

def cmpEventThreshold(event,active_server):
  global event_actives
  global cur
  res_status = False
  res_notify = False
  threshold_op = event['threshold_op']
  event_value = {}
  event_value['int'] = None
  event_value['float'] = None
  event_value['text'] = None
  event_value['boolean'] = None
  if event['threshold_type'] == 'fixed':
    value = active_server[event['attr_column']]
  elif event['threshold_type'] == 'relative':
    #print cur.mogrify(event['relative_sql'],active_server)
    cur.execute(event['relative_sql'],active_server)
    values = cur.fetchone()
    value = values['column_0']
    #value = values[0]
  # Value type
  if event['event_obj_attr_type'] == 'int':
    event_value['int'] = value
    threshold_value = event['threshold_int']
  elif event['event_obj_attr_type'] == 'float':
    event_value['float'] = value
    threshold_value = event['threshold_float']
  elif event['event_obj_attr_type'] == 'text':
    event_value['text'] = value
    threshold_value = event['threshold_text']
  elif event['event_obj_attr_type'] == 'boolean':
    event_value['boolean'] = value
    threshold_value = event['threshold_boolean']
  # Operation
  if threshold_op == 'eq':
    if value == threshold_value:
      res_status = True
  elif threshold_op == 'lt':
    if value < threshold_value:
      res_status = True
  elif threshold_op == 'le':
    if value <= threshold_value:
      res_status = True
  elif threshold_op == 'gt':
    if value > threshold_value:
      res_status = True
  elif threshold_op == 'ge':
    if value >= threshold_value:
      res_status = True
  elif threshold_op == 'not':
    if not value:
      res_status = True
  if res_status:
    res_notify = addEvent(cur,active_server,event,event_actives,event_value)
  else:
    res_notify = delEvent(cur,active_server,event,event_actives,event_value)
  if res_notify:
    print time.ctime(),res_status,active_server
  return res_notify

conn,cur = dbconn.getDbConnDict()
# Select actives events
sql = "SELECT * FROM event_log WHERE active='t'"
cur.execute(sql)
event_actives = cur.fetchall()
# Select Event object types
#sql = 'SELECT DISTINCT ON (event_obj_type) event_obj_type FROM events;'
sql = 'SELECT * FROM events ORDER BY event_obj_type;'
cur.execute(sql)
events = cur.fetchall()
event_obj_type_last = ''
notify_event = False
# Server type events
for event in events:
  if not event['event_obj_type'] == event_obj_type_last:
    event_obj_type_last = event['event_obj_type']
    if event_obj_type_last == 'server':
      sql = "SELECT DISTINCT ON (dhcpdhn) dhcpdhn,obj_orig_id,objects.id as object_id,active_stat.tst,active_count,inactive_count,dhcpdiscover,dhcpoffer,dhcprequest,dhcpack FROM active_stat JOIN servers ON servers.hostname=active_stat.dhcpdhn JOIN objects ON objects.obj_orig_id=servers.id WHERE objects.obj_orig_table='servers' AND objects.active='t' AND objects.alarm='t' AND active_stat.tst > (CURRENT_TIMESTAMP - interval '10 min') ORDER BY dhcpdhn,active_stat.tst DESC;"
      cur.execute(sql)
      if cur.rowcount:
	active_stat = cur.fetchall()
      else:
        active_stat = ()
    elif event_obj_type_last == 'ipblock':
      sql = "SELECT DISTINCT ON (ipblock) ipblock,obj_orig_id,objects.id as object_id,ipblock_stat.tst,active_count,inactive_count,dhcpdiscover,dhcpoffer,dhcprequest,dhcpack FROM ipblock_stat JOIN ipblock ON ipblock.ipblock_net=ipblock_stat.ipblock JOIN objects ON objects.obj_orig_id=ipblock.id WHERE objects.obj_type='ipblock' AND objects.active='t' AND objects.alarm='t' AND ipblock_stat.tst > (CURRENT_TIMESTAMP - interval '10 min') ORDER BY ipblock,ipblock_stat.tst DESC;"
      cur.execute(sql)
      if cur.rowcount:
	active_ipblocks = cur.fetchall()
      else:
        active_ipblocks = ()
  if event_obj_type_last == 'server':
    for active_server in active_stat:
      # Operation
      if cmpEventThreshold(event,active_server):
        notify_event = True
  elif event_obj_type_last == 'ipblock':
    for active_ipblock in active_ipblocks:
      # Operation
      if cmpEventThreshold(event,active_ipblock):
        notify_event = True
    pass

if notify_event:
  sql = "NOTIFY send_notify"
  cur.execute(sql)
#conn.rollback()
conn.commit()
conn.close()
