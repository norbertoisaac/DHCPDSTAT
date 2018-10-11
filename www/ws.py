import cgi
import dbconn
import json
bodyO = {'status':0,'message':'success'}
form = cgi.FieldStorage()
body = json.dumps(bodyO)
headers = 'Content-Type: text/html; charset=utf-8\r\n'
headers += "Content-Length: "+str(len(body))+"\r\n\r\n"
sys.stdout.write(headers+body)
