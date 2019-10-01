#!/usr/bin/env bash

# ###
# For each available IEX HIST file
# Download the archive file
# Gunzip file
# upload to S3
# delete gz and pcap files

BASEURL="https://www.googleapis.com/download/storage/v1/b/iex/o/data%2Ffeeds%2F"

dllinks=$(cat ../historical_data/iexfilelist_incomplete.txt |  uniq)

trap "exit" INT
for link in $dllinks; do
  fname=$(echo $link | cut -d "%" -f 1 )
  fulllink=${BASEURL}${link}"&alt=media"
  echo $fulllink
  curl -o $fname.pcap.gz $fulllink &
  wait %1
  gunzip $fname.pcap.gz &
  wait %1
  aws s3 cp $fname.pcap s3://historical-stock-data-insightds/
  wait %1
  rm $fname.pcap $fname.pcap.gz
done

