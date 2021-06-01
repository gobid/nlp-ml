import statsmodels.tsa.api as tsa
import statsmodels.api as sm
import statsmodels.stats.diagnostic as diag
from statsmodels.sandbox.tools import pca
import get_stock_data as gsd
from statsmodels.tsa.base.datetools import dates_from_range
import pandas as pd
import numpy as np
import MySQLdb
import pandas.io.sql as psql
from scipy import linalg 
from itertools import chain
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

endogenous = 'CHG_PCT_1D'

db = MySQLdb.connect('localhost', 'root', 'glassesandhair', "stocks")
#query = "select date, CHG_PCT_1D, PX_LAST, PX_RATIO, EBITDA, PX_ASK, PX_VOLUME, PX_BID, BOOK_VAL_PER_SH, MOV_AVG_200D, MOV_AVG_50D, PX_HIGH, PX_LOW, DIVIDEND_YIELD, DILUTED_EPS_AFT_XO_ITEMS_GROWTH, EQY_FLOAT, CUR_MKT_CAP, PX_OPEN, SALES_REV_TURN, EQY_SH_OUT, VOLATILITY_10D, VOLATILITY_180D, VOLATILITY_360D from stocks where ticker = 'GOOG UW Equity' and date>= '2011-01-01' and CHG_PCT_1D is not NULL and PX_LAST is not NULL and PX_RATIO is not NULL and EBITDA is not NULL and PX_ASK is not NULL and PX_VOLUME is not NULL and PX_BID is not NULL and BOOK_VAL_PER_SH is not NULL and CHG_PCT_1D is not NULL and MOV_AVG_200D is not NULL and MOV_AVG_50D is not NULL and PX_HIGH is not NULL and PX_LOW is not NULL and DIVIDEND_YIELD is not NULL and DILUTED_EPS_AFT_XO_ITEMS_GROWTH is not NULL and EQY_FLOAT is not NULL and CUR_MKT_CAP is not NULL and PX_OPEN is not NULL and SALES_REV_TURN is not NULL and EQY_SH_OUT is not NULL and VOLATILITY_10D is not NULL and VOLATILITY_180D is not NULL and VOLATILITY_360D is not NULL ORDER BY date"
query = "select date, CHG_PCT_1D, PX_LAST, PX_RATIO, EBITDA, PX_ASK, PX_VOLUME, PX_BID, BOOK_VAL_PER_SH, MOV_AVG_200D, MOV_AVG_50D, PX_HIGH, PX_LOW, DIVIDEND_YIELD, DILUTED_EPS_AFT_XO_ITEMS_GROWTH, EQY_FLOAT, CUR_MKT_CAP, PX_OPEN, SALES_REV_TURN, EQY_SH_OUT, VOLATILITY_10D, VOLATILITY_180D, VOLATILITY_360D from stocks where ticker = 'GOOG UW Equity' and date>= '2009-01-01' ORDER BY date"
#query = "select date, CHG_PCT_1D, PX_LAST, PX_RATIO, EBITDA, PX_ASK, PX_VOLUME, BOOK_VAL_PER_SH, PX_LOW, EQY_FLOAT, CUR_MKT_CAP, PX_OPEN, SALES_REV_TURN,VOLATILITY_10D, VOLATILITY_180D, VOLATILITY_360D, "
#query += "uni1, uni2, uni3, uni5, uni6, uni7, uni8, uni9, uni10, uni11, uni12, uni13, uni14, uni15, uni16, uni17, uni18, uni19, uni21, uni22, uni26, uni27, uni28, uni30,"
#query += "bi1, bi2, bi3, bi4, bi5, bi6, bi7, bi9, bi10, bi11, bi12, bi13, bi14, bi15, bi16, bi17, bi18, bi19, bi20, bi21, bi22 , bi23, bi25, bi26, bi29, bi30,"
#query += "tri1, tri2, tri3, tri4, tri5, tri6, tri7, tri8, tri9, tri10, tri11, tri12, tri13, tri14, tri15, tri16, tri17, tri18, tri19, tri20, tri21, tri23, tri24, tri25, tri26, tri27, tri28, tri29, tri30,"
#query += "feat1, feat2, feat3"
#query += " from goog_info where ticker = 'GOOG UW Equity' and date>= '2009-01-01' ORDER BY date"
#query = "select date, CHG_PCT_1D, PX_LAST, PX_RATIO, EBITDA, PX_ASK, PX_VOLUME, BOOK_VAL_PER_SH, PX_LOW, EQY_FLOAT, CUR_MKT_CAP, PX_OPEN, SALES_REV_TURN,VOLATILITY_10D, VOLATILITY_180D, VOLATILITY_360D, "
#query += "uni1, uni2, uni3, uni4, uni5, uni6, uni7, uni8, uni9, uni11, uni12, uni13, uni14, uni15, uni16, uni17, uni18, uni19, uni20, uni21, uni22, uni23, uni24, uni25, uni26, uni27, uni28, uni29, uni30,"
#query += "bi1, bi2, bi3, bi4, bi5, bi6, bi7, bi8, bi10, bi11, bi12, bi14, bi15, bi16, bi17, bi18, bi19, bi20, bi21, bi22 , bi23, bi24, bi25, bi26, bi27, bi28, bi29, bi30,"
#query += "tri1, tri2, tri3, tri6, tri7, tri8, tri9, tri10, tri11, tri12, tri13, tri14, tri15, tri16, tri17, tri18, tri19, tri20, tri21, tri22, tri23, tri24, tri25, tri26, tri27, tri28, tri29, tri30,"
#query += "feat1, feat2, feat3"
#query += " from GE where ticker = 'GE UN Equity' and date>= '2009-01-01' ORDER BY date"
#query = "select date, CHG_PCT_1D, PX_LAST, PX_RATIO, EBITDA, PX_ASK, PX_VOLUME, BOOK_VAL_PER_SH, PX_LOW, EQY_FLOAT, CUR_MKT_CAP, PX_OPEN, SALES_REV_TURN,VOLATILITY_10D, VOLATILITY_180D, VOLATILITY_360D, "
#query += "uni1, uni2, uni3, uni4, uni5, uni6, uni7, uni8, uni9, uni10, uni11, uni12, uni13, uni14, uni15, uni16, uni17, uni18, uni19, uni20, uni21, uni22, uni23, uni24, uni25, uni26, uni27, uni28, uni29, uni30,"
#query += "bi1, bi2, bi3, bi4, bi5, bi6, bi7, bi8, bi9, bi10, bi11, bi12, bi13, bi14, bi15, bi16, bi17, bi18, bi19, bi20, bi21, bi22 , bi23, bi24, bi25, bi26, bi27, bi28, bi29, bi30,"
#query += "tri1, tri2, tri3, tri4, tri5, tri6, tri7, tri8, tri9, tri10, tri11, tri12, tri13, tri14, tri15, tri16, tri17, tri18, tri19, tri20, tri21, tri22, tri23, tri24, tri25, tri26, tri27, tri28, tri29, tri30,"
#query += "feat1, feat2, feat3"
#query += " from goog_info where ticker = 'GOOG UW Equity' and date>= '2009-01-01' ORDER BY date"

