. /opt/binscripts/load.sh

LOG_FILE=/var/log/jgt/fdbscan.log
LOG_ENABLED=y

#v=$2
#if [ -z $v ]; then
#	v=0
#fi
v=""
n="-N"

fdbscan -t $1 $v  && log_info "FDB Scan completed for $1" || log_error "FDB Scan failed for $1"

_fdbscan_m5()
{
    fdbscan -t m5 $v  && log_info "FDB Scan completed for m5" || log_error "FDB Scan failed for m5"
}
_wtf_m5x()
{
    #local _n="$1"
    #if [ -z $_n ]; then
#	_n="-N"
#    fi
    wtf -t m5 -X $n && log_info "WTF m5 arrived. Clean exit." || log_error "WTF failed for m5"
}

if [ "$1" == "m15" ]; then
	# happens at :00,:15,:30,:45
	_fdbscan_m5
	#waits for :05,:20,:35,:50
    _wtf_m5x
	_fdbscan_m5
	#waits for :10,:25,:40,:55
	_wtf_m5x
	_fdbscan_m5
	#Then we are back to the wtf -t m15

fi


 

