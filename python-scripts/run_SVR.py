from sklearn.svm import SVR
from sklearn import linear_model
from sklearn import preprocessing
from sklearn.kernel_approximation import RBFSampler
from sklearn.cluster import KMeans, MiniBatchKMeans

import MySQLdb
import get_stock_data as gsd


#db = MySQLdb.connect('localhost', 'root', 'glassesandhair', "stocks")
#cursor = db.cursor()

#getTickersQuery = "SELECT DISTINCT ticker FROM stocks";
#cursor.execute(getTickersQuery)
#tickers = cursor.fetchall()

#for t in tickers:
	#print t
	#(x,y) = gsd.get_stock_matrix(t[0])

(x,y) = gsd.get_stock_matrix()
print len(x)

CVsize = round(.3 * len(x))
print CVsize

svr_rbf = SVR(kernel='rbf', C=1, gamma=.1, degree=3, max_iter = -1, cache_size = 200)
clf = linear_model.SGDRegressor(shuffle=True)
#clf = linear_model.Ridge(alpha=.001, normalize=True)
#svr_lin = SVR(kernel='linear', C=1e3, max_iter = -1)
#svr_poly = SVR(kernel='poly', C=1e3, degree=3, max_iter = -1)

x = preprocessing.scale(x)

optg = 0
optn = 0
optScore = -1e10
optFitScore = -1e10

for n in range(70, 65, 1):
	km = MiniBatchKMeans(n_clusters=n, init='k-means++', max_iter=500, n_init=5)
	#km = KMeans(n_clusters=n, init='k-means++', max_iter=500, n_init=5)
	km.fit(x)
	centers = km.cluster_centers_
	basis = centers[centers[:,0].argsort()]
	for g in range(5,20,1):
		rbf_feature = RBFSampler(gamma=g/100.0, n_components = n)
		xt = rbf_feature.fit(basis).transform(x)
		#xt = rbf_feature.fit_transform(x)
		clf.fit(xt[0:len(xt)-CVsize], y[0:len(y)-CVsize])
		score = clf.score(xt[len(xt)-CVsize:len(xt)-1],y[len(y)-CVsize:len(y)-1])
		fitScore = clf.score(xt[0:len(xt)-CVsize], y[0:len(y)-CVsize])

		if score > optScore:
			optg = g/100.0
			optn = n
			optScore = score
			optFitScore = fitScore

		print g/100.0
		print n
		print score
		print fitScore

print "optimal"
print optg
print optn
print optScore
print optFitScore

y_rbf = svr_rbf.fit(x[0:len(x)-CVsize], y[0:len(y)-CVsize]).predict(x[0:len(x)-CVsize])
#y_lin = svr_lin.fit(x[0:len(x)-CVsize], y[0:len(y)-CVsize]).predict(x[0:len(x)-CVsize])
#y_poly = svr_poly.fit(x[0:len(x)-CVsize], y[0:len(y)-CVsize]).predict(x[0:len(x)-CVsize])

print svr_rbf.score(x[len(x)-CVsize:len(x)-1],y[len(y)-CVsize:len(y)-1])
print svr_rbf.score(x[0:len(x)-CVsize],y[0:len(y)-CVsize])
#print svr_lin.score(x[len(x)-CVsize:len(x)-1],y[len(y)-CVsize:len(y)-1])
#print svr_poly.score(x[len(x)-CVsize:len(x)-1],y[len(y)-CVsize:len(y)-1])

#print 'predicted '
#print clf.predict(x[150000:150010, :])
#print 'actual ' 
#print y[150000:150010]
