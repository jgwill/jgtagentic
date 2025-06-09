---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---


# Entry Signal Details
## Trade Information
- **Entry Rate:** 1.36194
- **Stop Rate:** 1.35708
- **Buy/Sell:** B
- **Lots:** 1
- **Tlid ID:** 240822190651
- **Instrument:** USD/CAD
- **Timeframe:** D1

![](charts/signal.png)
[M1](charts/M1.png)-[W1](charts/W1.png)-[D1](charts/D1.png)-[H4](charts/H4.png)-[H1](charts/H1.png)-[m15](charts/m15.png)-[m5](charts/m5.png)

----
## Utilities

+++

* [entry.sh](.jgt/entry.sh)
* [cancel.sh](.jgt/cancel.sh)
* [watch.sh](.jgt/watch.sh)
* [status.sh](.jgt/status.sh)
* [update.sh](.jgt/update.sh)
* [env.sh](.jgt/env.sh)
* Other scripts might include: .jgt/mv.sh, .jgt/rmtrade.sh, .jgt/xtrail.sh, .jgt/xfdb.sh

### CLI Commands

```{code-cell}
#.jgt/env.sh
#fxtr -id $OrderID $demo_arg
#fxrmorder -id $OrderID $demo_arg
#fxclosetrade -tid $trade_id $demo_arg
#fxtr -id $OrderID $demo_arg
#jgtapp fxwatchorder -id $OrderID  -d $bs \$demo_arg
#jgtapp fxmvstop -tid $trade_id -x $1 $demo_arg
#jgtapp fxrmtrade -tid $trade_id  $demo_arg
#jgtapp fxmvstopgator -tid $trade_id -i $instrument -t $timeframe --lips $demo_arg
#jgtapp fxmvstopfdb -tid $trade_id -i $instrument -t $timeframe  $demo_arg
#jgtapp fxstatusorder -id $OrderID  $demo_arg
```

#### More

* run 

```{code-cell}
#mkdir -p helps
#jgtapp --help > helps/jgtapp.txt
#fxtr --help > helps/fxtr.txt
```

### --@STCIssue Future Enhancements
* CLI Commands to run, not hard coded scripts
* Example : _fxtrupdate, _jgtsession_mksg, _jgtsession_vswsopen, _jgtsession_mkads_ctx_timeframe, _jgtsession_mkads_all_timeframes

+++

## Signal Bar Data
| Metric           | Value         |
|------------------|---------------|
| BidOpen | 1.35942 |
| BidHigh | 1.36188 |
| BidLow | 1.3571 |
| BidClose | 1.36148 |
| AskOpen | 1.35958 |
| AskHigh | 1.36192 |
| AskLow | 1.35715 |
| AskClose | 1.36162 |
| Volume | 188332 |
| Open | 1.3595 |
| High | 1.3619 |
| Low | 1.357125 |
| Close | 1.36155 |
| Median | 1.3595125 |
| ao | -0.41322822628 |
| ac | -0.5040125002 |
| jaw | 1.37653125838 |
| teeth | 1.37509249308 |
| lips | 1.37125410557 |
| bjaw | 1.3606915742 |
| bteeth | 1.3647034811 |
| blips | 1.36958843916 |
| tjaw | 1.32087907465 |
| tteeth | 1.33945637297 |
| tlips | 1.3527929183 |
| fh | 0 |
| fl | 0 |
| fh3 | 0 |
| fl3 | 0 |
| fh5 | 0 |
| fl5 | 0 |
| fh8 | 0 |
| fl8 | 0 |
| fh13 | 0 |
| fl13 | 0 |
| fh21 | 0 |
| fl21 | 0 |
| fh34 | 0 |
| fl34 | 0 |
| fh55 | 0 |
| fl55 | 0 |
| fh89 | 0 |
| fl89 | 0 |
| mfi | 0.00253541618 |
| fdbb | 1 |
| fdbs | 0 |
| fdb | 1 |
| aoaz | 0 |
| aobz | 1 |
| zlc | 0.0 |
| zlcb | 0.0 |
| zlcs | 0.0 |
| zcol | red |
| zone_sig | -1.0 |
| sz | 1.0 |
| bz | 0.0 |
| acs | 0.0 |
| acb | 0.0 |
| ss | 0.0 |
| sb | 0.0 |
| price_peak_above | 0 |
| price_peak_bellow | 0 |
| ao_peak_above | 0 |
| ao_peak_bellow | 0 |
| mfi_sq | 0 |
| mfi_green | 0 |
| mfi_fade | 0 |
| mfi_fake | 1 |
| mfi_sig | 2 |
| mfi_str | -+ |

+++

## Current Bar Data
| Metric           | Value         |
|------------------|---------------|
| BidOpen | 1.36148 |
| BidHigh | 1.36161 |
| BidLow | 1.36055 |
| BidClose | 1.36064 |
| AskOpen | 1.36162 |
| AskHigh | 1.36194 |
| AskLow | 1.36059 |
| AskClose | 1.36068 |
| Volume | 2716 |
| Open | 1.36155 |
| High | 1.361775 |
| Low | 1.36057 |
| Close | 1.36066 |
| Median | 1.3611725 |
| ao | -0.45958427633 |
| ac | -0.44677523378 |
| jaw | 1.37608135389 |
| teeth | 1.37425624395 |
| lips | 1.36946378446 |
| bjaw | 1.36079793291 |
| bteeth | 1.36472578144 |
| blips | 1.37004561742 |
| tjaw | 1.32101644448 |
| tteeth | 1.33949340571 |
| tlips | 1.35289524179 |
| fh | 0 |
| fl | 0 |
| fh3 | 0 |
| fl3 | 0 |
| fh5 | 0 |
| fl5 | 0 |
| fh8 | 0 |
| fl8 | 0 |
| fh13 | 0 |
| fl13 | 0 |
| fh21 | 0 |
| fl21 | 0 |
| fh34 | 0 |
| fl34 | 0 |
| fh55 | 0 |
| fl55 | 0 |
| fh89 | 0 |
| fl89 | 0 |
| mfi | 0.04436671576 |
| fdbb | 0 |
| fdbs | 0 |
| fdb | 0 |
| aoaz | 0 |
| aobz | 1 |
| zlc | 0.0 |
| zlcb | 0.0 |
| zlcs | 0.0 |
| zcol | gray |
| zone_sig | 0.0 |
| sz | 0.0 |
| bz | 0.0 |
| acs | 0.0 |
| acb | 0.0 |
| ss | 0.0 |
| sb | 0.0 |
| price_peak_above | 0 |
| price_peak_bellow | 0 |
| ao_peak_above | 0 |
| ao_peak_bellow | 0 |
| mfi_sq | 0 |
| mfi_green | 0 |
| mfi_fade | 0 |
| mfi_fake | 1 |
| mfi_sig | 2 |
| mfi_str | -+ |
