## INTRODUCTION:

# CHEIRRS
Project based on  Lxd, Juju, Charms and Kubernetes; merged with Cyber Republic's Elastos Smartweb gRPC-based Blockchain and Database Server. Database ORM, reflection (at initialisation) and querying uses SQLAlchemy. The blockchain end of a transaction occurs first, followed by writing or reading of data to or from Postgres, via the "redis" cluster on the Kubernetes installation. 

gRPC protocols replace the older style REST APIs, for communicating requests, and data inputs, from the client, and responses from the blockchain &/or database back to the client; all this occurs through the smart-web server, employing a "microservices" architecture. Here the gRPC protocols are implemented in Python. The smart-web server has Carrier installed onboard, guaranteeing security. 

To tackle a full Kubernetes installation locally, ideally you would need a 32 GB RAM (minimum); 250 GB SSD; + HDD: PC (x86_64). eg an Extreme Gaming Computer. If you intend to include Machine Learning/AI capabilities, your Kubeflow installation will go much more easily with an 8 core Host processor rather than a 4 core one. You really need an Accelerator NVIDIA GPU of at least 10GB vRAM. ITCSA is using a 24GB NVIDIA Tesla K80.

The following figure represents the 'betrieb' controller with its 'werk' model, as opposed to 'lernenmaschine', the other model, on 'lernenmaschine' controller (based on microk8s). We install the Kubeflow (lernenmaschine) model first.

We base initial development such as this locally. It's cheaper!

<img src="./kubernetesinstallation-25-06-2021-1.png">

The schema above are labeled G(n,m) for the internetworked, multiple member class dApps. In reality there are only n schema with the member classes (m) being a data field in every table within the nth schema. In this way we can keep all transactions internal to a network on the same schema. The nth network is on the nth schema. The single member class, non-internetworked dApps (F(i)) are likewise constituted of all members of a network or dApp subscribers' group, on their own schema. Although this is the case with the set F(i), within a single network ie schema ie dApp, we will be able to use the field for a member's id ("j" in the diagram) to distinguish between members' different dApp requirements and proliferate different (custom) tables and processes within a single network/dApp/schema. The same is ideally the case for the G(n,m) set, such individual member Tables and dApps are theoretically possible, though expensive.

We utilise one "oseer" schema per network, so there is one schema for each of the G(n) networks/schema, and one for each of the F(i) future dApps, as well as one for each of the A, B and C dApps (Community Housing, RealEstate and convey-IT, respectively). Our schema called a_horse is the Head Overseeing Schema, for top level customer on-boarding, usage tracking and payments, as well as to "oversee the overseers".

You need to develop initially on docker. ITCSA uses Ubuntu 20.04 as the host platform.
You will not need an Extreme Gaming level of computer for Docker-based (initial - eg. database) work without Kubernetes.

See our website at https://www.itcsolutions.com.au/kubernetes-yaml-file-example/ for an older but more visual idea of this project and others.

The Front End dApp corresponding to this project is at https://github.com/john-itcsolutions/au.com.itcsolutions.cheirrs.0.01. It uses the Ionic Platform for web app (in our cases, "distributed app") development. However the Ionic system must be used in conjunction with the newly developing 'Elastos Essentials' package. This package will include all necessary interfaces for the Elastos Ecosystem from the points of view of both developers and users. You can follow this development process (expected to introduce the first stable distribution around July, 2021) at:

https://github.com/elastos/Elastos.Essentials

You would also require some dev tools and the openjdk for Java, as well as nodejs@12.x:

```
# Base requirements 
sudo apt -y install openjdk-8-jdk build-essential curl dirmngr apt-transport-https lsb-release ca-certificates
# Install NodeJS 12 instead of 8 or 10
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt -y install nodejs
```

As well as installing Ionic:

`sudo npm i -g @ionic/cli`

The Ionic docs are at:

https://ionicframework.com/docs

In an Ionic dApp (either React or Angular-based) you will find `manifest.json`.

This file is where you can whitelist websites (including the cloud database/blockchains and server site, even if local).

