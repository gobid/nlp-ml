#!/usr/bin/python
import sys
import urllib2
import csv
from sklearn.svm import SVR
import numpy as np
import pylab as pl

if len(sys.argv) < 2: 
	print 'python get_historical_data.py [TICKER]'
else :
	print 'Stock Prices for ' + sys.argv[1]
	pricecsv = urllib2.urlopen('http://ichart.yahoo.com/table.csv?s=' + sys.argv[1]).read()
	reader = csv.reader(pricecsv.split('\n'), delimiter=',')
	price = []
	for r in reader:
		if len(r) >= 1:
			price.append(r[len(r)-1])

price = price[1:len(price)]

X = []
y = []
for i in range(1,len(price)-1):
	X.append(float(price[i]))
	y.append(float(price[i-1])/float(price[i]))

print len(X)
print len(y)

X = np.array(X)
y = np.array(y)

X = X.reshape(-1, 1)
y = y.reshape(-1)

print X.shape
print y.shape

svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_lin = SVR(kernel='linear', C=1e3)
svr_poly = SVR(kernel='poly', C=1e3, degree=2)
y_rbf = svr_rbf.fit(X, y).predict(X)
y_lin = svr_lin.fit(X, y).predict(X)
y_poly = svr_poly.fit(X, y).predict(X)

pl.scatter(X, y, c='k', label='data')
pl.hold('on')
pl.plot(X, y_rbf, c='g', label='RBF model')
pl.plot(X, y_lin, c='r', label='Linear model')
pl.plot(X, y_poly, c='b', label='Polynomial model')
pl.xlabel('data')
pl.ylabel('target')
pl.title('Support Vector Regression')
pl.legend()
pl.show()

