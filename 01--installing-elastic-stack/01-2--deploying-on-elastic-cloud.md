## Deploying Elastic Stack on the Elastic Cloud

Create a deployment (`ax-va-deployment` in my case)

https://cloud.elastic.co/

Optionally create an API key to perform most of the operations available in the UI console through API calls

https://cloud.elastic.co/account/keys

Use the Elastic Cloud's main console

https://cloud.elastic.co/home

-> Click **Manage** -> **Cloud > Deployment > ax-va-deployment**

See, for example, `Deployment version v8.15.1`.

Optionally save the **Cloud ID**. 
It will be useful and convenient to configure Elasticsearch clients, Beats, Elastic Agent, 
and so on to send data to the Elastic deployment.

## Manage and configure the deployment

- Deployment autoscaling https://www.elastic.co/guide/en/cloud/current/ec-autoscaling.html
- Traffic Filtering https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-deployment-configuration.html
- etc