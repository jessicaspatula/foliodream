from IEXTools import IEXAPI
from IEXTools import Parser, messages
from datetime import datetime
import sys

filedate = sys.argv[1] + ".pcap"

print ("the script has the name %s" % (sys.argv[1]))

#api = IEXAPI()
#p = Parser(r'data_feeds_20190924_20190924_IEXTP1_TOPS1.6.pcap')
p = Parser(filedate)
allowed = [messages.TradeReport]
#for i in range(20):
leng=0
while True:
  p.get_next_message(allowed)
  leng += 1
  timestamp = datetime.fromtimestamp(p.message.timestamp/(10**9))
  print(timestamp,leng)
  #print(p.message)