x = psql.frame_query(query,con=db)
x = x.set_index('date')
#x = x.loc[:, (x <> x.ix[0]).any()] 

addDays= pd.date_range(x.index[0],x.index[-1],freq='B')
x=x.reindex(addDays)
x=x.apply(lambda col: col.interpolate('linear'))
x = x.loc[:, (x <> x.ix[0]).any()]
#print x.head(3).to_string()
x=x.shift(1,freq='B')
shiftedEndo = x[endogenous].shift(-1,freq='B')
x = x[:len(x)-1]
x[endogenous]=shiftedEndo
#print x.head(3).to_string()
x = x.fillna(0)
x = x.loc[:, (x <> x.ix[0]).any()]
print x

CVsize = round(.1 * len(x))

xt = x[0:len(x)-CVsize]
xc = x[len(x)-CVsize:len(x)]

optScore = -1000000
optTrainScore = -1000000
optAIC = 100000
optP = -1
optD = -1
optQ = -1
for a in range(1,2):
	for b in range(0,1):
		for c in range(10,11):
			#if True:
			try:
				#olsResults = sm.OLS(xt[endogenous],xt.drop(endogenous,axis=1)).fit()
				#prediction = olsResults.predict(x.drop(endogenous,axis=1))				
				#arima = tsa.ARIMA(olsResults.resid,order=(a,b,c),freq='B')
                                #results = arima.fit(transparam=True, dynamic=True)
                                #print prediction
				#prediction = prediction[b:] + results.predict(start=b,end=len(x)-1)
				#prediction = prediction[b:]
				#print results.predict(start=b,end=len(x)-1)
				#print diag.acorr_breush_godfrey(olsResults)
				
				arima = tsa.ARIMA(xt[endogenous], exog=xt.drop(endogenous,axis=1), order=(a,b,c),freq='B')
				results = arima.fit(transparam=True, dynamic=True)
				prediction = results.predict(start=b,end=len(x)-1, exog=x.drop(endogenous,axis=1))
				print results.params				

				ext = xt[endogenous][b:]
				exc = xc[endogenous]
				#print len(ext)+len(exc)
				#print xt[endogenous][b:8]
				#print xt[endogenous][len(xt)-8:]
				#print xc[endogenous][:8]
				#print prediction[len(ext)-8:len(ext)+8]
				score = 1 - (sum((prediction[len(ext):] - exc) ** 2)/sum((exc - exc.mean()) ** 2))
                                trainScore = 1 - (sum((prediction[0:len(ext)] - ext) ** 2)/sum((ext - ext.mean()) ** 2))

				print score
				print trainScore
				print results.aic
				print a,b,c
				#if score > optScore:
				if results.aic < optAIC:
					optScore = score
					optTrainScore = trainScore
					optAIC = results.aic
					optP = a
					optD = b
					optQ = c
			except Exception as e:
				print e

