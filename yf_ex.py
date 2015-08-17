import yahoo_finance
import cPickle
import zlib
import sqlite3
import os
from datetime import datetime, date
def timenow():
	return datetime.now()
class db(object):
	"""Connect to a sqlite3 Database (default = 'test.db'.) and open cursor-object self.cur.
	Database name is stored in self.dbname.
	"""
	def __init__(self, dbname = "test.db"):
		self.dbname = dbname
		rows = self.rows = []
		try:
			self.conn = sqlite3.connect(self.dbname)
			self.cur = self.conn.cursor()
			print "Database %s open successfully" %(self.dbname)
		except:
			print "Can't open Databse!"
			return
	def close(self):
		self.conn.close()
		print "Database %s Closed!" %(self.dbname)
	def drop(self, tablename):
		"""drop table <tablename>"""
		self.tablename = None
		self.cur.execute("DROP TABLE IF EXISTS %s" % (tablename))
	def create(self, tablename, fields):
		"""Create table <tablename>, with fields <fields>.
		fields is stored in self.fields.
		"""
		self.tablename = tablename
		self.fields = fields
		#try:
		fields = str(fields)
		print fields
		self.cur.execute("CREATE TABLE IF NOT EXISTS %s %s;" % (self.tablename, fields))
		#except:
		#	print "Couldn't create table"
		#	return
	def insert(self, field, values):
		"""Insert <values> (of type tuple) into <fields> (tuple)"""
		self.values = str(timenow())+ "," + str(values)
		self.field = "TIMESTAMP, " +field
		if not self.tablename:
			print "Please create a table first..."
			return
		#try:
		self.cur.execute("INSERT INTO %s(\"%s\") VALUES (\"%s\");" % (self.tablename, self.field, self.values))
		#self.cur.execute("INSERT INTO %s VALUES (\"%s\");" % (self.tablename, self.values))
		self.conn.commit()
		#except:
		#	print "Could not insert values!"
		#	return
	def query(self, req, tablename):
		"""Query db on str <req> and store result in self.rows."""
		self.req = req
		if self.tablename !=None:
			self.cur.execute("SELECT %s FROM %s;" %(self.req, self.tablename))
		else:
			print "Sorry Table does not exist!"
		rows = self.cur.fetchall()
		self.rows = rows
		if rows:
			for row in rows:
				print row
	def commit(self):
		self.conn.commit()
class db_dict(db):
	""" Extends Class db by dict functionality."""
	def listify(self, ydict):
		"""Parameter ydict is a dict of a Share object (yahoo-finance). 
			It delets the double entry "Symbol" and keeps column (key) "symbol".
			keys are stored in self.keys, values of the ydict are stored in self.values."""
		self.ydict = ydict
		self.keys = []
		self.values = []
		for k in self.ydict:
			if k != "Symbol":
				self.keys.append(k)
		for i in self.keys:
			if self.ydict[i] == None:
				self.ydict[i] = "None"
			if i != "Symbol":
				self.values.append(self.ydict[i])
	def create_dict_table(self, tablename, ydict):
		"""Creates a table from a yahoo-result dict.
			<tablename> (str)
			<ydict> yahoo-finance module resulting dict."""
		self.tablename = tablename
		self.listify(ydict)

		c = ("TIMESTAMP",)
		self.fields =  tuple(self.keys)
		print "FIELDS: ", self.fields
		self.create(self.tablename, self.fields)
	def insert_by_keylist(self, tablename, ydict, keylist):
		
		"""Insert Values of <ydcit> (dict) into <tablename> (str) by <KEYLIST> (list).
		"""
		self.tablename = tablename
		d = tuple(keylist)
		f = []
		for k in keylist:
			if ydict[k] !=None and ydict[k] != "None":
				f.append(ydict[k])
			else:
				ydict[k] = "NULL"
				f.append("NULL")
		b = tuple(f)
		c = (str(timenow()),)
		e = ("TIMESTAMP",)
		#b = tuple(self.values)
		#d = tuple(self.keys
		
		print "Number of Values", len(b), "Number of Columns", len(d)
		if len(b) == len(d) and "None" not in d and None not in d:
			print d
			print b
			print "____________________________________________________________________"
			print "INSERT INTO %s(\"%s\") VALUES %s;" % (self.tablename, d, b)
			
			#if len(b) ==83:
			self.cur.execute("INSERT INTO %s VALUES %s;" % (self.tablename, b))
		else:
			print "Not enough arguments!"

	def insert_dict_values(self, tablename, ydict):
		"""Insert Values of <ydcit> (dict) into <tablename> (str).
		"""
		self.listify(ydict)
		self.tablename = tablename
		c = (str(timenow()),)
		e = ("TIMESTAMP",)
		b = tuple(self.values)
		d = tuple(self.keys)
		print d
		print b
		print "____________________________________________________________________"
		print "INSERT INTO %s(\"%s\") VALUES %s;" % (self.tablename, d, b)
		print "Number of Values", len(b), "Number of Columns", len(d)
		#if len(b) ==83:
		self.cur.execute("INSERT INTO %s VALUES %s;" % (self.tablename, b))
		
		#c = tuple(self.ydict.keys())
		#print c, b
		#d = zip(c,b)
