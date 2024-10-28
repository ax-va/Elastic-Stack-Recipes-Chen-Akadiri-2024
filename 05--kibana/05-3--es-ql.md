## ES|QL

Press `Ctrl` + `Enter` to run ES|QL.

Chain processing with the pipe (`|`)
```es|ql
from <data_view>
| where <field> == <value>
| limit 50
```

Use `stats...by` to average `traveltime.duration` in `denomination` groups and 
`sort` to sort in descending order
```es|ql
from metrics-rennes_traffic-raw
| where traffic_status == "congested"
| stats avg_traveltime = avg(traveltime.duration) by denomination
| sort avg_traveltime desc
| limit 50
```

