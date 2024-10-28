# ES|QL

Press `Ctrl + Enter` to run *ES|QL*.

Chain processing with the pipe (`|`)
```es|ql
from <data_view>
| where <field> == <value>
| limit 50
```

## stats...by, sort, eval, keep

Use `stats...by` to average `traveltime.duration` in `denomination` groups and 
`sort` to sort in descending order
```es|ql
from metrics-rennes_traffic-raw
| where traffic_status == "congested"
| stats avg_traveltime = avg(traveltime.duration) by denomination
| sort avg_traveltime desc
| limit 50
```
-> The `avg_traveltime` and `denomination` fields will be shown.

Convert seconds into minutes.
`keep` specifies what columns are returned as well as their order.
```es|ql
from metrics-rennes_traffic-raw
| where traffic_status == "congested"
| stats avg_traveltime = avg(traveltime.duration) by denomination
| eval avg_traveltime_min = round(avg_traveltime/60)
| sort avg_traveltime_min desc
| keep denomination, avg_traveltime_min
| limit 50
```
-> The `denomination` and `avg_traveltime_min` fields will be shown.

## enrich

An enrich policy defines how to combine multiple indices for enrichment.

To set up the source index used for enrichment:
1. In **Kibana**, navigate to **Home** -> **Upload a file** and select `05--kibana/data/insee-postal-codes.csv`.

2. On the **Import data** page, click on the **Advanced** tab, name the index `enrich-insee-codes`, and replace the default **Mappings** with:
```json
{
  "properties": {
    "code_postal": {
      "type": "keyword"
    },
    "insee": {
      "type": "keyword"
    },
    "libelle_acheminement": {
      "type": "keyword"
    },
    "ligne_5_adresse_postale": {
      "type": "keyword"
    },
    "nom_de_la_commune": {
      "type": "keyword"
    }
  }
}
```
Then,  the index is available in **Discover**.

3. Navigate to **Management** -> **Dev Tools**. In **Console**, define the request:
```
PUT /_enrich/policy/rennes-data-enrich
{
  "match": {
    "indices": [
      "enrich-insee-codes"
    ],
    "match_field": "insee",
    "enrich_fields": [
      "code_postal",
      "nom_de_la_commune"
    ]
  }
}
```
Press `Shift + Enter` to finish.
Then, execute the request:
```
PUT /_enrich/policy/rennes-data-enrich/_execute
```

4. To validate navigate to **Stack Management** -> **Index Management** -> **Enrich Policies** and see the enrich policy.

Use the `enrich` command to enrich `metrics-rennes_traffic-raw` with `code_postal` and `nom_de_la_commune` from `insee`:
```
from metrics-rennes_traffic-raw
| where traffic_status == "congested"
| enrich rennes-data-enrich on insee with code_postal, nom_de_la_commune
| keep average_vehicle_speed, code_postal, nom_de_la_commune, denomination
| sort average_vehicle_speed desc
| limit 50
```

Use the newly added fields for aggregation:
```
from metrics-rennes_traffic-raw
| where traffic_status == "congested"
| enrich rennes-data-enrich on insee with code_postal, nom_de_la_commune
| stats avg_traveltime = avg(traveltime.duration) by nom_de_la_commune
| sort avg_traveltime desc
| limit 50
```

