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

TensorFlow by Google. https://www.tensorflow.org/install/pip#tensorflow-2-packages-are-available

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

Create a Juju Controller for this Cloud

`juju bootstrap localhost`

Add a model named "k8s"

`juju add-model k8s`

Deploy the Kubernetes Charm

`juju deploy charmed-kubernetes`

`juju config kubernetes-master proxy-extra-args="proxy-mode=userspace"`

`juju config kubernetes-worker proxy-extra-args="proxy-mode=userspace"`

At this stage your lxd/juju assemblage is converging towards stability. You can observe the status of the assemblage with

`watch -c juju status --color` or, `juju status` for short.

It may take a few hours if your network is slow. Be patient. When you see everything 'green' except possibly the 2 masters in a permamnent "wait" state ("Waiting for 3 kube-system pods to start"), you may continue.

Deploy PostgreSQL (Juju sorts out Master and Replicating servers automatically). Note; when lxd was set up, storage space was also set up on the local SSD.

`juju deploy --config admin_addresses='127.0.0.1','192.168.1.7' -n 2 postgresql --storage pgdata=lxd,50G postgresql`

# The second IP address in the above command should be your own   Host's IP Adress.

Deploy Redis, make it contactable:

`juju deploy cs:~redis-charmers/redis`

`juju expose redis`

Note; you are user 'ubuntu' here, so if you need a new password, just

`sudo passwd ubuntu`

_________________________________________________________________

 ## DATABASE & REDIS:- Set Up:

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

Au fin du jour, nous avons été déçus .. 


________________________________________________________________
 
## DATABASE

## Copy sql scripts; Build Database Schema:

From Host, in /elastos-smartweb-service/grpc_adenine/database/scripts folder:

`juju scp create_table_scripts.sql <machine number of postgresql master>:/var/lib/postgresql/10/main/`

`juju scp insert_rows_scripts.sql <machine number of postgresql master>:/var/lib/postgresql/10/main/`

`juju scp reset_database.sql <machine number of postgresql master>:/var/lib/postgresql/10/main/`

## The following 3 commands would be possible only after you are positively identified, gain our trust, and sign an agreement to work with us, in order to obtain these backup files. Or, develop your own!

`juju scp ../../cheirrs_backup.sql <machine number of postgresql>:/var/lib/postgresql/10/main/`

`juju scp ../../cheirrs_oseer_backup.sql <machine number of postgresql>:/var/lib/postgresql/10/main/`

`juju scp ../../a_horse_backup.sql <machine number of postgresql>:/var/lib/postgresql/10/main/`

exec into master db container:

`juju ssh <machine number of postgresql>`

Inside postgres master container:

`sudo passwd postgres`

Enter your new postgres user's password twice.

`su postgres`

`createdb general`

`psql general < /var/lib/postgresql/10/main/cheirrs_backup.sql`

`psql general < /var/lib/postgresql/10/main/cheirrs_oseer_backup.sql`

`psql general < /var/lib/postgresql/10/main/a_horse_backup.sql`

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

`psql -h localhost -d general -U gmu -a -q -f /var/lib/postgresql/10/main/create_table_scripts.sql`

`psql -h localhost -d general -U gmu -a -q -f /var/lib/postgresql/10/main/insert_rows_scripts.sql`

Now if you

`psql general`

then

`\dt` (to reveal tables in default public schema) you should see 3 tables.

Try:

`select * from users;`

You should see the single user's details.
__________________________________________________________________

## Getting PostGIS and Open Street Map

Inside your postgresql Master 

`juju ssh <postgresql_Master_machine_number>` 

get ubuntugis repo

`sudo add-apt-repository ppa:ubuntugis/ppa`

`sudo apt update`

`sudo apt-get install postgis`

`sudo apt update`

`sudo apt-get install osm2pgrouting`
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

And actually having done all that, we realised that we really must build a "smart-web" charm, rather than simply using kubectl to deploy the software. Otherwise we have no simple mechanisms for smart-web to find and connect to its environment.

TO BE CONTINUED .. we're learning to build charms now ..

_____________________________________________________________

## TESTING the smartweb-service/Blockchains/Postgresql System


_____________________________________________________________

## 'KUBEFLOW', TensorFlow and Machine Learning (Artificial Intelligence & Statistical Learning)

On juju you will need to have available, and allow for, 16GB of RAM at least, and 4 cpu cores in your 'kubeflow' virtual machine. This means you need a second model which you configure at 4 cores (if you have an 8 core or better machine) and mem=16G.

For genuine processing capacity, also necessary is at least 10GB of GPU Accelerator Card RAM. The card needs to be CUDA Architecture-compatible.

`juju add-model --config cores=4 --config mem=16G kubeflow`

This may seem a large lot for 3 workers at 4 cores and 16GB each, however we will be removing the kubernetes-worker/1 and kubernetes/2 units (--force) as well as one master.

This will leave 1 Master (2 cores default) and 1 x 4-core 16GB RAM worker for tensorflow.

`juju deploy charmed-kubernetes`

`juju config kubernetes-master proxy-extra-args="proxy-mode=userspace"`

`juju config kubernetes-worker proxy-extra-args="proxy-mode=userspace"`

`juju remove-unit kubernetes-worker/1 --force`

`juju remove-machine <kubernetes-worker/1_machine_number> --force`

`juju remove-unit kubernetes-worker/2 --force`

`juju remove-machine <kubernetes-worker/2_machine_number> --force`

`juju remove-unit kubernetes-master/1 --force`

`juju remove-machine <kubernetes-master/1_machine_number> --force`

After the model has converged and settled, as with k8s model, you will probably require a relational database system. However we intend to set up the postgresql database in k8s model as a cross model referencing database by setting up an "offer" for it so that applications (charms) from other models may access the database. In this case the tensorflow charm will access postgresql vi cross model referencing, although it may require a caching server as a web interface participant (unsure right now):

`juju deploy cs:~redis-charmers/redis`

`juju expose redis`

`juju deploy cs:~johnsca/tensorflow-0`

Passthrough is natively enabled to the Accelerator GPU.

Good luck! (see either https://statlearning.com/ (the Authors' own website) - or -  https://dokumen.pub/introduction-to-statistical-learning-7th-printingnbsped-9781461471370-9781461471387-2013936251.html -  download "An Introduction to Statistical Learning"; Gareth James et al.). 

Read it slowly, carefully and repeatedly. This represents only the theoretical framework for the more general field of TensorFlow and Machine Learning. One develops, builds, trains, tests and finally deploys Machine Learning "models". 

AI (Artificial Intelligence) includes further technical solutions to involve the results of the deployment of models in industrial and commercial production applications, to achieve economic and strategic benefits.


## Getting PostGIS and Open Street Map for 'Kubeflow'-PostgreSQL

It's worth noting that PostGIS is capable of storing representations of Neural Networks. The original Design Case for TensorFlow was as a Deep Learning Neural Network Simulator.

Your database has already been set up within the cross model referenced database (postgresql) in k8s.
_________________________________________________________________

## NOW: How to use a spatial database in connection with TensorFlow?

1.
A Brain and a 3 dimensional spatial database are both correspondent in meta-structure. It is possible to map 3-D neuronal graphs to a spatial database.

2.
Is it possible, however to model a more-than-3-dimensional Graph and represent it on a PostGIS database?

3.
It appears to us that since it is possible to serialise all data on a sequential computer, it should be possible to store multi-dimensional graphs in a hyper-spatial database.

4.
Does PostGIS allow this?

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
