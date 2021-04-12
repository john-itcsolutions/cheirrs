## SMART-WEB - a Docker charm for the elastos-smartweb-service:

## This charm is being designed and built to enable the elastos-smartweb-service to serve a connection to Elastos Blockchains, and to ITCSA's database ("house"). The entire repository may be considered as part of the cheirrs project at:

https://github.com/john-itcsolutions/cheirrs


## The way forward:

We know that we must build a "smart-web" charm, rather than simply using kubectl to deploy the software, as was done in our smart-web-postgresql-grpc repo. Otherwise we would have no simple mechanisms for smart-web to find, connect and synchronise with its environment.

For juju charms, their 'relations' and 'hooks' enable synchronous operation with the other charms in their environment. The relations and hooks operate by boolean logic and are programmed 'reactively', meaning the hooks react to changes in the environment to signal to other hooks. A change might be a machine going offline, or one coming online, or a machine moving from "available" to "ready", or some other change-in-state of the model containing the charms.

We may have to add another model on the 'house' controller to take care of all our 'Docker' requirements (which are rumoured incompatible with non-docker models - yet to be confirmed) on juju.


In this case we would begin by:

`juju switch house`

`juju add-model docks`

`juju deploy cs:~cynerva/easyrsa-8`

`juju deploy cs:~yellow/cert-manager-3`

`juju add-relation easyrsa cert-manager`

`juju deploy cs:etcd-553`

`juju add-relation easyrsa etcd`

However at this stage we are trying to go ahead and set up the docker based infrastructure on the dbase-bchains model itself (where the smart-web-service will be connecting anyway, even if ultimately via cross-model referencing.)

So we `juju switch dbase-bchains` or `juju switch house`, if you were on Kubeflow.

There is no 'docker' charm as yet. This will be started from the process of running the docker subordinate charm itself. 

Now, we need to begin to assemble the smart-web charm, layer by layer, before we can build it. There are fundamentally 3 stages in assembling the layers: first is the base layer with any of the provided base charms for this layer. We choose, not code, this layer. There is a minor amount of 'boilerplate' with some charms, layers and interfaces. This is found on the juju repo sites on github.

Please refer to  https://github.com/juju/layer-index. We choose the docker base layer; the method is simply:

`juju deploy cs:~containers/docker-91`

The second stage consists of "interfaces" and "charm-layers", which we likewise choose, to satisfy our requirements, such that the coding revolves around the relations and hooks to be brought to life in response to planned changes in the model environment as a charm is started and begins relating to its providers and requirers. The third stage is the building and packaging of the actual charm (a docker-based charm, in our case) But before this we require the charm tools:

`sudo snap install charm --classic`

From your outer working directory:

`charm create smart-web`

Refer to - https://discourse.charmhub.io/t/deploy-your-docker-container-to-any-cloud-with-charms/1135

and: https://discourse.charmhub.io/t/layers-for-charm-authoring/1122

and: https://discourse.charmhub.io/t/interface-layers/1121

and for the base layer: https://charmsreactive.readthedocs.io/en/latest/layer-basic.html

`cd smart-web`

`mkdir interfaces`

`mkdir layers && cd layers`

Starting from the first (base) layer we need:

`git clone https://github.com/juju-solutions/layer-docker-resource.git`

`git clone https://github.com/juju-solutions/layer-tls.git`

`git clone https://github.com/juju-solutions/layer-tls-client.git`

`cd ../interfaces`

`git clone https://github.com/juju-solutions/interface-dockerhost.git`

`git clone https://github.com/juju-solutions/interface-docker-image-host.git`

`git clone https://github.com/juju-solutions/interface-docker-registry.git`

`git clone https://github.com/juju-solutions/interface-etcd.git`

`git clone https://github.com/juju-solutions/interface-pgsql.git`

`git clone https://github.com/juju-solutions/interface-redis.git`

`git clone https://github.com/juju-solutions/interface-tls.git`

`git clone https://github.com/juju-solutions/interface-http.git`

`git clone https://github.com/juju-solutions/interface-tls-certificates.git`

Refer to https://discourse.charmhub.io/t/charm-tools/1180 for details of "charm tools" commands. Note also that each interface or layer is documented on its own repo site.

We have begun to assemble the code in metadata.yaml, layer.yaml, and smart_web.py (the so-called reactive code in Python). Aside from cloning this repo (`git clone https://github.com/john-itcsolutions/smart-web.git`), one also needs to git clone the repo's above (12 in all) in the list of layers above. These must be cloned into the "layers" and "interfaces" directories under "smart-web/".

# TO BE CONTINUED .. we're learning to use Docker to build charms now ..

(Refer to https://discourse.charmhub.io/t/deploy-your-docker-container-to-any-cloud-with-charms/1135)



## In the case that the charm will run equally on the original dbase-bchains model (which we are attempting), we could dispense with the entire "docks" model, and simply deploy our built smart-web docker charm onto the dbase-bchains model.


_____________________________________________________________
