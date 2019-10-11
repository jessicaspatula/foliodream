from __future__ import print_function
import os
import sys
import json

from pyspark import SparkContext

from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql import Row
import stock_trends

import spark_kafka_keys as skk

ss = stock_trends.stock_stats()
sflags =  ss.flags

if __name__ == "__main__":

    sc = SparkContext(appName="StreamingDirectKafkaStockMetrics")
    ssc = StreamingContext(sc, 1)

    topic   = "stock-update"
    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": skk.brokers})
    
    # Convert Stream to JSON
    # Group updates by Stock Symbol
    # Retain only most recent update for any stock
    data = kvs.map(lambda x: json.loads(x[1])).map(lambda x: ( x["symbol"],x)).reduceByKey(lambda x,y: max((x, y), key=lambda x: x['timestamp']))

    # Subset stocks that are not flagged
    # Flag stocks that demonstrate a buying opportunity
    unflagged = data.filter(lambda (sym,x):  not  sflags.get(sym,{"BUY":False})["BUY"] and not sflags.get(sym,{"SELL":False})["SELL"])
    watchable_buy = unflagged.filter(lambda (sym,x): sym in sflags and  x['price'] < sflags[sym]["LOW"] )   
    watchable_buy.foreachRDD(lambda r: r.foreach(ss.flag_buy))
    watchable_sell = unflagged.filter(lambda (sym,x): sym in sflags and  x['price'] > sflags[sym]["HIGH"] )   
    watchable_sell.foreachRDD(lambda r: r.foreach(ss.flag_sell))

    # Subset of stocks that are flagged for buying opportunities
    # Filter flags for BUY opportunity values 
    buy_opp = data.filter(lambda (sym,x):   sflags.get(sym,{"BUY":False})["BUY"]).filter(lambda (sym,x): x['price'] > sflags[sym]["LOW"] )

    # Subset of stocks that are flagged for SELL opportunities
    # Filter flags for SELL opportunity values
    sell_opp = data.filter(lambda (sym,x):   sflags.get(sym,{"SELL":False})["SELL"]).filter(lambda (sym,x): x['price'] > sflags[sym]["HIGH"] )

    # Unset watch flag and save opportunity to db
    buy_opp.foreachRDD(lambda r: r.foreach(ss.set_buy_opp))
    buy_opp.foreachRDD(lambda rdd: rdd.foreachPartition(stock_trends.save_opportunity))
    sell_opp.foreachRDD(lambda r: r.foreach(ss.set_sell_opp))

    ssc.start()
    ssc.awaitTermination()
