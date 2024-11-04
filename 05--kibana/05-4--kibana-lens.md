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

See also:

- Examples of Kibana Formula:

https://www.elastic.co/blog/kibana-10-common-questions-formulas-time-series-maps

## Sampling

**Sampling** reduces the number of documents used for the aggregation.
This feature is based on random sampler aggregation.
The **Sampling** rate can be adjusted in **Layer settings**.

See also: 
https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-random-sampler-aggregation.html

## Annotation

E.g., in **Annotation query**, setting
```
max_speed=110 and traffic_status: "congested"
```
adds a layer of annotation to the visualization that marks data with numbered lines.

## TSVB

**TSVB (Time Series Visual Builder)** is deprecated in Elastic Stack 8.x. Use Kibana Lens instead.

See also:

- How to convert the existing TSVB visualizations to Kibana Lens visualizations: 
https://www.elastic.co/guide/en/kibana/current/tsvb.html#edit-visualizations-in-lens
