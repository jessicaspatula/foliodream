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
from producer_keys import KAFKA_IP, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

def main():


        # get producer
        producer = KafkaProducer(bootstrap_servers = (KAFKA_IP) + ':9092', api_version=(1,0,0))

        # get bucket
        # s3 = boto3.resource('s3', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
        s3 = boto3.resource('s3')
        #bucket = s3.Bucket('historical-stock-data-insightds')

        # get list of historical trading days
        tradingdays = open("../historical_data/tradingdays.txt","r") 

        #with open("../../historical_data/tradingdays.txt") as tradingdays:
        for day in tradingdays: 
               #line = fp.readline()
               s3_object = s3.Object('historical-stock-data-insightds',day.rstrip() +'.pcap')
               #historical-stock-data-insightds
               pcappath = 'https://s3-us-west-2.amazonaws.com/historical-stock-data-insightds/' + day.rstrip() + '.pcap'

               iex_parser = Parser(pcappath)
               print(day)

        '''
        #t bucket contains a list of csv links that point to data for each hour of trading
        # access each pcap file
        for object in bucket.objects.all():
                pcap = 'https://s3-us-west-2.amazonaws.com/historical-stock-data-insightds/' + object.key
                data = pd.read_csv(pcap)
                #read through pcap and send each update to the kafka topic
                for index, row in data.iterrows():
                    output = ''
                    for element in row:
                        output = output + str(element) + "^"
                        producer.send('stock-update', output.encode())
                        producer.flush()
        '''

        return

if __name__ == '__main__':
        main()

