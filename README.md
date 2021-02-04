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

TensorFlow by Google. `juju deploy cs:~johnsca/tensorflow-0`

The predominant language used to code for this project is Python (here, mainly version 3.8).

_________________________________________________________________

## SET UP NODES:

(The database schema for ITCSA's project are private and available only under certain conditions.)

Development is easiest in Docker as opposed to Kubernetes.

Nevertheless, if you wish to go on to build a full set of nodes enabled on Kubernetes, we use lxd, juju, as follows.

On host terminal, preferably in a directory within the 2nd HDD if available, to save working files in case of a crash:

Install lxd

`sudo snap install lxd`

`sudo lxd init`

Note: Currently, Charmed Kubernetes only supports dir as a storage option and does not support ipv6, which should be set to none from the init script. Additional profiles will be added automatically to LXD to support the requirements of Charmed Kubernetes.

Install juju

`sudo snap install juju --classic`

`sudo snap install juju-wait --classic`

`sudo snap install juju-helpers --classic`

Create a Juju Controller for this Cloud

`juju bootstrap localhost`

Add a model named "k8s"

`juju add-model k8s`

Deploy the Kubernetes Charm

`juju deploy cs:bundle/charmed-kubernetes-559`

`juju config kubernetes-master proxy-extra-args="proxy-mode=userspace"`

`juju config kubernetes-worker proxy-extra-args="proxy-mode=userspace"`

At this stage your lxd/juju assemblage is converging towards stability. You can observe the status of the assemblage with

`watch -c juju status --color` or, `juju status` for short.

It may take a few hours if your network is slow. Be patient. Nevertheless we do not really require 3 workers, 2 masters and 3 etcd's so you may remove these machines.

`juju remove-machine <etcd/1_machine-number> --force`

.. and similarly for etcd/2, kubernetes-master/1, kubernetes-worker/1 and kubernetes-worker/2 ..

The earlier in the deployment cycle that you remove these machines the better.

When you see everything 'green' except possibly the master in a permamnent "wait" state ("Waiting for 3 kube-system pods to start"), you may continue.

Deploy PostgreSQL (Juju sorts out Master and Replicating servers automatically). Note; when lxd was set up, storage space was also set up on the local SSD.

`juju deploy --config admin_addresses='127.0.0.1','192.168.1.7' -n 2 postgresql --storage pgdata=lxd,50G postgresql`

# The second IP address in the above command should be your own   Host's IP Adress.

Deploy Redis, make it contactable:

`juju deploy cs:~redis-charmers/redis`

`juju expose redis`

Note; you are user 'ubuntu' here, so if you need a new password, just

`sudo passwd ubuntu`

 <!-- ## DATABASE & REDIS:- Set Up:

NOTE: As yet Redis is not programmed to act as a Query Cache Server. This requires investment of time and effort in analysis of your DApp's requirements.

As a separate matter, ITCSA is experimenting with the "discourse" charm to link the redis and postgres machines. See https://charmhub.io/discourse/docs/database-relations

`juju deploy cs:~discourse-charmers/discourse-k8s` or even `juju deploy cs:~discourse-charmers/discourse`

The charm will not function without a connection to a PostgreSQL database and Redis, so they do need to be running and ready first.
_
`juju config discourse redis_host=${REDIS_IP}`

(where you need to replace ${REDIS_IP} with the IP of the redis machine - see:

`juju status`
)

`juju relate discourse postgresql:db-admin`

Au fin du jour, nous avons été déçus ..  -->
________________________________________________________________
 
## DATABASE

## Copy sql scripts; Build Database Schema:

From Host, in /elastos-smartweb-service/grpc_adenine/database/scripts folder:

`juju scp *.sql <machine number of postgresql master>:/home/ubuntu/`

## The following command would be possible only after you are positively identified, gain our trust, and sign an agreement to work with us, in order to obtain these backup files. Or, develop your own!

`cd ../../../../../ && juju scp *.sql <machine number of postgresql master>:/home/ubuntu/`

exec into master db container:

`juju ssh <machine number of postgresql master>`

Now you are inside postgres master container, in the /home/ubuntu directory:

`sudo passwd postgres`

Enter your new postgres user's password twice.

`su postgres`

`createdb general`

`psql general < cheirrs_backup.sql`

`psql general < cheirrs_oseer_backup.sql`

`psql general < a_horse_backup.sql`

Create users in postgres:

`psql general`

`create role cheirrs_user with login password 'passwd';`

`create role cheirrs_admin with superuser login password 'passwd';`

`create role cheirrs_oseer_admin with superuser login password 'passwd';`

`create role a_horse_admin with superuser login password 'passwd';`

`create role gmu with login password 'gmu';`

Check Schemas: there should be 'public, 'a_horse'; 'cheirrs'; 'cheirrs_oseer'.

`\dn`

Check off users:

`\du`

`\dt ` should reveal no instances (in default public schema)

`set search_path to cheirrs;`

.. now, `\dt` should reveal a full set of 600+ tables in 2 categories: 1) accounting_<xyz> and 2) uc_<uvw> ('uc_' for use_case)

