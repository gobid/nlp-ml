import xlrd
import _mysql
import time
import datetime
import multiprocessing

db = _mysql.connect('localhost', 'root', 'glassesandhair', "stocks")

#wb = xlrd.open_workbook('2013.xls', formatting_info=True)
#sh = wb.sheet_by_index(0);

numfeatures = 28

def parseStock(startRow):
	print startRow
	stockName = sh.cell(startRow,0).value
	i = 1;
	while i < sh.ncols and (sh.cell_type(startRow+1, i) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK)):
		insertQuery = "INSERT INTO stocks VALUES('" + stockName + "',"
		for j in range(1,numfeatures+2):
			if sh.cell_type(startRow+j,i) == xlrd.XL_CELL_DATE and j == 1:
				year, month, day, hour, minute, second = xlrd.xldate_as_tuple(sh.cell(startRow+j,i).value, wb.datemode)
				date = datetime.datetime(year, month, day, hour, minute, second)
				insertQuery = insertQuery + "'" + date.strftime("%Y-%m-%d %H:%M:%S") + "'"
			elif sh.cell(startRow+j,i).value != "#N/A N/A":
				insertQuery = insertQuery + str(sh.cell(startRow+j,i).value)
			else:
				insertQuery = insertQuery + "NULL"

			if j < (numfeatures + 1):
				insertQuery = insertQuery + ","

		insertQuery = insertQuery + ")"
		try:
			db.query(insertQuery)
		except Exception, e:
			print repr(e)
		i = i + 1

#for rownum in range(0, sh.nrows, numfeatures+3):
#	parseStock(rownum)
for data in ('2010Q3.xls', '2010Q1.xls', '2009Q3.xls', '2009Q1.xls'):
	print data
	wb = xlrd.open_workbook(data, formatting_info=True)
	sh = wb.sheet_by_index(0);
	pool = multiprocessing.Pool(4)
	pool.map(parseStock, range(0, sh.nrows, numfeatures+3))
