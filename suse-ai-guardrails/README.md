
# GreenDoc - SUSEAI Demo Lab

*Author:* Alessandro Festa

*Rev. Number:* v1.0

SUSE AI Demo enviroment is a simple document that is intended to describe how to implement a local lab to demonstrate capabilites of SUSE AI 
If you are interested in understanding more what is SUSE AI please refer to [http://suse.com/products/ai](http://suse.com/products/ai)

The applications in this repo are pulled from the SUSE Application Collection [https://apps.rancher.io/](https://apps.rancher.io/) check the documentation at [https://docs.apps.rancher.io/](https://docs.apps.rancher.io/) to learn more about AppCo

This GreenDoc is structured in the following way:

* Cluster setup
* Rancher Fleet setup (for automation of the GreenDoc)
* GreenDoc Configuration
* GreenDoc deployment
* Simple final Demo


## Cluster Setup

For the purpose of this GreenDoc we'll use [K3s](https://k3s.io).

### Create namespaces used in the environment

```SHELL
kubectl create namespace cert-manager
```
```SHELL
kubectl create namespace suseai
```

### Create secrets for namespaces

```SHELL
kubectl create secret docker-registry application-collection \
--docker-server=dp.apps.rancher.io \
--docker-username=<your registered account on appco> \
--docker-password=<INSERT YOUR TOKEN FROM APPCO> \
-n cert-manager
```

```SHELL
kubectl create secret docker-registry application-collection \
--docker-server=dp.apps.rancher.io \
--docker-username=<your registered account on appco>\
--docker-password=<INSERT YOUR TOKEN FROM APPCO> \
-n suseai
```

## Use Rancher Application Collection for components

### Deploy cert-manager helm chart

```SHELL
helm upgrade --install cert-manager \
  oci://dp.apps.rancher.io/charts/cert-manager \
  --version 1.17.2 \
  -n cert-manager \
  --create-namespace \
  --set crds.enabled=true \
  --set "global.imagePullSecrets[0].name"="application-collection"
```

### Deploy Rancher

We have to install Rancher enabling the OCI extensions
```SHELL
helm install rancher rancher-stable/rancher \
--namespace cattle-system \
--set hostname=192.168.5.15 \
--set bootstrapPassword=admin \
--set-string extraEnv[0].name=EXPERIMENTAL_OCI_STORAGE \
--set-string extraEnv[0].value=true \
```
Let's wait for Rancher to be installed. Follow the instruction from [here](https://ranchermanager.docs.rancher.com/getting-started/quick-start-guides/deploy-rancher-manager/helm-cli#install-rancher-with-helm).
Login into Rancher UI and check if everything is up and running.

Now let's move to the final steps, first let's add a generic secret for basic authentication

```SHELL
kubectl create secret generic basic-auth-secret \--from-literal=username=<your registered account on appco> \
--from-literal=password=<INSERT YOUR TOKEN FROM APPCO> \
-n fleet-local
```
Once done we may move to Rancher Continous Delivery in the Rancher UI and add our repo.

* Give a generic name, in this example we use the root folder name (i.e.: suse-ai-guardrails).
* Add the github repo `https://github.com/alessandro-festa/demos`
* Choose the fleet-local deployment (on the top right of the page) and add as namespace `suseai``
* Finally in the last step edit using the YAML file and replace the value in `HELMSecret`adding `basic-auht-secret`(the secret we created above)

Hit finish and that's it You should have minimal SUSE AI stack deployed

Let's check that! Simply open a browser and point to [http://localhost:31000](http://localhost:31000)

