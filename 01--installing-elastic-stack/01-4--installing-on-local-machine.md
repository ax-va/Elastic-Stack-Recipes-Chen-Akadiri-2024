# Installing a self-managed Elastic Stack

- Ensure compatibility with your operating system

https://www.elastic.co/de/support/matrix

- Download Elasticsearch

https://www.elastic.co/downloads/elasticsearch

- Download Kibana

https://www.elastic.co/de/downloads/kibana

# Installing on Ubuntu (22.04. LTS)

## Install Elasticsearch

- How to install on Posix

https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html

- Download and unzip `.tar.gz`

https://www.elastic.co/de/en/en/downloads/elasticsearch

```unix
$ cd /bin
$ sudo mkdir elasticsearch
$ sudo mv /home/<my_name>/Downloads/elasticsearch-8.15.1-linux-x86_64.tar.gz /bin/elasticsearch
$ cd elasticsearch
$ sudo tar -xzf elasticsearch-8.15.1-linux-x86_64.tar.gz
```

## Install Kibana

- Download and unzip `.tar.gz`

```unix
$ cd /bin
$ sudo mkdir kibana
$ sudo mv /home/delorian/Downloads/kibana-8.15.1-linux-x86_64.tar.gz /bin/kibana
$ cd kibana
$ sudo tar -xzf kibana-8.15.1-linux-x86_64.tar.gz
```

## Prepare a non-root user

- In order to avoid the error 
`fatal exception while booting Elasticsearchjava.lang.RuntimeException: can not run elasticsearch as root`,
create a new user and a new group if necessary, and change the owner for all subdirectories
```unix
$ sudo adduser <username>
$ sudo chown -R <username>:<username> /bin/elasticsearch/elasticsearch-8.15.1
$ sudo chown -R <username>:<username> /bin/kibana/kibana-8.15.1
```

## Prepare settings

- Configure `bin/elasticsearch/elasticsearch-8.15.1/config/elasticsearch.yml` to change defaults if necessary.

- In order to avoid the error `Elasticsearch died while starting up, with exit code 137`, 
create a `jvm.options.d/jvm.options` file
```unix
$ cd elasticsearch-8.15.1/config
$ sudo -u <username> touch jvm.options.d/jvm.options
```
Adjust heap size to 4 GB adding the following lines to the file
```
-Xms4g
-Xmx4g
```

## Run Elasticsearch (as a single-node cluster)

- Run Elasticsearch
```unix
elasticsearch-8.15.1$ sudo -u <username> ./bin/elasticsearch
```

- Securely save a generated password of the elastic user, HTTP CA certificate SHA-256 fingerprint, 
and the enrollment token for Kibana (valid for 30 minutes).

## Run Kibana

- Run Kibana

```unix
kibana-8.15.1$ sudo -u <username> ./bin/kibana
```

Browser to localhost `http://localhost:5601/...`, set the enrollment token, and log in.

## How to use a self-managed deployment with Docker

https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html
