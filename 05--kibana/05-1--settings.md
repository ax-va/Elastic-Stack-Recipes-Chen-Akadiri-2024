## Kibana settings

- Set up in `kibana.yml` more rows to export in CSV 
(in `Discover` with top-right `Share` -> `CSV Reports` -> `Generate csv`)
```yaml
xpack.reporting.csv.maxSizeBytes: ...
```