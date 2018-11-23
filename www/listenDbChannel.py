import dbconn
import select
import time
import datetime
import psycopg2
def getDbConn(channel):
  conn,cur = dbconn.getDbConnDict()
  sql = "LISTEN "+channel
  cur.execute(sql)
  conn.commit()
  return (conn,cur)

def notifyMain(channel,callbackProcessFunction):
  #conn,curs = getDbConn()
  conn = None
  cur = None
  while 1:
    try:
      tIso = datetime.datetime.now().isoformat()
      if conn==None:
	conn, curs = getDbConn(channel)
      else:
         if conn.closed:
           conn.reset()
      if select.select([conn],[],[],5) == ([],[],[]):
	#print "Timeout"
	pass
      else:
	conn.poll()
	while conn.notifies:
	  notify = conn.notifies.pop(0)
	  #recvnotify( notify.payload)
	  #print "Got NOTIFY:", notify.pid, notify.channel, notify.payload
          callbackProcessFunction(conn,curs,notify.payload)
    except NameError:
      time.sleep(1)
      print tIso,'NameError',NameError
    except psycopg2.OperationalError as e:
      time.sleep(1)
      print tIso,'psycopg2.OperationalError',str(e)
    except Exception  as e:
      time.sleep(1)
      print tIso,'Exception',str(e)
      pass

