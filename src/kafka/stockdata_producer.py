###########################################################
# Kafka producer 
# * Reads data from S3 bucket
# * Reformats data into json 
# * Forwards to broker topic. 
##########################################################

from kafka import KafkaProducer
from datetime import datetime
import time
import boto3
import botocore
from IEXTools import IEXAPI
from IEXTools import Parser, messages
import sys
from io import BytesIO
import binascii
from producer_keys import KAFKA_IP, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

trading_days_fp = "tradingdays.txt"
BUCKET='historical-stock-data-insightds'

def main():
        # get producer
        producer = KafkaProducer(bootstrap_servers = (KAFKA_IP) + ':9092', api_version=(1,0,0))

        with open(trading_days_fp) as tradingdays:
          for day in tradingdays:
               day_key = day.rstrip() +'.pcap' 
               day_path = "historical_data/" + day_key
               iex_parser = Parser(day_path)
               allowed = [messages.TradeReport]
               leng=0
               while True:
                  output = ''
                  iex_parser.get_next_message(allowed)
                  leng += 1
                  timestamp = datetime.fromtimestamp(iex_parser.message.timestamp/(10**9))
                  output = str(iex_parser.message.flags) + \
                        str(iex_parser.message.timestamp) + \
                         str(iex_parser.message.symbol) + \
                        str(iex_parser.message.size) + \
                        str(iex_parser.message.price_int) + \
                        str(iex_parser.message.trade_id)
                  producer.flush()

        return

if __name__ == '__main__':
        main()
