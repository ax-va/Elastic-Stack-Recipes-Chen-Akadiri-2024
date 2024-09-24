## Elastic Cloud

Create a deployment (`ax-va-deployment`)

https://cloud.elastic.co/

Create an API key to perform most of the operations available in the UI console through API calls

https://cloud.elastic.co/account/keys

Elastic Cloud's main console

https://cloud.elastic.co/home

-> Click **Manage** -> **Cloud > Deployment > ax-va-deployment**

For example: Deployment version v8.15.1.

Save the **Cloud ID**. It will be useful and convenient to configure Elasticsearch clients, Beats, Elastic Agent, 
and so on to send data to the Elastic deployment.

## Manage and configure the deployment

- Deployment autoscaling https://www.elastic.co/guide/en/cloud/current/ec-autoscaling.html
- Traffic Filtering https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-deployment-configuration.html
- etc