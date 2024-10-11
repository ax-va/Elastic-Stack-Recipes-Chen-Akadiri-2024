## Node roles

An Elasticsearch cluster can have a variety of node roles, besides data tiers, to function efficiently:

- Ingest
- Master
- Machine Learning
- Content / Search
- Data - Hot
- Data - Warm
- Data - Cold
- Data - Frozen
- Transform
- Coordinating

# Nodes to create

- a dedicated master eligible node
- a machine learning node

# Creating nodes

- Create a new directory for each node, e.g.

- `/bin/elasticsearch-node-master`
- `/bin/elasticsearch-node-ml`

```unix
$ cd /bin
$ sudo mkdir elasticsearch-node-master
$ sudo mkdir elasticsearch-node-ml
```

- Download and extract the content of Elasticsearch package in each directory. 
Make sure to use the same version and operating system as for the cluster.

```unix
$ sudo cp /bin/elasticsearch/elasticsearch-8.15.1-linux-x86_64.tar.gz /bin/elasticsearch-node-master
$ sudo cp /bin/elasticsearch/elasticsearch-8.15.1-linux-x86_64.tar.gz /bin/elasticsearch-node-ml
$ cd /bin/elasticsearch-node-master
$ sudo tar -xzf elasticsearch-8.15.1-linux-x86_64.tar.gz
$ cd /bin/elasticsearch-node-ml
$ sudo tar -xzf elasticsearch-8.15.1-linux-x86_64.tar.gz
```

- Change the owner to another user, because Elasticsearch cannot be run by root
```unix
$ sudo chown -R <username>:<username> /bin/elasticsearch-node-master/elasticsearch-8.15.1
$ sudo chown -R <username>:<username> /bin/elasticsearch-node-ml/elasticsearch-8.15.1
```

- Open `elasticseach.yml` for the master node and add
```yaml
node.name: node-master
node.roles: ["master"]
```
and same for the ml node
```yaml
node.name: node-ml
node.roles: ["ml"]
```

- Create `jvm.options.d/jvm.options` for each new node
```unix
$ cd elasticsearch-8.15.1/config
$ sudo -u <username> touch jvm.options.d/jvm.options
```
```
-Xms4g
-Xmx4g
```
to avoid the error `Elasticsearch died while starting up, with exit code 137` (see `01-4` for more details).

- Enroll
```unix
$ cd /bin/elasticsearch/elasticsearch-8.15.1
$ sudo ./bin/elasticsearch-create-enrollment-token -s node
```
```unix
$ cd /bin/elasticsearch-node-master/elasticsearch-8.15.1
$ sudo -u <username> ./bin/elasticsearch --enrollment-token <enrollment_token>
