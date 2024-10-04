## Four data tiers provided by Elasticsearch

- **Hot tier** handles mostly indexing and query for *timestamped data* (most recent and frequently accessed data);
can also be referenced as the **content tier** for *non-timestamped data*.
- **Warm tier** is used for less recent timestamped data (more than seven days) that does not need to be updated; 
extends storage capacity up to five times compared to the hot tier.
- **Cold tier** is used for timestamped data that is not so frequently accessed and not updated anymore; 
is built on searchable snapshots technology and can store twice as much data compared to the warm tier.
- **Frozen tier** is used for timestamped data that is never updated and queried rarely but needs to be kept for 
regulation, compliance, or security use cases; stores most of the data on searchable snapshots 
and only the necessary data based on query is pulled and cached on a local disk inside the node.

## How to add a new node to the cluster

https://www.elastic.co/guide/en/elasticsearch/reference/master/configuring-stack-security.html#stack-enroll-nodes

## Searchable snapshots

https://www.elastic.co/guide/en/elasticsearch/reference/current/searchable-snapshots.html

## Problems encountered

- Not enough storage set for a frozen node and how to add a failed node
https://discuss.elastic.co/t/node-frozen-fatal-exception-while-booting-elasticsearchjava-io-uncheckedioexception-java-io-ioexception-not-enough-free-space-55991361536-for-cache-file-of-size-131852140544-in-path-usr-bin-elasticsearch-node-frozen-elasticsearch-8-15-1-data/368072/8

## How to set up data tiers in a self-managed Elasticsearch cluster

- Open the `elasticearch.yml` file of the cluster (the previously installed and set up node) 
and uncomment the `transport.host` setting at the end.
```yaml
transport.host: 0.0.0.0
```

- Create two new directories for the new nodes, e.g.
- `/bin/elasticsearch-node-cold`
- `/bin/elasticsearch-node-frozen`

```unix
$ cd /bin
$ sudo mkdir elasticsearch-node-cold
$ sudo mkdir elasticsearch-node-frozen
```

- Download and extract the content of Elasticsearch package in each directory. 
Make sure to use the same version and operating system as for the cluster.

```unix
$ sudo cp /bin/elasticsearch/elasticsearch-8.15.1-linux-x86_64.tar.gz /bin/elasticsearch-node-cold
$ sudo cp /bin/elasticsearch/elasticsearch-8.15.1-linux-x86_64.tar.gz /bin/elasticsearch-node-frozen
$ cd /bin/elasticsearch-node-cold
$ sudo tar -xzf elasticsearch-8.15.1-linux-x86_64.tar.gz
$ cd /bin/elasticsearch-node-frozen
$ sudo tar -xzf elasticsearch-8.15.1-linux-x86_64.tar.gz
```

- Change the owner to another user, because Elasticsearch cannot be run by root
```unix
$ sudo chown -R elastic:elastic /bin/elasticsearch-node-cold/elasticsearch-8.15.1
$ sudo chown -R elastic:elastic /bin/elasticsearch-node-frozen/elasticsearch-8.15.1
```

- Open `elasticseach.yml` for the cold node and add
```yaml
node.name: node-cold
node.roles: ["data_cold"]
```
and same for the frozen node
```yaml
node.name: node-frozen
node.roles: ["data_frozen"]
```

- Create `jvm.options.d/jvm.options` for each new node (as for the cluster) but with less RAM
```
-Xms2g
-Xmx2g
```
to avoid the error `Elasticsearch died while starting up, with exit code 137` (see `01-4` for more details).

- If the part `BEGIN SECURITY AUTO CONFIGURATION` exists in `elasticseach.yml`, 
remove it completely to avoid skipping security auto-configuration.
(It appears after the failing node`s first run.)

- If the `elasticsearch.keystore` file exist, remove it completely to avoid aborting auto-configuration.
(It appears after the failing node`s first run.)

- Generate enrollment tokens (`-s node` specifies enrolling an Elasticsearch node into the cluster) with
```unix
$ cd /bin/elasticsearch/elasticsearch-8.15.1
$ sudo ./bin/elasticsearch-create-enrollment-token -s node
```

- Pass the enrollment token with `--enrollment-token` for the cold node
```unix
$ cd /bin/elasticsearch-node-cold/elasticsearch-8.15.1
$ sudo -u elastic ./bin/elasticsearch --enrollment-token <enrollment_token>
```
and same for the frozen node
```unix
$ cd /bin/elasticsearch-node-frozen/elasticsearch-8.15.1
$ sudo -u elastic ./bin/elasticsearch --enrollment-token <enrollment_token>
```

## How to set up data tiers on Elastic Cloud

...