Identical results will appear for:

`set search_path to cheirrs_oseer;`

and,

`set search_path to a_horse;`

when you run 

`\dt`

In postgres master machine:

Exit psql shell:

`\q`

Still inside postgres master machine:

Run Elastos scripts to prepare database public schema for Blockchains interaction;

`psql -h localhost -d general -U gmu -a -q -f create_table_scripts.sql`

`psql -h localhost -d general -U gmu -a -q -f insert_rows_scripts.sql`

Now if you

`psql general`

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

get ubuntugis repo

`sudo add-apt-repository ppa:ubuntugis/ppa`

`sudo apt update`

`sudo apt-get install postgis`

`sudo apt update`

`sudo apt-get install osm2pgrouting`

`psql general`

-- Enable PostGIS
`CREATE EXTENSION postgis;`
-- enable raster support (for 3+)
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

## Set up Cross-Model Referenced "offer" for apps on other models to access PostgreSQL solo installation on this cmr-model called 'k8s'.

`juju switch k8s`

`juju offer postgresql:db`

then, if you `juju status` in the k8s model you will see, at the foot of the output, a reference to the Offer.

An application (and user - here admin) set to `consume` the postgres service from a different model and controller (eg here: from the 'uk8s' controller, ie from the 'kubeflow' model), is connected with (this needs to be run while in kubeflow model):

`juju grant admin consume localhost-localhost:admin/k8s.postgresql`

`juju grant ubuntu consume localhost-localhost:ubuntu/k8s.postgresql`

.. then the authorised user (in the kubeflow model - see below)may use:

`juju add-relation <application>:db localhost-localhost:admin/k8s.postgresql:db`

to connect "application" to the database from the uk8s controller in the kubeflow model (in this case).
__________________________________________________________________

## Blockchains-Database Server (Smart-web) 

Now we turn to setting up the Blockchain/Database gRPC Server Deployment,

In a Host terminal,

`git clone https://gitlab.com/john_olsenjohn-itcsolutions/cheirrs`

NOTE: As we don't own or control the elastos sub-modules, and since the cheirrs/elastos-smartweb-service/grpc_adenine/__init__.py file is empty in the elastos-smartweb-service module, we have included a version of __init__.py in the cheirrs root directory. This version caters for initialising the SQLAlchemy interface from an existing database, and generating a full set of Models, using SQLAlchemy's ORM & methods of Database Metadata Reflection. However we need to re-insert the root-directory-version at /grpc_adenine/__init__.py (in local copies) to enable it to work properly as a Python init file, to be run by the system before running the server in /grpc_adenine/server.py. You would have to keep these 2 versions in sync with each other if you need to edit __init__.py, and want to use your own gitlab account for repo and container registry storage.

`cd path/to/cheirrs`