All websites are blacklisted by default, until you whitelist the sites required by your dApp.

This enables the Elastos Carrier system to do its magic and connect in a private and ultra-secure way to websites, with no websockets used.

(see the Elastos Whitepaper at https://www.elastos.org/downloads/elastos_whitepaper_en.pdf)

Currently (May 2021) the Elastos Developer Documentation does not address development with the new Elastos Essentials.

## ________________________________________________________________________________________________________________________

## Get:

Docker for Ubuntu: https://docs.docker.com/engine/install/ubuntu/  - SAFEST WAY!

Remember to

`sudo usermod -aG docker $USER && newgrp docker`

after install is complete.

The docker-based development on this project is adapted from the code in:

https://github.com/cyber-republic/elastos-smartweb-service  (smartweb-server, providing blockchain access, containerised by ITCSA)

and

https://github.com/cyber-republic/python-grpc-adenine  (smartweb-client, database query client with Python)

and

lxd, juju, kubernetes and Kubeflow. Also:

https://jaas.ai/u/stub/postgresql (PostgreSQL without PostGIS initially)

We rely on the "redis" cluster of the kubernetes charmed ecosystem to provide the in-memory, "key-value" query cache servers for the database transactions,

TensorFlow by Google. 

The predominant language used to code for this project is Python (here, mainly version 3.8).

______________________________________________________________

## Preliminaries: NOTE The following remarks on installing the Nvidia and Cuda systems constitute a work in progress only:

With the exception of noting that this:

`nvidia-smi`

should produce a positive message, if you want to use your nvidia gpu with CUDA capacities as part of the system; we cannot advise further.

________________________________________________________________


## We continue by installing Kubeflow to obtain a controller compatible with this Juju/TensorFlow environment:
________________________________________________________________


In case lxd is not already installed, this is how, however it is most likely to be present initially:

`sudo snap install lxd`

`sudo lxd init`

storage type must be "dir" and ipv6 should be "none", otherwise all default answers are fine.


## 'KUBEFLOW', TensorFlow and Machine Learning (Artificial Intelligence & Statistical Learning)

Unfortunately the charmed system is mainly oriented for Public Clouds when it comes to the Kubeflow charm bundle. However in combination with microk8s, much can still be achieved ..

From the outermost directory in your working system (on a second HDD if available), check out these repositories locally:

`git clone https://github.com/john-itcsolutions/cheirrs.git`

`git clone https://github.com/juju-solutions/bundle-kubeflow.git`

`cd bundle-kubeflow`

The below commands will assume you are running them from the bundle-kubeflow directory.

Then, follow the instructions from the subsection below to deploy Kubeflow to microk8s.

Microk8s is the only way to easily obtain a working Kubeflow/tensorflow installation on your localhost without paying cloud fees ..

Setup microk8s on the Ubuntu Host:

`sudo snap install microk8s --classic`

Next, you will need to add yourself to the microk8s group:

`sudo usermod -aG microk8s $USER && newgrp microk8s`

`sudo su - $USER`   (quick reset of terminal)

On the Host, you'll need to install these snaps to get started:

`sudo snap install juju --classic`

`sudo snap install juju-wait --classic`

`sudo snap install juju-helpers --classic`

If you

`juju clouds`

you will aleady find that there exists a 'microk8s/localhost' cloud. Later we will set up another 'localhost/localhost' cloud with different properties, for the main blockchains, database schema and database servers in a kubernetes installation.

Finally, you can run these commands to set up kubeflow/TensorFlow, but you have to have the cloned "bundle-kubeflow", from the above section, available:

Note: After this installation of the 'lernenmaschine' model on the 'microk8s' controller in a 'kubeflow-lite' package (we edited the cli script and names), we will be installing a 'betrieb' controller with 'werk' model. 

Initially:

`sudo apt install python3-pip`

`pip3 install click`

`cd /path/to/bundle-kubeflow`

If you need to choose 'kubeflow lite' (recommended for initial development), you can edit the relevant code in scripts/cli.py and note that you may also alter the controller name, if you take care to alter the commands you issue.

`python3 scripts/cli.py microk8s setup --controller lernenmaschine`

The upcoming deploy-to command allows manually setting a public address that is used for accessing Kubeflow on MicroK8s. However in some deployment scenarios (such as local development), you would need to configure MicroK8s to use LAN DNS instead of the default of 8.8.8.8. To do this, edit the coredns configmap with this command:

`microk8s.kubectl edit configmap -n kube-system coredns`

Edit the line with 8.8.8.8 8.8.4.4 to use your local DNS, e.g. 192.168.1.1. You will need to use the arrow keys and the 'insert' and 'delete' keys carefully! Save and exit as for vim.

If you make mistakes during editing, it is safest to:

`juju destroy-controller microk8s --destroy-all-models --destroy-storage `

and restart from 

`python3 scripts/cli.py microk8s setup --controller lernenmaschine`

followed by editing the coredns configmap again.

     _____________________________________________

Only when the coredns configmap is correct for your LAN:

`python3 scripts/cli.py deploy-to lernenmaschine`

(Passthrough should already be natively enabled to your Accelerator GPU.)

Check the status of the installation with:

`watch -c juju status --color`

or:

`juju status`

for a static summary.

On Host, you could switch between other possible controllers by noting the current controllers known to juju:

`juju controllers`

and then selecting the target for switching, and:

`juju switch <target-controller-name>`

Within controllers you may substitute <target-model-name> and use:

`juju switch <target-model-name>`

to move between models on the same controller.

The following image is a screenshot of the `lernenmaschine` model's status board after successful installation of "kubeflow-lite":

<img src="./Screenshot from 2021-06-16 18-14-22.png">
     
Note that we have actually found it impossible to sustain a kubeflow controller on the microk8s cloud at the same time as we are running the second controller on the localhost cloud referred to in the text below the kubeflow Manual (following). The host randomly reboots. The latter cloud works alone, and, as it represents the more business-end of our business, we continue with no kubeflow. A singleton setup may work better with Kubeflow installed alone on a microk8s/localhost host. There is sufficient RAM onboard our host according to the system monitor, so at this stage the cause is unknown.
______________________________________________________________

## USING KUBEFLOW

### Main Dashboard

Most interactions will go through the central dashboard, which is available via
Ambassador at `/`. The deploy scripts will print out the address you can point your browser to when they are done deploying.

### Pipelines

Pipelines are available either by the main dashboard, or from within notebooks
via the [fairing](https://github.com/kubeflow/fairing) library.

Note that until https://github.com/kubeflow/pipelines/issues/1654 is resolved,
you will have to attach volumes to any locations that output artifacts are
written to, see the `attach_output_volume` function in
`pipline-samples/sequential.py` for an example.

### Argo UI

You can view pipelines from the Pipeline Dashboard available on the central
dashboard, or by going to `/argo/`.

### TensorFlow Jobs

To submit a TensorFlow job to the dashboard, you can run this `kubectl`
command:

    kubectl create -n <NAMESPACE> -f path/to/job/definition.yaml

Where `<NAMESPACE>` matches the name of the Juju model that you're using,
and `path/to/job/definition.yaml` should point to a `TFJob` definition
similar to the `mnist.yaml` example [found here][mnist-example].

[mnist-example]: charms/tf-job-operator/files/mnist.yaml

### TensorFlow Serving

See https://github.com/juju-solutions/charm-tf-serving


## Removing

### Kubeflow model

To remove Kubeflow from your Kubernetes cluster, first run this command to
remove Kubeflow itself:

    juju destroy-model lernenmaschine --destroy-storage

If you encounter errors while destroying the model, you can run this command
to force deletion:

    juju destroy-model lernenmaschine --yes --destroy-storage --force

Alternatively, to simply release storage instead of deleting it, run with this
flag:

    juju destroy-model lernenmaschine --release-storage

### Kubeflow controller

You can destroy the controller itself with this command:

    # For microk8s
    juju destroy-controller $(juju show-controller | head -n1 | sed 's/://g') --destroy-storage

## Tests

To run the test suite included in this repository (bundle-kubeflow), start by installing the Python dependencies:

    pip install --user -r requirements.txt -r test-requirements.txt

Next, ensure that you either have the `juju-helpers` snap package installed, or you have
the `kubectl` binary available with `~/.kube/config` set up correctly.

Then, run the tests with this command:

    pytest tests/ -m <bundle>

where `<bundle>` is whichever bundle you have deployed, one of `full`, `lite`, or `edge`.

If you have Charmed Kubeflow deployed to a remote machine with an SSH proxy available
(for example, if you have MicroK8s running on an AWS VM), you can run the tests like this to run them against the remote machine:

    pytest tests/ -m <bundle> --proxy=localhost:9999 --url=http://10.64.140.43.xip.io/ --password=password

Additionally, if you'd like to view the Selenium tests as they're in progress, you can
pass in the `--headful` option like this:

    pytest tests/ -m <bundle> --headful
______________________________________________________________

# There is a possibility of setting up a Postgres database with PostGIS and Open Street Maps. It appears that the procedure Canonical have taken with Kubeflow above utilises MongoDB during installation, a no-SQL, non-relational database system, as one of the persistence stores as well as Mariadb (a resurrection of the opensource version of mysql) within the "kubeflow" model (which we are calling `lernenmaschine` ..)

As noted below, it is possible, using cross-model referencing, and "offers", to enable an application on a separate controller and/or model, eg the kubeflow model in the uk8s controller, (or just a separate model on the same controller) to access the PostgreSQL/PostGIS database ('haus') on the 'betrieb' controller and the 'werk' model (see following) therein.

See below at the "## Set up Cross-Model Referenced "offer" .. " heading.

But which `<application-name>` (in kubeflow model) to use as requiring connection to the provided db?

To be continued.

_________________________________________________________________

## A Second Model on a second controller:

(The database schema for ITCSA's project are private and available only under certain conditions.)

In a host terminal, from a second HDD if available, to save working files in case of a crash:

Bootstrap a new controller - but this time on the 'localhost' cloud - (when you installed juju, it recognised that localhost was already installed, and juju created a 'localhost' cloud for you to use. Verify this with `juju clouds`):

(You should change ownership of files on your system to your own username. Do this with 

`sudo chown -R <your-username-on-linux> ~ && sudo chown -R <your-username-on-linux> /tmp`

). Then:

`juju bootstrap localhost betrieb`

Add a model named "werk"

`juju add-model werk`

Deploy the 'Calico' Kubernetes Charm, since default CNI provider 'Flannel' does not provide all necessary services:

`juju deploy cs:~containers/bundle/kubernetes-calico-1070`

`juju config kubernetes-master proxy-extra-args="proxy-mode=userspace"`

`juju config kubernetes-worker proxy-extra-args="proxy-mode=userspace"`

At this stage your juju assemblage is converging towards stability. You can observe the status of the assemblage with

`watch -c juju status --color` or, `juju status` for short.

It may take a few hours if your network is slow. Be patient.

When you see everything 'green', you may continue.

Deploy PostgreSQL (Juju sorts out Master and Replicating servers automatically).

`juju deploy postgresql pg-a`

`juju add-unit pg-a`
     
`juju config pg-a admin_addresses=127.0.0.1,0.0.0.0,<ip-addr-worker-0>,<ip-addr-worker-1>`

Deploy a Redis cluster for in-memory caching:

`juju deploy cs:~omnivector/bundle/redis-cluster-1`
     
`juju expose redis`


*******************************************************

________________________________________________________________
 
## DATABASE: Internals

## Copy sql scripts; Build Database Schema:

From Host, in .... /cheirrs/elastos-smartweb-service/grpc_adenine/database/scripts folder:

`juju scp *.sql <machine number of postgresql master>:/home/ubuntu/`

## The following command would be possible only after you are positively identified, gain our trust, and sign an agreement to work with us, in order to obtain these backup files. Or, develop your own!

`cd ../../../../ && juju scp dbase_setup.sh *.sql <machine number of postgresql master>:/home/ubuntu/ && cd ../ && juju scp *.sql <machine number of postgresql master>:/home/ubuntu/`

where some of the relevant .sql backup files are outside the 'cheirrs' repository, and generally unavailable publically.

exec into master db container:

`juju ssh <machine number of postgresql master>`

Now you are inside postgres master container, in the /home/ubuntu directory:

`sudo passwd postgres`

Enter your new postgres user's password twice.

`su postgres`

`./dbase_setup.sh`

(.. wait a minute or 2. Don't worry about the syntax errors visible when the scripts have run)

`\dt ` should reveal no instances (in default public schema)

`set search_path to cheirrs;`

.. now, `\dt` should reveal a full set of 600+ tables in 2 categories: 1) accounting_<xyz> and 2) uc_<uvw> ('uc_' for use_case)

Identical results will appear for:

`set search_path to cheirrs_oseer;`

and, for example;

`set search_path to a_horse;`

when you run 

`\dt`

In postgres master machine:

Exit psql shell:

`\q`


__________________________________________________________________

## Getting PostGIS and Open Street Maps

Inside your postgresql Master (

`juju ssh <postgresql_Master_machine_number>`, or if you are already acting as user 'postgres' on postgresql-master, simply `exit` 

)

As user ubuntu (if acting as "postgres" `exit`as "postgres" is not a sudoer) & get ubuntugis repo:

`sudo add-apt-repository ppa:ubuntugis/ppa`

`sudo apt update`

`sudo apt-get install postgis`

`sudo apt update`

`sudo apt-get install osm2pgrouting`

`su postgres`

`psql haus`

Now you are interfaced to the haus database.

-- Enable PostGIS

`CREATE EXTENSION postgis;`

-- enable raster support (only for 3+ - may lead to an error on postgres < v12 - ignorable)

`CREATE EXTENSION postgis_raster;`

-- Enable Topology

`CREATE EXTENSION postgis_topology;`

-- Enable PostGIS Advanced 3D
-- and other geoprocessing algorithms
-- sfcgal not available with all distributions

`CREATE EXTENSION postgis_sfcgal;`

-- fuzzy matching needed for Tiger

`CREATE EXTENSION fuzzystrmatch;`

-- rule based standardizer

`CREATE EXTENSION address_standardizer;`

-- example rule data set

`CREATE EXTENSION address_standardizer_data_us;`

-- Enable US Tiger Geocoder

`CREATE EXTENSION postgis_tiger_geocoder;`

Finally, we can create all initial users and usage permissions

`\i /home/ubuntu/create_users.sql`

(Note for the smart-web blockchains to work, gmu must exist as a user with password gmu, and with usage permission to all schema.)

Check Schemas: there should be 'a_horse'; 'cheirrs'; 'cheirrs_oseer', 'chubba_morris', 'chubba_morris_oseer', 'convey_it', 'convey_it_oseer', 'the_general', 'the_general_oseer', 'tiger', 'tiger_data', 'topology', and 'public'.

`\dn`

Check off users:

`\du`
                                                                              
` \q`
                                                                              
Now, at /home/ubuntu:

Run Elastos scripts to prepare database public schema for Blockchains interaction;

`psql -h localhost -d haus -U gmu -a -q -f create_table_scripts.sql`

`psql -h localhost -d haus -U gmu -a -q -f insert_rows_scripts.sql`

Now if you

`psql haus`

then

`\dt` (to reveal tables in default public schema) you should see 3 tables.

Try:

`select * from users;`

You should see the single user's details.
                                                                              
`\q`

`exit`

`exit`

You're back on Host.

_________________________________________________________________

## Set up Cross-Model Referenced "offer" for apps on other models to access PostgreSQL solo installation on this controller called 'betrieb', within this cmr-model called 'werk'.

[cmr-model == "Container Managed Reference"-model]

(If not on "betrieb" controller)

`juju switch betrieb`

`juju offer pg-a:db`

then, if you `juju status` in the werk model you will see, at the foot of the output, a reference to the Offer.

An application (and users - here admin and ubuntu) set to `consume` the postgres service from a different model and controller (eg here: from the 'microk8s' controller, ie from the 'lernenmaschine' model), is connected with (this needs to be run while in lernenmaschine model):

`juju grant admin consume microk8s:admin/werk.pg-a`

`juju grant ubuntu consume microk8s:ubuntu/werk.pg-a`

.. then the authorised user (in the lernenmaschine model - see above) may use:

`juju add-relation <application>:db microk8s:admin/werk.pg-a:db`

`juju add-relation <application>:db microk8s:ubuntu/werk.pg-a:db`

to connect "application" to the database (in werk model)from 'microk8s' controller, ie from the lernenmaschine model (in this case).

_______________________________________________________________

ALSO:

## Blockchains-Database Server (werk model) 

We turn to finish setting up the Blockchain/Database gRPC Server Deployment,

NOTE: As we don't own or control the elastos sub-modules, and since the `cheirrs/elastos-smartweb-service/grpc_adenine/database/__init__.py` file is not fully usable as it is, in the elastos-smartweb-service module, we have included ITCSA's version of `__init__.py` in the cheirrs root directory. This version caters for initialising the SQLAlchemy interface from the existing database, and generating a full set of Database Models, using SQLAlchemy's ORM & methods of Database Metadata Reflection. However you need to re-insert the root-directory-version at your `cheirrs/elastos-smartweb-service/grpc_adenine/database/__init__.py` (in local copies) to enable it to work properly as a Python init file. This init file will be run by the system before running the server at /grpc_adenine/server.py. You would have to keep these 2 versions of `__init__.py` in sync with each other if you need to edit `__init__.py`, and want to use your own github account. Please note you will actually have to delete the initial elastos repo directories after cloning cheirrs, followed by cloning the complete repo's back into cheirrs/ from https://github.com/cyber-republic/elstos-smartweb-service and https://github.com/cyber-republic/python-grpc-adenine.
   
     After this, on host:

`cd path/to/cheirrs/elastos-smartweb-service`

The .env.example file here needs to be filled-in with the correct database name, database server address and port as well as the correct addresses for the smart-web virtual machine. ie the blockchain addresses and ports to access the smart-web environment. It then will need to be copied to the worker machine as ".env" (but if you follow the instructions below, you might like to copy .env.example as edited to cheirrs/elastos-smartweb-service/TO*/*database/.env and while you're at it copy the same file to the same directory as ".env.test". However the final copy into the kubernetes-worker-0 cannot be done until we have cloned the elastos-smartweb-service repo into the worker (see below). Smart-web will be running on its own worker machine, as will pgadmin4. There is no need for a separate Carrier Node as smart-web contains a Carrier implementation.

The blockchain server ip-addresses in the .env.example, .env, and .env.test files need to match the address of the kubernetes-worker-0 machine, here. Also the database details will require alteration.
     
Presuming you have obtained a fresh clone of "elastos-smartweb-service", you will need to ensure the __init__.py within grpc_adenine/database directory is updated to our repo's version (as discussed above).
     
You also need to treat the "run.sh" and "test.sh" (which are in cheirrs root directory also) identically. So we will copy them soon to elastos-smartweb-service over the existing "run.sh" and "test.sh". Postgres connections in Kubernetes are not possible in the fashion assumed by "run.sh" and "test.sh" in elastos by default.

Enter worker-0:
     
`juju ssh <machine-number-worker-0>`
     
`git clone https://github.com/cyber-republic/elastos-smartweb-service.git`

Note that in the host's (in cheirrs root) "TO_BE_COPIED_TO_smartweb-service" directory are scripts and modules in .sh, and .py that have had to be altered from those provided in the experimental Elastos-smartweb-service repo. These should be copied over the existing files in the worker-0 machine. Therefore:

`exit`

`cd ....path/to/cheirrs`

`juju scp TO*service/TO*service/*.sh <machine-number-worker-0>:/home/ubuntu/elastos-smartweb-service`

`juju scp TO*service/TO*adenine/*.py <machine-number-worker-0>:/home/ubuntu/elastos-smartweb-service/grpc_adenine`

`juju scp TO*service/TO*database/*.py <machine-number-worker-0>:/home/ubuntu/elastos-smartweb-service/grpc_adenine/database`

`juju scp TO*service/TO*python/*.py <machine-number-worker-0>:/home/ubuntu/elastos-smartweb-service/grpc_adenine/stubs/python`

Re-enter worker-0:

`juju ssh <machine-number-worker-0>`

`cd el*`

`./run.sh`
 

.. and wait and watch .. and examine logs in case of errors, which are in the machines (`juju ssh <machine-number>`) at /var/log/juju/filename.log. If all is well, you should be looking at the blockchains' log, on stdout, as the cycles roll every 30 seconds. The logs of units housed by other machines are available on those machines.


              ____________________________

(Note; you are user 'ubuntu' here, so if you need a new password, just

`sudo passwd ubuntu`

Later, within the master postgresql database container, you will need to give postgres user a password:

`sudo passwd postgres`

does this.

To add, for example, 2 load-balancer units, simply

`juju add-unit -n 2 kubeapi-load-balancer`

)
_________________________________________________________________________________________________
     
     The following is a screenshot of the status board after successful installation:
     
<img src="./Screenshot from 2021-06-22 06-28-06.png">
     
     stdout of Blockchains looks like:
     
<img src="./Screenshot from 2021-06-24 22-56-05.png">
     

_____________________________________________________________


## TESTING the smartweb-service/Blockchains/Postgresql System

     Enter kubernetes-worker-0 and:
     
     `cd el*`
     
     `./test.sh`
     
     We are having difficulties with the jwt token and key system for entry authentication to the smart-web server ..
     
To be continued ..
_____________________________________________________________

## Enter kubernetes-worker-1, to set-up pgadmin4.

## Get: PGADMIN4:  Got to https://www.pgadmin.org/download/pgadmin-4-apt/ and follow instructions for web-server mode.

Allow installation of Apache server.

Then visit your own kubernetes-worker-1 address in http mode in a browser such as (example only):

http://10.57.133.75/pgadmin4

You should now have administrative access to your database. You will need to connect as user 'gmu' with password 'gmu'.

This is the real business end of the operation and where most of the data processing needs to occur. ITCSA has, for example, 627 tables in our 'cheirrs' schema, currently. 

Use triggers and trigger functions liberally. Also consider only allowing http POST queries, proscribing deletions, and dividing your schemata into 2 sections: Use_case_forms_based_tables and Accounting_based_tables, with trigger functions to process and post data from the Use_case_forms to the accounting_based_tables. This is more inuitive than some of the more complex "middleware" approaches, assuming someone understands the data-processing that is necessary and also understands the structure of the accounting_based_tables.
________________________________________________________________
     
     ## Enter kubernetes-worker-2, to set-up an iot server with node-red.
     
     `juju ssh 9`

## Get: node-red (see above if you do not yet have nodejs and npm installed):
     
`sudo npm install -g --unsafe-perm node-red`

You also will need to mimic an "edge" client or source for iot messages and signals, on your host. So:
     
`exit`
     
`sudo npm install -g --unsafe-perm node-red`
     
`node-red`
     
     and go to your own host's LAN address on browser with port `1880`
     
     Now re-enter worker-2:
     
`juju ssh 9`
     
`node-red`
     
     and go to the ip address of the worker-2 vm with port `1880`, in your host browser. 
     
     These 2 pages can interact and generate and forward messages and events.
     
     Eventually the idea is to be able to "log" and respond (in appropriate timeframes corresponding to the message origin and content)
     to events considered as "exceptional" in some way. The events and messages will be logged on blockchains and database via "smart-web" server.
     
     In order for the worker-2 server to talk to the "smart-web" server (on worker-0) we need to clone the smartweb client from elastos in worker-2:
     
`git clone https://github.com/cyber-republic/python-grpc-adenine.git`
     
     Follow the README.md instructions on the repo site to build the client.
     
     We are currently having a problem related to the errors when we ran "test.sh" from snart-web. It appears to be due to lack of a jwt token at authentication in both cases.
     
     A typical node-red site appears as follows:
     
 <img src="./Screenshot from 2021-06-25 02-37-18.png">

_________________________________________________________________________________________________________________________________________
     
     
     Good luck! For refs see:

See Using Kubeflow above.

Also refer to any official docs on TensorFlow and its history, background and usage.

## (In particular, visit either https://statlearning.com/ (the Authors' own website) - or -  https://dokumen.pub/introduction-to-statistical-learning-7th-printingnbsped-9781461471370-9781461471387-2013936251.html -  & download "An Introduction to Statistical Learning"; 2017. James, Witten, Hastie, Tibshirani. 441p.). 

Read it slowly, carefully and repeatedly. This represents only the theoretical framework for the more general field of TensorFlow and Machine Learning. One develops, builds, trains, tests and finally deploys Machine Learning "models". 

## (For a more mathematical treatment you can obtain a copy of the Mother of Statistical Learning Texts at https://web.stanford.edu/~hastie/Papers/ESLII.pdf Elements of Statistical Learning 2nd Ed; 2008. Hastie, Tibshirani, Friedman. 764p.)

AI (Artificial Intelligence) includes further technical solutions to involve the results of the deployment of models in military, industrial and commercial production applications, to achieve economic and strategic benefits.
_________________________________________________________________

## NOW: How to use a spatial database in connection with TensorFlow?

I.
A Brain and a 3 dimensional spatial database are both correspondent in meta-structure. It is possible to map 3-D neuronal graphs to a spatial database.

II.
Is it possible, however to model a more-than-3-dimensional Graph and represent it on a PostGIS database?

III.
It appears to us that since it is possible to serialise all data on a sequential computer, it should be possible to store multi-dimensional graphs in a hyper-spatial database. Or is the use of MongoDB indicating that data for these already multi-dimensional Tensors is better stored in a non-relational, non-SQL structure?

IV.
Even if desirable, does PostGIS allow hyperspatiality? How would we connect PostgreSQL + PostGIS in the above 'house' controller, with TensorFlow on the 'uk8s' controller in the kubeflow model, if only to obtain the benefits possible from a strictly GEO-spatial databse system?

V.
At the least, PostGIS is commonly used to ADD the informational capacities introduced by a geo-spatial database to Machine Learning Models.

VI.
Therefore one question is: Is there anything to be gained by Hyper-Dimensional Spatialities? Can Machines be taught and learn within a hyper-spatial cosmos? Is that not what they are doing already, mathematically, in (v)RAM? Can a hyper-spatial database benefit anyone?

VII.
By adding a capacity for a quasi-synchronous (fourth), "Time" dimension, some capabilities could be achieved, compared to "chronostatic" geospatial databases. What could these capacities be?

VIII.
But could there be other uses for further dimensionality, in the fields of Machine Learning? Or is that already obvious to the cognoscenti? Possibly it would be the case that one would require a Database whose spatial dimensionality is a software-design variable, determined individually for each application, but not hard-wired into the Database as a whole?

IX.
Financial modeling (now involving M/L) encompasses certain agreed principles which have been worked out over centuries to retain some rights for customers and borrowers relating to Banks. In the same way as rules have been established to fix financial modeling used by Banks and Money Lenders to ensure fairness to customers, why not apply a similar approach to the Global Financial Models used by Pharmaceutical Companies to determine world pricing. Extra constraints are required to save lives and relieve suffering. Some of us believe profits are killing and disabling people who would otherwise have a chance in this world. Just ask your doctor about Type 1 Diabetes in the so-called third world.

_________________________________________________________________

   My LinkedIn:
                                                                              
   https://www.linkedin.com/in/john-lloyd-olsen/                                                                           
_________________________________________________________________

