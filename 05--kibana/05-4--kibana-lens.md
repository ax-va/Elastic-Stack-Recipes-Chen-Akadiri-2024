# Kibana Lens

Kibana Lens offers a UI for creating charts. 

**Kibana** -> **Analytics** -> **Visualize Library** -> **Create visualization** -> **Lens**

Use the drag-and-drop actions for data-view fields on the left panel and chart configurations on the right panel.

## Formula

**Formula** offers to combine aggregation and mathematical functions, e.g.,

```
percentile(average_vehicle_speed, percentile=99) / percentile(average_vehicle_speed, percentile=99, shift='1w')
```
where `average_vehicle_speed` is a data-view field.

## Sampling

**Sampling** reduces the number of documents used for the aggregation.
This feature is based on random sampler aggregation.
The **Sampling** rate can be adjusted in **Layer settings**.

See also: 
https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-random-sampler-aggregation.html