class db_read(db_dict):
	def __init__(self):
		super(db, delf).__init__()
class flush_yahoo_data(object):
	def __init__(self, x ,y, filename_keys = "flush_keys.yahoo", filename_values = "flush_values.yahoo"):
		self.x = x
		self.y = y
		with open(filename_keys, "wb") as xf:
			z1 = cPickle.dump(x, xf)
		with open(filename_values, "wb") as yf:
			z2 = cPickle.dump(y, yf)
	def check(self):
		return os.system("ls *.yahoo")
class load_yahoo_data(object):
	def __init__(self, filename_keys = "flush_keys.yahoo", filename_values = "flush_values.yahoo"):
		self.keys = []
		self.values = []
		with open(filename_keys, "r") as x:
			self.keys.append(x.readlines())
		with open(filename_values, "r") as y:
			self.values.append(y.readlines())
		z = zip(self.keys, self.values)
		print "-------------------------------------"
		print "Keys/Values:"
		print "============="
		print z
class save_obj(object):
	"""Dump cPickle pf <o> (Object) into <filename> (file)."""
	def __init__(self, o, filename):
		with open(filename, "wb") as f:
			cPickle.dump(o, f)
class save_info(object):
	def __init__(self, sym):
		self.sym = sym
		self.info = yahoo_finance.Share(sym)
		self.filename = sym + ".txt"
		self.save = save_obj(self.info, self.filename)
class Info(object):
	def __init__(self, sym):
		self.timestamp = timenow()
		self.info = yahoo_finance.Share(sym)	
class load_obj(object):
	def __init__(self, sym):
		self.sym = sym
		filename = sym + ".txt"
		with open(filename, "wb") as f:
			self.info = cPickle.load(filename)
class update(object):
	def __init__(self, tablename = "trading", symbollist = "./symbols.txt"):
		self.symbollist = symbollist
		l = yahoo_finance.Share("YHOO")
		s = l.data_set
		self.db = db_dict()
		self.db.create_dict_table(tablename,s)
		self.syms = []
		with open(self.symbollist, "r") as s:
			for line in s:
				if line != None and line != "" and line != "\n":
					self.syms.append(line.strip("\n"))
		print self.syms
		for i in self.syms:
			share = yahoo_finance.Share(i)
			s = share.data_set

			self.db.insert_dict_values(tablename,s)
			self.db.conn.commit()
		self.db.query("*", "*")
class update_trading(object):
	def __init__(self, tablename, symbollist = "./symbols.txt"):
		self.symbollist = symbollist
		self.db = db_trading("trading.db")
		self.db.create(tablename)

		self.syms = []
		with open(self.symbollist, "r") as s:
			for line in s:
				if line != None and line != "" and line != "\n":
					self.syms.append(line.strip("\n"))
		print self.syms
		for i in self.syms:
			share = yahoo_finance.Share(i)
			s = share.data_set
			s["TIMESTAMP"] = str(timenow())
			o = self.db.prepare_dict(s)
			print self.db.okeys
			self.db.insert_by_keylist(tablename, o, self.db.okeys)
			#self.db.insert_dict_values(tablename,s)
			self.db.conn.commit()
		self.db.query("*", "*")
		self.db.close()
