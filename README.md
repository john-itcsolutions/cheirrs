## INTRODUCTION:

# CHEIRRS
Project based on  Lxd, Juju, Charms and Kubernetes merged with Cyber Republic's Elastos Smartweb gRPC-based Blockchain and Database Server and SQLAlchemy.

To tackle a full Kubernetes installation, ideally you would need a 32 GB RAM; 250 GB SSD; + HDD: PC (x86_64). eg an Extreme Gaming Computer. If you intend to include Machine Learning/AI capabilities, your Kubeflow installation will go much more easily with an 8 core Host rather than a 4 core one. You really need an Accelerator NVIDIA GPU of at least 10GB vRAM. ITCSA is using a 24GB NVIDIA Tesla K80.

We base initial development such as this locally. It's cheaper!

You need to develop initially on docker. ITCSA uses Ubuntu 20.04 as host platform.

You will not need an Extreme Gaming level of computer for Docker-based (initial - eg. database) work without Kubernetes.

See our website at https://www.itcsolutions.com.au/kubernetes-yaml-file-example/ for an older but more visual idea of this project and others.

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

lxd, juju and kubernetes. Also:

https://jaas.ai/u/stub/postgresql (PostgreSQL without PostGIS initially)

https://jaas.ai/u/juju/redis-charmers (Redis memory-cached, and backed-up, query server for common and predictable transactions)

TensorFlow by Google. 

The predominant language used to code for this project is Python (here, mainly version 3.8).

______________________________________________________________

## Preliminaries

Check your system following here: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#ubuntu-installation

Download and Install CUDA Driver:

`wget https://developer.download.nvidia.com/compute/cuda/11.2.0/local_installers/cuda_11.2.0_460.27.04_linux.run`

`sudo sh ./cuda_11.2.0_460.27.04_linux.run`

We start by installing kubeflow to obtain a controller compatible with this Juju/TensorFlow environment:
________________________________________________________________

## 'KUBEFLOW', TensorFlow and Machine Learning (Artificial Intelligence & Statistical Learning)

Unfortunately the charmed system is mainly oriented for Public Clouds when it comes to the Kubeflow charm bundle. However in combination with microk8s, much can still be achieved ..

From the outermost directory in your working system (on a second HDD if available), check out these repositories locally:

`git clone https://gitlab.com/john_olsenjohn-itcsolutions/cheirrs.git`

`git clone https://github.com/juju-solutions/bundle-kubeflow.git`

`cd bundle-kubeflow`

The below commands will assume you are running them from the bundle-kubeflow directory, which you will mount within your kubeflow vm (see below).

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

Finally, you can run these commands to set up kubeflow/TensorFlow, but you have to have the cloned "bundle-kubeflow", from the above section, available:

`cd /path/to/bundle-kubeflow`

`python3 scripts/cli.py microk8s setup --controller uk8s`

The upcoming deploy-to command allows manually setting a public address that is used for accessing Kubeflow on MicroK8s. However in some deployment scenarios (such as local development), you may need to configure MicroK8s to use LAN DNS instead of the default of 8.8.8.8. To do this, edit the coredns configmap with this command:

`microk8s.kubectl edit configmap -n kube-system coredns`

Edit the lines with 8.8.8.8 8.8.4.4 to use your local DNS, e.g. 192.168.1.2. You will need to use the arrow keys and the 'insert' and 'delete' keys carefully! Save and exit as for vim.

If you make mistakes during editing, it is safest to:

`juju destroy-controller uk8s --destroy-all-models --destroy-storage `

and restart from 

`python3 scripts/cli.py microk8s setup --controller uk8s`

followed by editing the coredns configmap again.

     _____________________________________________

Only when the coredns configmap is correct for your LAN:

`python3 scripts/cli.py deploy-to uk8s`

(Passthrough should already be natively enabled to your Accelerator GPU.)

On Host, you could switch between other possible controllers by noting the current controllers known to juju:

`juju controllers`

and then selecting the target for switching, and:

`juju switch <target-controller-name>`

Within controllers you may substitute <target-model-name> and use:

`juju switch <target-model-name>`

to move between models on the same controller.

______________________________________________________________

# There is a possibility of setting up a Postgres database with PostGIS and Open Street Maps. It appears that the procedure Canonical have taken with TensorFlow above utilises MongoDB, a no-SQL, non-relational database system, as the persistence store ..

As noted below, it is possible, using cross-model referencing, and "offers", to enable an application on a separate controller and/or model, eg the kubeflow model in the uk8s controller, (or just a separate model on the same controller) to access the PostgreSQL/PostGIS database ('house') on the 'house' controller and the 'dbase-bchains' model (see following) therein.

