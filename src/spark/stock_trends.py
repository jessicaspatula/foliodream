from __future__ import print_function
import re
import psycopg2
import pgcopy
import postgres_keys as pgk

def save_opportunity(rdd):
        connection = psycopg2.connect(host = pgk.host , database = pgk.database, user = pgk.user, password = pgk.password )
        cursor = connection.cursor()

        for line in rdd:
                query = 'INSERT INTO trade_opportunity (stock_symbol,type,price) VALUES (%s, %s, %s)'
                data = (str(line[0]), 'BUY',  line[1]['price'])
                cursor.execute(query, data)
                
        #close db connection
        connection.commit()
        connection.close()

class stock_stats(object):
    def __init__(self):
        self.flags = self.get_stock_flags() 

    def get_stock_flags(self):
        f = open("stocklist.txt", "r")
        flags = {}
        for x in f:
           line = re.split(r'\t+', x)
           flags[unicode(line[0],"utf-8")] = {"BUY":False,"SELL":False,"HIGH": 0, "LOW": 0}
        return flags

    def set_buy_opp(self,(sym,x)):
	self.flags[sym]["BUY"] = False

    def set_sell_opp(self,(sym,x)):
	self.flags[sym]["SELL"] = False

    def flag_buy(self,(sym,x)):
	self.flags[sym]["BUY"] = True 

    def flag_sell(self,(sym,x)):
	self.flags[sym]["SELL"] = True
        