class db_scheme(db):
	def __init__(self):
		super(db_scheme, self).__init__()
	def create(self, tablename):
		self.tablename = tablename
		self.scheme = """
			CREATE TABLE IF NOT EXISTS %s ( 
				ID                              INTEGER PRIMARY KEY,
				TIMESTAMP                                           DATE,
			    YearLow                                        REAL,
			    OneyrTargetPrice                               REAL,
			    DividendShare                                  REAL,
			    ChangeFromFiftydayMovingAverage                REAL,
			    FiftydayMovingAverage                          REAL,
			    SharesOwned                                    INT,
			    PercentChangeFromTwoHundreddayMovingAverage,
			    PricePaid                                      REAL,
			    DaysLow                                        REAL,
			    DividendYield                                  REAL,
			    Commission                                     REAL,
			    EPSEstimateNextQuarter                         REAL,
			    ChangeFromYearLow                              REAL,
			    ChangeFromYearHigh                             REAL,
			    EarningsShare                                  REAL,
			    AverageDailyVolume                             INT,
			    LastTradePriceOnly                             REAL,
			    YearHigh                                       REAL,
			    EBITDA                                         REAL,
			    Change_PercentChange,
			    AnnualizedGain,
			    ShortRatio                                     REAL,
			    LastTradeDate                                  REAL,
			    PriceSales                                     REAL,
			    EPSEstimateCurrentYear                         REAL,
			    BookValue                                      REAL,
			    LASTTRADEDATETIMEUTC,
			    Bid                                            REAL,
			    AskRealtime                                    REAL,
			    PreviousClose                                  REAL,
			    DaysRangeRealtime                              REAL,
			    EPSEstimateNextYear                            REAL,
			    Volume                                         INT,
			    HoldingsGainPercent,
			    PercentChange,
			    TickerTrend,
			    Ask                                            REAL,
			    ChangeRealtime                                 REAL,
			    PriceEPSEstimateNextYear                       REAL,
			    HoldingsGain                                   REAL,
			    Change                                         REAL,
			    MarketCapitalization                           REAL,
			    Name                                           TEXT,
			    HoldingsValue                                  REAL,
			    DaysRange                                      TEXT,
			    AfterHoursChangeRealtime,
			    symbol                                         TEXT,
			    ChangePercentRealtime,
			    DaysValueChange                                REAL,
			    LastTradeTime,
			    StockExchange                                  TEXT,
			    DividendPayDate                                DATE,
			    LastTradeRealtimeWithTime,
			    Notes                                          TEXT,
			    MarketCapRealtime                              REAL,
			    ExDividendDate                                 DATE,
			    PERatio                                        REAL,
			    DaysValueChangeRealtime                        REAL,
			    ErrorIndicationreturnedforsymbolchangedinvalid,
			    ChangeinPercent,
			    HoldingsValueRealtime                          REAL,
			    PercentChangeFromFiftydayMovingAverage,
			    PriceBook                                      REAL,
			    ChangeFromTwoHundreddayMovingAverage,
			    DaysHigh,
			    PercentChangeFromYearLow,
			    TradeDate,
			    LastTradeWithTime,
			    BidRealtime,
			    YearRange,
			    HighLimit,
			    OrderBookRealtime,
			    HoldingsGainRealtime,
			    PEGRatio,
			    Currency,
			    LowLimit,
			    HoldingsGainPercentRealtime,
			    TwoHundreddayMovingAverage,
			    PERatioRealtime,
			    PercebtChangeFromYearHigh,
			    Open,
			    PriceEPSEstimateCurrentYear,
			    MoreInfo 
			);

			""" % (self.tablename)
		self.cur.execute(self.scheme)
class db_trading(db_scheme, db_dict, db):
	def __init__(self, dbname = "test.db"):
		super(db_trading, self).__init__()
	def create(self, tablename):
		self.tablename = tablename
		#ID                              INTEGER PRIMARY KEY,
		self.scheme = """
			CREATE TABLE IF NOT EXISTS %s ( 
				
				TIMESTAMP                                           TEXT,
				symbol                                         TEXT,
				Name                                           TEXT,
				PreviousClose                                  REAL,
				YearRange                                      TEXT,
				YearLow                                        REAL,
				YearHigh                                       REAL,
				ChangeFromYearLow                              REAL,
				PercentChangeFromYearLow,
				ChangeFromYearHigh                             REAL,
				PercebtChangeFromYearHigh,
				Volume                                         INT,
				AverageDailyVolume                             INT,
				ShortRatio                                     REAL,
				PEGRatio                                       REAL,
			    FiftydayMovingAverage                          REAL,
			    TwoHundreddayMovingAverage                     REAL,
			    PriceSales                                     REAL,
			    BookValue                                      REAL,
			    MarketCapitalization                           REAL,
			    PriceBook                                      REAL,
			    Currency                                       TEXT);
			""" % (self.tablename)
		self.cur.execute(self.scheme)
	def prepare_dict(self, ydict):
		self.ndict = {}
		self.keylist = ["symbol", "Name", "PreviousClose","YearRange","YearLow","YearHigh", "ChangeFromYearLow", "PercentChangeFromYearLow", "ChangeFromYearHigh", "PercebtChangeFromYearHigh","Volume", "AverageDailyVolume","ShortRatio",
"PEGRatio","FiftydayMovingAverage","TwoHundreddayMovingAverage","PriceSales","BookValue","MarketCapitalization","PriceBook","Currency"]
		self.okeys = ["TIMESTAMP"] + self.keylist
		self.ndict["TIMESTAMP"] = str(timenow())
		for k in self.keylist:
			self.ndict[k] = ydict[k]
			print k, self.ndict[k]
		return self.ndict
if __name__ == "__main__":
	#share = yahoo_finance.Share("YHOO")
	#d = share.data_set
	#d["TIMESTAMP"] = str(timenow())
	#db = db_dict()
	#db.tablename = "newtest"
	#db.create_dict_table(db.tablename, d)
	#db.insert_dict_values(db.tablename, d)
	#db.query("*", "*")
	#db.commit()
	#db.close()
	#print db.rows
	#db.conn.commit()
	#syms = update()
	#newtable = db_trading()
	#newtable.create("yahoofinance")
	a = update_trading("trading")
	#d2 = newtable.prepare_dict(d)
	#newtable.insert_by_keylist(newtable.tablename,d2, newtable.okeys)
	#newtable.query("*","*")
	#newtable.commit()
	#que = db_trading()
	#que.tablename = "yahoofinance"
	#que.query("*","*")
	#que.close()

	


