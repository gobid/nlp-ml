# get_stock_data module

import MySQLdb
import numpy as np

Y_LABEL_INDEX = 0

def get_stock_matrix(): 
	db = MySQLdb.connect('localhost', 'root', 'glassesandhair', "stocks")
	c = db.cursor()
	query = "select CHG_PCT_1D, PX_LAST, PX_RATIO, EBITDA, PX_ASK, PX_VOLUME, PX_BID, BOOK_VAL_PER_SH, MOV_AVG_200D, MOV_AVG_50D, PX_HIGH, PX_LOW, DIVIDEND_YIELD, DILUTED_EPS_AFT_XO_ITEMS_GROWTH, EQY_FLOAT, CUR_MKT_CAP, PX_OPEN, SALES_REV_TURN, EQY_SH_OUT, VOLATILITY_10D, VOLATILITY_180D, VOLATILITY_360D from stocks where CHG_PCT_1D is not NULL and PX_LAST is not NULL and PX_RATIO is not NULL and EBITDA is not NULL and PX_ASK is not NULL and PX_VOLUME is not NULL and PX_BID is not NULL and BOOK_VAL_PER_SH is not NULL and CHG_PCT_1D is not NULL and MOV_AVG_200D is not NULL and MOV_AVG_50D is not NULL and PX_HIGH is not NULL and PX_LOW is not NULL and DIVIDEND_YIELD is not NULL and DILUTED_EPS_AFT_XO_ITEMS_GROWTH is not NULL and EQY_FLOAT is not NULL and CUR_MKT_CAP is not NULL and PX_OPEN is not NULL and SALES_REV_TURN is not NULL and EQY_SH_OUT is not NULL and VOLATILITY_10D is not NULL and VOLATILITY_180D is not NULL and VOLATILITY_360D is not NULL and date >= '2012-01-01' ORDER BY date limit 10000"
	c.execute(query)
	results = c.fetchall()
	l = [list(sublist) for sublist in results]	
	if len(l) > 0:
		x = np.array(l)
		y = x[:, Y_LABEL_INDEX]
		print y
		y = y[1:y.size]
		print y
		x = np.delete(x, Y_LABEL_INDEX, 1)
		(m,n) = x.shape
		print x
		x = x[0:m-1,:]
		(m,n) = x.shape
		print x
	else: 
		x = []
		y = []
	return x, y
