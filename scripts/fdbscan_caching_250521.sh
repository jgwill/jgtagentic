#!/bin/bash

. /opt/binscripts/load.sh

# The goal is a simple scan with caching in current directory so we can use the CDS charting data in other apps such as TrinityTrading
#
log_outfile=logs/fdbscan_$(tlid min).log.md
mkdir -p logs
export cache_dir=cache

for i in EUR/USD AUD/USD SPX500;do 
	echo "## Scanning : $i  "
	for t in H4 H1 m15;do 
		echo "### Scanning timeframe: $t  "
		JGT_CACHE=$cache_dir fdbscan -i $i -t $t
		echo "----"
	done
	echo "----"
done | tee $log_outfile && \
	echo "## Finished scanning" && \
	echo "## Log file: $log_outfile" && \
	echo "## Cache directory: $cache_dir" || \
	echo "## Error during scanning"
# EOF
#