`sudo rm -f grpc_adenine/__init__.py`

`cp __init__.py grpc_adenine/`

`sudo apt-get update`

`sudo apt-get install -y curl openssh-server ca-certificates tzdata perl`

`sudo apt-get install -y postfix`

Gitlab offers a container registry, along with a code repository. Sign up for your own.

Once set up in gitlab, create a blank repo, and find "Personal Access Tokens" in your personal settings. Obtain and record your token, which you use as a password to login to your Gitlab-hosted Docker container repo.

`docker login -u "<your-gitlab-name>" -p "<your-20-char-token>" registry.gitlab.com`

From elastos-smartweb-service directory (where a Dockerfile is located):

`sudo docker build -t registry.gitlab.com/<your_gitlab_name>/smart:1 .`

`cd ../`

In cheirrs/elastos-smartweb-service dir:

`docker push registry.gitlab.com/<your_gitlab_name>/smart:1`

`git remote add origin git@gitlab.com:<your_gitlab_name>/cheirrs.git`

`git push -u origin --all`

`git push -u origin --tags`

From cheirrs dir:

Now, you need to ensure the image tags in the .yml files you are about to build from are in sync with the actual last image tag you built (+1). This comment always applies to smart-web  Docker-built images, as you progress. This means you have to "bump" along the image tags in both the tag given (at the command line - sudo docker build -t registry.gitlab.com/<your_gitlab_name>/smart:<your-tag>) when you build from the Dockerfile to its target, and the kubernetes smart-web.yml file that references that image (ie: "smart:<your-tag>"). 

(smart-web.yml is in the root directory of "cheirrs")

`kubectl apply -f smart-web.yml`

`watch kubectl get pods`

And actually having done all that, we suspect that we must build a "smart-web" charm, rather than simply using kubectl to deploy the software. Otherwise we may have no simple mechanisms for smart-web to find and connect to its environment.

# TO BE CONTINUED .. we're learning to build charms now ..

_____________________________________________________________

## TESTING the smartweb-service/Blockchains/Postgresql System


_____________________________________________________________

## 'KUBEFLOW', TensorFlow and Machine Learning (Artificial Intelligence & Statistical Learning)

Unfortunately the charmed system is oriented for Public Clouds when it comes to the Kubeflow charm bundle. However in combination with microk8s, much can still be achieved ..

From the outermost directory in your working system, check out this repository locally:

`git clone https://github.com/juju-solutions/bundle-kubeflow.git`

`cd bundle-kubeflow`

The below commands will assume you are running them from the bundle-kubeflow directory within your kubeflow vm.

Then, follow the instructions from the subsection below to deploy Kubeflow to microk8s.

Microk8s is the only way to easily obtain a working Kubeflow/tensorflow installation on your localhost without paying cloud fees ..

Setup microk8s with multipass on the Ubuntu Host:

`sudo snap install multipass`

`multipass launch -c 4 -d 50G -m 20G -n kubeflow`

