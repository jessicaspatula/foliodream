############################################################
# Kafka producer which 
# reads data from S3 bucket
# and forwards to broker topic. 
############################################################

from kafka import KafkaProducer
import time
import boto3
import botocore

def main():

        producer = KafkaProducer(bootstrap_servers = 'KAFKA_IP:9092')

        s3 = boto3.resource('s3', aws_access_key_id = 'AWS_ACCESS_KEY_ID', aws_secret_access_key = 'AWS_SECRET_ACCESS_KEY')
        bucket = s3.Bucket('historical-stock-data-insightds')

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

        return

if __name__ == '__main__':
        main()

