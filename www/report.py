# MSG
url = "http://www-mydomain.com/dhcpdstat/index.py"
mailBodyHtml = '''
<h2>DHCP server connection statistics</h2><p>Graphs in attached, <a href="'''+url+'''">or open in browser</a></p>
'''

# EMAIL
# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

# Define these once; use them twice!
strFrom = 'report@mydomain.com'
strTo = ['user1@mydomain.com','user2@mydomain.com']

# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['X-Priority'] = '2'
msgRoot['Subject'] = 'DHCP server report'
msgRoot['From'] = strFrom
msgRoot['To'] = strTo
msgRoot.preamble = 'This is a multi-part message in MIME format.'

msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

msgText = MIMEText(mailBodyHtml, 'html')
msgAlternative.attach(msgText)

import graph
import dbconn
conn,cur = dbconn.getDbConn()
fname = graph.graph_actives(conn,cur,'dhcpserver','pdf')
f = open(fname,'rb')
msgImage = MIMEImage(f.read(),_subtype="pdf")
f.close()
# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<dhcpservergraph>')
msgImage.add_header('Content-Disposition', 'inline', filename='conectedPerDHCPServer.pdf')
msgRoot.attach(msgImage)

# Send the email (this example assumes SMTP authentication is required)
import smtplib
smtp = smtplib.SMTP()
smtp.connect(smtp.mydomain.com)
smtp.sendmail(strFrom,strTo,msgRoot.as_string())
smtp.quit()
