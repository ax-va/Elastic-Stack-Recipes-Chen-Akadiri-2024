# Installing a self-managed Elastic Stack  

Ensure compatibility with the operating system

https://www.elastic.co/de/support/matrix

## Install Elasticsearch

- See how to download Elasticsearch

https://www.elastic.co/downloads/elasticsearch

- Download and unzip `.tar.gz` 

https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html

```unix
$ cd /bin
$ sudo mkdir elasticsearch
$ sudo mv /home/<my_name>/Downloads/elasticsearch-8.15.1-linux-x86_64.tar.gz /bin/elasticsearch
$ cd elasticsearch
$ sudo tar -xzf elasticsearch-8.15.1-linux-x86_64.tar.gz
```

- Configure `bin/elasticsearch/elasticsearch-8.15.1/config/elasticsearch.yml` to change defaults.

- In order to avoid the error `Elasticsearch died while starting up, with exit code 137`, 
create a `jvm.options.d/jvm.options` file
```unix
$ cd elasticsearch-8.15.1/config
$ sudo touch jvm.options.d/jvm.options
```
Adjust heap size to 4 GB adding the following lines to the file
```
-Xms4g
-Xmx4g
```

## Install Kibana

- Download and unzip `.tar.gz`

https://www.elastic.co/de/downloads/kibana

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
create a new user and a new group, and change the owner
```unix
$ sudo adduser elastic
$ sudo chown -R elastic:elastic /bin/elasticsearch/elasticsearch-8.15.1
$ sudo chown -R elastic:elastic /bin/kibana/kibana-8.15.1
```

## Run Elasticsearch

- Run Elasticsearch
```unix
elasticsearch-8.15.1$ sudo -u elastic ./bin/elasticsearch
```

- Securely save a generated password of the elastic user, HTTP CA certificate SHA-256 fingerprint, and  
the enrollment token for Kibana (valid for 30 minutes).

## Run Kibana

- Run Kibana

```unix
kibana-8.15.1$ sudo -u elastic ./bin/kibana
```

Browser to localhost `http://localhost:5601/...`, set the token, and log in. 
