import urllib2
from datetime import date, timedelta as td

API_KEY = 'AIzaSyDDp9yCeGfA7ZkVplHopyrc4nIoPvPcGsU'
CX = '018061362833819783195:u5g6pmnm-v4'
query = 'AAPL%20Apple%20Inc.'

d1 = date(2004,8,19)
d2 = date(2004,11,27)
delta = d2 - d1 

for i in range(delta.days + 1):
	date = str(d1).replace('-','')
	url = 'https://www.googleapis.com/customsearch/v1?key='
	url += API_KEY + '&cx=' + CX + '&q=' + query + '&sort=date:r:' + date + ':' + date
	print 'url: ' + url
	content = urllib2.urlopen(url).read()
	print content
	d1 += td(days=1)