See below at the "## Set up Cross-Model Referenced "offer" .. " heading.

But which `<application-name>` (in kubeflow model) to use as requiring connection to the provided db?

To be continued.

_________________________________________________________________

## A Second Model on a second controller:

(The database schema for ITCSA's project are private and available only under certain conditions.)

In a host terminal, from a second HDD if available, to save working files in case of a crash:

Bootstrap a new controller (when you installed juju, it recognised that microk8s was already installed, and juju created a 'microk8s' cloud for you to use. Verify this with `juju clouds`):

`juju bootstrap microk8s house`

Add a model named "smart-web"

`juju add-model dbase-bchains`

Deploy the Kubernetes Charm

`juju deploy cs:bundle/charmed-kubernetes-559`

`juju config kubernetes-master proxy-extra-args="proxy-mode=userspace"`

`juju config kubernetes-worker proxy-extra-args="proxy-mode=userspace"`

At this stage your microk8s/juju assemblage is converging towards stability. You can observe the status of the assemblage with

`watch -c juju status --color` or, `juju status` for short.

It may take a few hours if your network is slow. Be patient. Nevertheless we do not really require 3 workers, 2 masters and 3 etcd's so you may remove the majority of these machines.

`juju remove-machine <etcd/1_machine-number> --force`

.. and similarly for etcd/2, kubernetes-master/1, kubernetes-worker/1 and kubernetes-worker/2 ..

The earlier in the deployment cycle that you remove these machines the better.

When you see everything 'green' except possibly the master in a permamnent "wait" state ("Waiting for 3 kube-system pods to start"), you may continue.

Deploy PostgreSQL (Juju sorts out Master and Replicating servers automatically).

`juju deploy -n 2 postgresql --storage pgdata=lxd,100G postgresql`

To allow access for administrative purposes from anywhere on your LAN:

`juju config postgresql admin_addresses=0.0.0.0`

Deploy Redis, and make it contactable:

`juju deploy cs:~redis-charmers/redis`

`juju expose redis`

Note; you are user 'ubuntu' here, so if you need a new password, just

`sudo passwd ubuntu`

Later, within the master postgresql database container, you will need to give postgres user a password:

`sudo passwd postgres`

does this.
________________________________________________________________
 
## DATABASE

## Copy sql scripts; Build Database Schema:

From Host, in .... /cheirrs/elastos-smartweb-service/grpc_adenine/database/scripts folder:

`juju scp *.sql <machine number of postgresql master>:/home/ubuntu/`

## The following command would be possible only after you are positively identified, gain our trust, and sign an agreement to work with us, in order to obtain these backup files. Or, develop your own!

`cd ../../../../../ && juju scp *.sql <machine number of postgresql master>:/home/ubuntu/`

where the relevant .sql backup files are outside the 'cheirrs' repository, and generally unavailable publically.

exec into master db container:

`juju ssh <machine number of postgresql master>`

Now you are inside postgres master container, in the /home/ubuntu directory:

`sudo passwd postgres`

Enter your new postgres user's password twice.

`su postgres`

`createdb house`

`psql house < cheirrs_backup.sql`

`psql house < cheirrs_oseer_backup.sql`

`psql house < a_horse_backup.sql`

`psql house < chubba_morris_backup.sql`

`psql house < chubba_morris_oseer_backup.sql`

`psql house < convey_it_backup.sql`

`psql house < convey_it_oseer_backup.sql`

`psql house < the_general_backup.sql`

`psql house < the_general_oseer_backup.sql`

Create users in postgres:

`psql house`

`create role cheirrs_user with login password 'passwd';`

`create role cheirrs_admin with superuser login password 'passwd';`

`create role cheirrs_oseer_admin with superuser login password 'passwd';`

`create role a_horse_admin with superuser login password 'passwd';`

`create role chubba_morris_user with login password 'passwd';`

`create role chubba_morris_admin with superuser login password 'passwd';`

`create role chubba_morris_oseer_admin with superuser login password 'passwd';`

`create role convey_it_user with login password 'passwd';`

`create role convey_it_admin with superuser login password 'passwd';`

`create role convey_it_oseer_admin with superuser login password 'passwd';`

`create role the_general_user with login password 'passwd';`

`create role the_general_admin with superuser login password 'passwd';`

`create role the_general_oseer_admin with superuser login password 'passwd';`

`create role gmu with login password 'gmu';`

Note for the smart-web blockchains to work, gmu must exist as a user with password gmu.

Check Schemas: there should be 'a_horse'; 'cheirrs'; 'cheirrs_oseer', 'chubba_morris', 'chubba_morris_oseer', 'convey_it', 'convey_it_oseer', 'the_general', 'the_general_oseer' and 'public'.

`\dn`

Check off users:

`\du`

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

Exit psql shell and machine:

`\q`

`exit`

`exit`

On Host:

`juju config postgresql admin_addresses=127.0.0.1,0.0.0.0`

Re-enter postgresql master:

`juju ssh <postgresql-master-machine-number>`

Now, back inside postgres master machine at /home/ubuntu:

Run Elastos scripts to prepare database public schema for Blockchains interaction;

`psql -h localhost -d house -U gmu -a -q -f create_table_scripts.sql`

`psql -h localhost -d house -U gmu -a -q -f insert_rows_scripts.sql`

Now if you

`psql house`

then

`\dt` (to reveal tables in default public schema) you should see 3 tables.

Try:

`select * from users;`

You should see the single user's details.
__________________________________________________________________

## Getting PostGIS and Open Street Maps

Inside your postgresql Master (

`juju ssh <postgresql_Master_machine_number>` 

)

get ubuntugis repo:

`sudo add-apt-repository ppa:ubuntugis/ppa`

`sudo apt update`

`sudo apt-get install postgis`

`sudo apt update`

`sudo apt-get install osm2pgrouting`

`psql house`

-- Enable PostGIS

`CREATE EXTENSION postgis;`

-- enable raster support (only for 3+ - may lead to an error - ignorable)

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

_________________________________________________________________

## Set up Cross-Model Referenced "offer" for apps on other models to access PostgreSQL solo installation on this controller called 'localhost-localhost', within this cmr-model called 'smart-web'.

`juju switch house`

`juju offer postgresql:db`

then, if you `juju status` in the k8s model you will see, at the foot of the output, a reference to the Offer.

An application (and users - here admin and ubuntu) set to `consume` the postgres service from a different model and controller (eg here: from the 'uk8s' controller, ie from the 'kubeflow' model), is connected with (this needs to be run while in kubeflow model):

`juju grant admin consume uk8s:admin/smart-web.postgresql`

`juju grant ubuntu consume uk8s:ubuntu/smart-web.postgresql`

.. then the authorised user (in the kubeflow model - see above) may use:

`juju add-relation <application>:db uk8s:admin/smart-web.postgresql:db`

`juju add-relation <application>:db uk8s:ubuntu/smart-web.postgresql:db`

to connect "application" to the database (in smart-web model)under 'uk8s' controller, from the kubeflow model (in this case).
__________________________________________________________________

## Blockchains-Database Server (Smart-web) 

Now we turn to setting up the Blockchain/Database gRPC Server Deployment,

NOTE: As we don't own or control the elastos sub-modules, and since the cheirrs/elastos-smartweb-service/grpc_adenine/__init__.py file is empty in the elastos-smartweb-service module, we have included ITCSA's version of __init__.py in the cheirrs root directory. This version caters for initialising the SQLAlchemy interface from an existing database, and generating a full set of Database Models, using SQLAlchemy's ORM & methods of Database Metadata Reflection. However you need to re-insert the root-directory-version at your /grpc_adenine/__init__.py (in local copies) to enable it to work properly as a Python init file, to be run by the system before running the server in /grpc_adenine/server.py. You would have to keep these 2 versions in sync with each other if you need to edit __init__.py, and want to use your own gitlab account for repo and container registry storage.

`cd path/to/cheirrs`

`sudo rm -f grpc_adenine/__init__.py`

`cp __init__.py grpc_adenine/`

`sudo apt-get update`

`sudo apt-get install -y curl openssh-server ca-certificates tzdata perl`

`sudo apt-get install -y postfix`

From this point there are 3 avenues of progress. The first requires a gitlab account and involves uploading and downloading. The second requires you to set up a local docker registry on the Host. The third appears to be the safest way forward.

## First way:

Gitlab offers a free container registry, along with a free code repository. Sign up for your own.

Once set up in gitlab, create a blank repo, and find "Personal Access Tokens" in your Personal Settings. Obtain and record your token, which you use as a password to login to your Gitlab-hosted Docker container repo.

`docker login -u "<your-gitlab-name>" -p "<your-20-char-token>" registry.gitlab.com`

Now, you need to ensure the image tags in the .yml files you are about to build from are in sync with the actual last image tag you built (+1). This comment always applies to smart-web  Docker-built images, as you progress. This means you have to "bump" along (if you make alterations to the code) the image tags in both the tag given (at the command line - sudo docker build -t registry.gitlab.com/<your_gitlab_name>/smart:<your-tag>) when you build from the Dockerfile to its target, and the kubernetes smart-web.yml file that references that image (ie: "smart:<your-tag>" in smart-web.yml - which is found in cheirrs directory). 

From cheirrs/elastos-smartweb-service directory (where a Dockerfile is located):

`sudo docker build -t registry.gitlab.com/<your_gitlab_name>/smart:<your-tag> .`

`cd ../`

In cheirrs dir:

`docker push registry.gitlab.com/<your_gitlab_name>/smart:<your-tag>`

`git remote add origin git@gitlab.com:<your_gitlab_name>/cheirrs.git`

`git push -u origin --all`

`git push -u origin --tags`

Continued below ..

_________________________________________________________________

## Second way:

find the LAN IP Address of your Host, and copy it to the clipboard:

Create/edit the file:

`sudo nano /etc/docker/daemon.json`

You need to follow the section of the following link that refers to how to set up an insecure local registry; see https://microk8s.io/docs/registry-built-in

`sudo systemctl daemon-reload`

`sudo systemctl restart docker`

Having set up the correct address in your daemon.json,

From cheirrs/elastos-smartweb-service:

`sudo docker build -t localhost:32000/smart:<your-tag> .`

`sudo docker push localhost:32000/smart:<your-tag>`

`cd ../`


From cheirrs dir:

(smart-web.yml is in the root directory of "cheirrs")

`kubectl apply -f smart-web.yml`

`watch kubectl get pods`

_________________________________________________________________

## Third way:

And actually having done all that, we suspect that we must build a "smart-web" charm, rather than simply using kubectl to deploy the software. Otherwise we may have no simple mechanisms for smart-web to find and connect to its environment.

# TO BE CONTINUED .. we're learning to use Docker to build charms now ..

_____________________________________________________________

## TESTING the smartweb-service/Blockchains/Postgresql System

To be continued ..
_____________________________________________________________


________________________________________________________________

Good luck! For refs see:

https://jaas.ai/kubeflow#setup-microk8s and find microk8s section, and following ('Using')

Also refer to any official docs on TensorFlow and its history, background and usage.

## (In particular, visit either https://statlearning.com/ (the Authors' own website) - or -  https://dokumen.pub/introduction-to-statistical-learning-7th-printingnbsped-9781461471370-9781461471387-2013936251.html -  & download "An Introduction to Statistical Learning"; Gareth James et al.). 

Read it slowly, carefully and repeatedly. This represents only the theoretical framework for the more general field of TensorFlow and Machine Learning. One develops, builds, trains, tests and finally deploys Machine Learning "models". 

AI (Artificial Intelligence) includes further technical solutions to involve the results of the deployment of models in industrial and commercial production applications, to achieve economic and strategic benefits.
_________________________________________________________________

## NOW: How to use a spatial database in connection with TensorFlow?

I.
A Brain and a 3 dimensional spatial database are both correspondent in meta-structure. It is possible to map 3-D neuronal graphs to a spatial database.

II.
Is it possible, however to model a more-than-3-dimensional Graph and represent it on a PostGIS database?

III.
It appears to us that since it is possible to serialise all data on a sequential computer, it should be possible to store multi-dimensional graphs in a hyper-spatial database. Or is the use of MongoDB indicating that data for these already multi-dimensional Tensors is better stored in a non-relational, non-SQL structure?

IV.
Even if desirable, does PostGIS allow hyperspatiality? How would we connect PostgreSQL + PostGIS in the above uk8s sub-installation, with TensorFlow on the uk8s controller in the kubeflow model, if only to obtain the benefits possible from a strictly GEO-spatial databse system?

V.
At the least, PostGIS is commonly used to ADD the informational capacities introduced by a geo-spatial database to Machine Learning Models.

VI.
Therefore one question is: Is there anything to be gained by Hyper-Dimensional Spatialities? Can Machines be taught and learn within a hyper-spatial cosmos? Is that not what they are doing already, mathematically, in RAM? Can a hyper-spatial database benefit anyone?

VII.
By adding a capacity for a quasi-synchronous (fourth), "Time" dimension, some capabilities could be achieved, compared to "chronostatic" geospatial databases. What could these capacities be?

VIII.
But could there be other uses for further dimensionality? Or is that already obvious to the cognoscenti?

IX.
In the same way as rules have been established to fix financial modeling used by Banks to ensure fairness to customers (over the centuries), why not apply a similar approach to the global financial models used by Pharmaceutical Companies to determine world pricing. Extra constraints are rquired to save lives and relieve suffering. Some of us believe profits are killing and disabling people who would otherwise have a chance in this world. Just ask your doctor about Type 1 Diabetes in the so-called third world.

_________________________________________________________________

_________________________________________________________________


# To be continued ..
