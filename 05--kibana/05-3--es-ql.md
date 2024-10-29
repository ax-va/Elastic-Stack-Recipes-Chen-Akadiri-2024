# ES|QL

An *ES|QL* query is composed of a series of commands chained together by pipes (`|`) like this
```es|ql
from <data_view>
| where <field> == <value>
| limit 50
```

Press `Ctrl + Enter` to run *ES|QL*.

## Commands

There are two types of commands:

- *source commands* to retrieve or generate data in the form of tables;

- *processing commands* to take a table as input and produce a new table as output.

| Source commands | Processing commands |
|-----------------|---------------------|
| `FROM`          | `DISSECT`           |
| `ROW`           | `DROP`              |
| `SHOW`          | `ENRICH`            |
|                 | `EVAL`              |
|                 | `GROK`              |
|                 | `KEEP`              |
|                 | `LIMIT`             |
|                 | `MV_EXPAND`         |
|                 | `RENAME`            |
|                 | `SORT`              |
|                 | `STATS...BY`        |
|                 | `WHERE`             |

## STATS...BY, SORT, EVAL, KEEP

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

## ENRICH

- Explanation:
```
                                                                              |
                                                                          input table
                                                                              V
[Source Indices] -> [Enrich Policy] -produces-> [Enrich Index] <-query- [Erich Command]
                                                                              |
                                                                          output table
                                                                              V
```

1. There should be at least one *source index*, which contains the enrich data 
the `ENRICH` command will use to add data to the input tables.

2. The *enrich index* is a read-only internal Elasticsearch-managed index to increase performance.

3. The *enrich policy* is a set of configurations describing how to add the enrich data to the input table.

- How to set up the source index used for enrichment:

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

## See also:

- https://elasticsearch-benchmarks.elastic.co/#tracks/esql/nightly/default/90d

- https://www.elastic.co/blog/introduction-to-esql-new-query-language-flexible-iterative-analytics
