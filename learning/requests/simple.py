__author__ = 'mcxiaoke'

import requests
import simplejson

req = requests.get('http://moment.douban.com/api/stream/current?format=lite')
print req.status_code
# print req.headers
# print req.encoding
print req.json()['posts'][0]['title']
#json_data= req.text
#json=json.loads(json_data)
#print json