pd.set_option('display.max_rows', len(xc[endogenous]))
print xc.index
print xc[endogenous].values
print prediction[len(ext):].values
pd.reset_option('display.max_rows')

plt.figure()
with pd.plot_params.use('x_compat', True):
	x[endogenous].plot(color='r')
	prediction.plot(color='g')
plt.savefig("/home/ubuntu/app/plottest.png")

print 'OPTIMAL'
print optScore
print optTrainScore
print optAIC
print optP,optD,optQ

optScoreFS = optScore
optTrainScoreFS = optTrainScore
optAICFS = optAIC

numToDrop = 0
endFS = False
print 'START FEATURE SELECTION'
for j in range(0,numToDrop-1):
	if endFS:
		print 'ENDING FEATURE SELECTION'
		break
	dropCol = 1
	tempScore = -100000
	for i in range(15,len(x.drop(endogenous,axis=1).columns)-j-2):
		#if True:
		try:
			arima = tsa.ARIMA(xt[endogenous], exog=xt.drop(endogenous,axis=1).drop(x.columns[i],axis=1), order=(optP,optD,optQ),freq='B')
        		results = arima.fit(transparam=True, dynamic=True)
        		prediction = results.predict(start=optD,end=len(x)-1, exog=x.drop(endogenous,axis=1).drop(x.columns[i],axis=1))

        		ext = xt[endogenous][optD:]
        		exc = xc[endogenous]

			score = 1 - (sum((prediction[len(ext):] - exc) ** 2)/sum((exc - exc.mean()) ** 2))
        		trainScore = 1 - (sum((prediction[0:len(ext)] - ext) ** 2)/sum((ext - ext.mean()) ** 2))
			
			print x.columns[i]
                	print score
                	print trainScore
                	print results.aic

			if score > tempScore:
                        	tempScore = score
                                optTrainScoreFS = trainScore
                                optAICFS = results.aic
				dropCol = i
		except Exception as e:
                        print e
	if tempScore > optScoreFS and tempScore > optScore:
		print 'DROPPING'
		print x.columns[dropCol]
		print x
		optScoreFS = tempScore
		print optScoreFS
		x=x.drop(x.columns[dropCol],axis=1)
		xt=xt.drop(xt.columns[dropCol],axis=1)
		xc=xc.drop(xc.columns[dropCol],axis=1)
	else:
		endFS = True
