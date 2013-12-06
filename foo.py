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

endogenous = 'CHG_PCT_1D'

db = MySQLdb.connect('localhost', 'root', 'glassesandhair', "stocks")
#query = "select date, CHG_PCT_1D, PX_LAST, PX_RATIO, EBITDA, PX_ASK, PX_VOLUME, PX_BID, BOOK_VAL_PER_SH, MOV_AVG_200D, MOV_AVG_50D, PX_HIGH, PX_LOW, DIVIDEND_YIELD, DILUTED_EPS_AFT_XO_ITEMS_GROWTH, EQY_FLOAT, CUR_MKT_CAP, PX_OPEN, SALES_REV_TURN, EQY_SH_OUT, VOLATILITY_10D, VOLATILITY_180D, VOLATILITY_360D from stocks where ticker = 'GOOG UW Equity' and date>= '2011-01-01' and CHG_PCT_1D is not NULL and PX_LAST is not NULL and PX_RATIO is not NULL and EBITDA is not NULL and PX_ASK is not NULL and PX_VOLUME is not NULL and PX_BID is not NULL and BOOK_VAL_PER_SH is not NULL and CHG_PCT_1D is not NULL and MOV_AVG_200D is not NULL and MOV_AVG_50D is not NULL and PX_HIGH is not NULL and PX_LOW is not NULL and DIVIDEND_YIELD is not NULL and DILUTED_EPS_AFT_XO_ITEMS_GROWTH is not NULL and EQY_FLOAT is not NULL and CUR_MKT_CAP is not NULL and PX_OPEN is not NULL and SALES_REV_TURN is not NULL and EQY_SH_OUT is not NULL and VOLATILITY_10D is not NULL and VOLATILITY_180D is not NULL and VOLATILITY_360D is not NULL ORDER BY date"
query = "select date, CHG_PCT_1D, PX_LAST, PX_RATIO, EBITDA, PX_ASK, PX_VOLUME, BOOK_VAL_PER_SH, PX_LOW, EQY_FLOAT, CUR_MKT_CAP, PX_OPEN, SALES_REV_TURN,VOLATILITY_10D, VOLATILITY_180D, VOLATILITY_360D, "
query += "uni1, uni2, uni3, uni5, uni6, uni7, uni8, uni9, uni10, uni11, uni12, uni13, uni14, uni15, uni16, uni17, uni18, uni19, uni20, uni21, uni22 , uni23, uni24, uni25, uni26, uni27, uni28, uni29, uni30,"
query += "bi1, bi2, bi3, bi4, bi5, bi6, bi7, bi8, bi9, bi10, bi11, bi12, bi13, bi14, bi15, bi16, bi17, bi18, bi19, bi20, bi21, bi22 , bi23, bi24, bi25, bi26, bi27, bi29, bi30,"
query += "tri1, tri2, tri3, tri4, tri5, tri6, tri7, tri8, tri9, tri10, tri11, tri12, tri13, tri14, tri15, tri16, tri17, tri18, tri19, tri20, tri21, tri22 , tri23, tri24, tri25, tri26, tri27, tri28, tri29, tri30,"
query += "feat1, feat2, feat3"
query += " from goog_info where ticker = 'GOOG UW Equity' and date>= '2009-01-01' ORDER BY date"
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

CVsize = round(.1 * len(x))

xt = x[0:len(x)-CVsize]
xc = x[len(x)-CVsize:len(x)]
