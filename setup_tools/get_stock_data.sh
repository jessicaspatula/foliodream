#!/bin/bash

# created: GB June 2019

# Time-stamp: <2019-06-01 10:50:47 giulio>

#obtain the list of companies
#wget --output-document=companies.txt 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'

#filter pharma firms
#tickers=$( gawk -F, '{ if($7=="\"Major Pharmaceuticals\""){ gsub(/"/,"",$1); print $1} }' companies.txt )

tickers=$(cat NASDAQ_partb.txt | cut -d "	" -f 1 | uniq)

#download data and save in file
for ticker in $tickers; do
    #wget --output-document=${ticker}_.csv "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=${ticker}&apikey=[APIKEY]&datatype=csv"
    wget --output-document=${ticker}.csv "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=${ticker}&apikey=JC126XLFNMZD037I&datatype=csv"
					 #https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=MSFT&apikey=JC126XLFNMZD037I&datatype=csv
    #wget --output-document=${ticker}.csv "http://jessicamontoya.com"
    
    #echo "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=${ticker}&apikey=[APIKEY]&datatype=csv"
    sleep 13s
done