print 'OPTIMAL FS'
print x
print optScoreFS
print optTrainScoreFS
print optAICFS

tempScorePCA = -1000000000
runPCA = True
tol = 0
for dim in range(len(x.drop(endogenous,axis=1).columns), 1000000000, -1):
	print 'NEXT ITERATION PCA'
	xred, fact, eva, eve  = pca(xt.drop(endogenous,axis=1), keepdim=dim, normalize=1)
	
	test = np.array(x.drop(endogenous,axis=1))
	m = test.mean(0)
	test_reduced = np.dot(fact, eve.T) + m

	arima = tsa.ARIMA(xt[endogenous], exog=xred, order=(optP,optD,optQ),freq='B')
        results = arima.fit(transparam=True, dynamic=True)
        prediction = results.predict(start=optD,end=len(x)-1, exog=test_reduced)

        ext = xt[endogenous][optD:]
        exc = xc[endogenous]

        score = 1 - (sum((prediction[len(ext):] - exc) ** 2)/sum((exc - exc.mean()) ** 2))
        trainScore = 1 - (sum((prediction[0:len(ext)] - ext) ** 2)/sum((ext - ext.mean()) ** 2))

	if score > optScore and score > tempScorePCA - tol:
		tempScorePCA = score
		print 'DROPPING PCA'
		print dim
		print tempScorePCA
		print trainScore
	else:
		print 'ENDING PCA %f', score
		print tempScorePCA
		print trainScore
		runPCA = False

tempScoreFilter = optScore
runFilter = False
tol = .01
denEnd = ((x[endogenous] * x[endogenous]).sum() - x[endogenous].sum() * x[endogenous].sum())
while runFilter:
	minR2 = 10000000
	i = -1
	for j in range(15, len(x.columns)):
		num = ((x[endogenous] * x[x.columns[j]]).sum() - x[endogenous].sum() * x[x.columns[j]].sum()) ** 2
		den = ((x[x.columns[j]] * x[x.columns[j]]).sum() - x[x.columns[j]].sum() * x[x.columns[j]].sum())
		R2val = num/(denEnd * den)
		
		if R2val < minR2:
			minR2 = R2val
			i = j

	try:
		arima = tsa.ARIMA(xt[endogenous], exog=xt.drop(endogenous,axis=1).drop(x.columns[i],axis=1), order=(optP,optD,optQ),freq='B')
                results = arima.fit(transparam=True, dynamic=True)
                prediction = results.predict(start=optD,end=len(x)-1, exog=x.drop(endogenous,axis=1).drop(x.columns[i],axis=1))

                ext = xt[endogenous][optD:]
                exc = xc[endogenous]

                score = 1 - (sum((prediction[len(ext):] - exc) ** 2)/sum((exc - exc.mean()) ** 2))
                trainScore = 1 - (sum((prediction[0:len(ext)] - ext) ** 2)/sum((ext - ext.mean()) ** 2))
		
		if score > (tempScoreFilter-tol) and score > (optScore-tol):
			tempScoreFilter = score
			print 'DROPPING Filter'
			print x.columns[i]
			print tempScoreFilter
			print trainScore
			x=x.drop(x.columns[i],axis=1)
                	xt=xt.drop(xt.columns[i],axis=1)
                	xc=xc.drop(xc.columns[i],axis=1)
		else:
			print 'END FILTER'
			print score
			print 'OPTIMAL'
			print tempScoreFilter
			runFilter = False
	except Exception as e:
		print e

#print x
