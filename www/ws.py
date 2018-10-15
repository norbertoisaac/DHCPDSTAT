#! /usr/bin/python
import cgi
import dbconn
import json
import sys
bodyO = {'status':0,'message':'success'}
form = cgi.FieldStorage()
body = json.dumps(bodyO)
headers = 'Content-Type: application/json; charset=utf-8\r\n'
headers += "Content-Length: "+str(len(body))+"\r\n\r\n"
sys.stdout.write(headers+body)