(you'll also need to install the microk8s snap on your new vm:)

Enter kubeflow vm:

`multipass shell kubeflow`

inside kubeflow on /home/ubuntu:

`mkdir shared`

On this Ubuntu vm, you'll need to install these snaps to get started:

`sudo snap install juju --classic`
`sudo snap install juju-wait --classic`
`sudo snap install juju-helpers --classic`

Then, mount your outer working directory to kubeflow -

`exit`

`multipass mount /path/to/your/working/directory kubeflow:/home/ubuntu/shared`

`multipass shell kubeflow`

`sudo snap install microk8s --classic`

Next, you will need to add yourself to the microk8s group:

`sudo usermod -aG microk8s $USER && newgrp microk8s`

Finally, you can run these commands to set up microk8s, but you have to have the cloned "bundle-kubeflow", from the above section, available from /home/ubuntu/shared:

`cd shared/../path/to/bundle-kubeflow`

`python3 scripts/cli.py microk8s setup --controller uk8s`

The upcoming deploy-to command allows manually setting a public address that is used for accessing Kubeflow on MicroK8s. In some deployment scenarios, you may need to configure MicroK8s to use LAN DNS instead of the default of 8.8.8.8. To do this, edit the coredns configmap with this command:

`microk8s.kubectl edit configmap -n kube-system coredns`

Edit the line with 8.8.8.8 8.8.4.4 to use your local DNS, e.g. 192.168.1.2. You will need to use the 'insert' and 'delete' keys carefully! Save and exit as for vim.

`python3 scripts/cli.py deploy-to uk8s`

(Passthrough should be natively enabled to your Accelerator GPU.)

______________________________________________________________

# There is commented-out text below (hidden), refering to setting up a Postgres database with PostGIS and Open Street Maps. It appears that the procedure above utilises MongoDB, a no-SQL, non-relational database system, as the persistence store ..

As noted above, it is possible, using cross-model referencing, and "offers", to enable an application in a separate controller and model, eg the kubeflow model in the uk8s controller, (or just a separate model on the same controller) to access the PostgreSQL/PostGIS database ('general') on the localhost-localhost controller and the k8s model therein. (See above at the "## Set up Cross-Model Referenced "offer" .. " heading.)

To be continued.

______________________________________________________________

<!-- FROM HOST TERMINAL: clone the following repo to your outermost working directory

`cd ../[[../]../], etc`

`git clone https://github.com/john-itcsolutions/smart-web-postgresql-grpc`

`cd smart-web-postgresql-grpc`

## Database Preliminaries:

IN HOST TERMINAL:
 
 We pull the images we need:
 
 `docker pull redis:5.0.4`

 `docker pull postgres:10.15`
 
 `sudo nano /etc/docker/daemon.json`

 You need to have something like:
 
`{`

`  insecure-registries : [localhost:32000,`

`                     ]`
`}`

Then:

`sudo systemctl daemon-reload`

`sudo systemctl restart docker`

`docker tag redis:5.0.4 localhost:32000/redis:5.0.4`

`docker tag postgres:10.15 localhost:32000/postgres:10.15`

Now push the images to the microk8s registry:

`docker push localhost:32000/redis:5.0.4`

`docker push localhost:32000/postgres/10:15`

_____________________________________________________________

## DATABASE & REDIS:- Set Up secrets:

In the absence of a database (in the charmed-kubernetes installation) within scope of tensorflow, we will provide a second postgresql replicated set on microk8s.

Note: "You can edit secret.yml, and you would have to edit kustomization.yaml, but then you need to alter the redis.yml as the hash for the keys will change. So you would have to find the hashes in that yml file and alter to match newly created keys - from running `microk8s kubectl apply -k .`"

Run `microk8s kubectl apply -f config/secret.yml` and then `cd config && ./create_configmap.sh`    

`cd ../../`

Generate further secrets from kustomization file (in smart-web-postgresql-grpc dir):

`microk8s kubectl apply -k .`

________________________________________________________________

 ## Set Up Redis
 
 In smart-web-postgresql-grpc directory:
 
 `sudo ./volumes-redis.sh`
 
 `sudo ./copyredisconf.sh`
 
 which copies redis.conf (unedited as yet) to the config directory.
 
 You then need to edit redis.conf in place (ie in /mnt/disk/config-redis) and insert the name of the data backup folder which the dump.rdb file will be placed in. You must search redis.conf for the correct line to edit.
 
 First see what folders you have:
 
 `ls /mnt/disk`
 
 Then:
 
 `sudo nano /mnt/disk/config-redis/redis.conf`
 
 The name of the data backup foldder is /mnt/disk/data-redis, however, relative to the location of redis.conf you need to insert 
 
 `../data-redis`, inside redis.conf, at the approriate position.

`cd /path/to/smart-web-postgresql-grpc`

`microk8s kubectl apply -f redis.yml`

check pods .. `watch microk8s kubectl get pods`

NOTE: As yet Redis is not programmed to act as a Query Cache Server. This requires investment of time and effort in analysis of your DApp's requirements.
________________________________________________________________

## DATABASE
## Create places for Persistent Volumes on database node and allow access:

From postgres-statefulset directory:

`sudo ./volumes-postgres.sh`

________________________________________________________________

## Start master and replica:

In primary node, in "shared" directory and inside "smart-web-postgresql-grpc/app/postgres-statefulset" folder, as above, start master postgres server:

`microk8s kubectl apply -f statefulset-master.yml`

`watch microk8s kubectl get pods`

If errors or excessive delay get messages with:

`microk8s kubectl describe pods`

 .. fix errors!
 
 After master is successfully running and ready, start replica server:

`microk8s kubectl apply -f statefulset-replica.yml`
 
 Check pods.

## Getting PostGIS and Open Street Map for 'Kubeflow'-PostgreSQL

It's worth noting that PostGIS is capable of storing representations of Neural Networks. The original Design Case for TensorFlow was as a Deep Learning Neural Network Simulator.

Inside your postgresql Master ie with

`microk8s exec -it postgresql-0 -- sh` 

get ubuntugis repo

`sudo add-apt-repository ppa:ubuntugis/ppa`

`sudo apt update`

`sudo apt-get install postgis`

`sudo apt update`

`sudo apt-get install osm2pgrouting`

(Make sure you are running a debian or ubuntu-based version of postgres, not the alpine version)
 -->

________________________________________________________________

Good luck! For refs see:

https://jaas.ai/kubeflow#setup-microk8s and find microk8s section, and following ('Using')

Also refer to any official docs on TensorFlow and its history, background and usage.

## (In particular, see either https://statlearning.com/ (the Authors' own website) - or -  https://dokumen.pub/introduction-to-statistical-learning-7th-printingnbsped-9781461471370-9781461471387-2013936251.html -  download "An Introduction to Statistical Learning"; Gareth James et al.). 

Read it slowly, carefully and repeatedly. This represents only the theoretical framework for the more general field of TensorFlow and Machine Learning. One develops, builds, trains, tests and finally deploys Machine Learning "models". 

AI (Artificial Intelligence) includes further technical solutions to involve the results of the deployment of models in industrial and commercial production applications, to achieve economic and strategic benefits.
_________________________________________________________________

## NOW: How to use a spatial database in connection with TensorFlow?

1.
A Brain and a 3 dimensional spatial database are both correspondent in meta-structure. It is possible to map 3-D neuronal graphs to a spatial database.

2.
Is it possible, however to model a more-than-3-dimensional Graph and represent it on a PostGIS database?

3.
It appears to us that since it is possible to serialise all data on a sequential computer, it should be possible to store multi-dimensional graphs in a hyper-spatial database.

4.
Does PostGIS allow this? How to connect PostgreSQL with PostGIS in the above microk8s sub-installation, with TensorFlow?

5.
At the least, PostGIS is commonly used to ADD the informational capacities introduced by a geo-spatial database to Machine Learning Models.

6.
Therefore one question is: Is there anything to be gained by Hyper-Dimensional Spatialities? Can Machines be taught and learn within a hyper-spatial cosmos? Is that not what they are doing already, mathematically? Can a hyper-spatial database benefit anyone?

7.
By adding a capacity for a quasi-synchronous (fourth), "Time" dimension, some capabilities could be achieved, compared to "chronostatic" geospatial databases. What could these capacities be?

8.
But could there be other uses for further dimensionality? Or is that already obvious to the cognescenti?

9.
In the same way as rules have been established to fix financial modeling used by Banks to ensure fairness to customers (over the centuries), why not apply a similar approach to the global financial models used by Pharmaceutical Companies to determine world pricing. Some of us believe profits are killing and disabling people who would otherwise have a chance in this world. Just ask about Type 1 Diabetes in the so-called third world.

__________________________________________________________________

_________________________________________________________________


# To be continued ..
