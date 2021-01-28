## INTRODUCTION:

# CHEIRRS
Project based on  Lxd, Juju, Charms and Kubernetes merged with Cyber Republic's Elastos Smartweb gRPC-based Blockchain and Database Server and SQLAlchemy.

To tackle a full Kubernetes installation, ideally you would need a 32 GB RAM; 250 GB SSD; + HDD: PC (x86_64). eg an Extreme Gaming Computer. If you intend to include Machine Learning/AI capabilities, your Kubeflow installation will go much more easily with an 8 core Host rather than a 4 core one. You really need an Accelerator NVIDIA GPU of at least 10GB vRAM. ITCSA is using a 24GB NVIDIA Tesla K80.

We base initial development such as this locally. It's cheaper!

You need to develop initially on docker. ITCSA uses Ubuntu 20.04 as host platform.

You will not need an Extreme Gaming level of computer for Docker-based (initial - eg. database) work without Kubernetes.

See our website at https://www.itcsolutions.com.au/kubernetes-yaml-file-example/ for an older but more visual idea of this project and others.

## Get:

Docker for Ubuntu: https://docs.docker.com/engine/install/ubuntu/

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

https://jaas.ai/u/juju/redis-k8s (Redis memory-cached, and backed-up, query server for common and predictable transactions)

TensorFlow by Google. https://www.tensorflow.org/install/pip#tensorflow-2-packages-are-available

The predominant language used to code for this project is Python (here, mainly version 3.8).

_______________________________________________________________________________

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

It's essential to add a model named "k8s"

`juju add-model k8s`

Deploy the Kubernetes Charm

`juju deploy charmed-kubernetes`

`juju config kubernetes-master proxy-extra-args="proxy-mode=userspace"`

`juju config kubernetes-worker proxy-extra-args="proxy-mode=userspace"`

At this stage your lxd/juju assemblage is converging towards stability. You can observe the status of the assemblage with

`watch -c juju status --color` or, `juju status` for short.

It may take a few hours if your network is slow. Be patient. When you see everything 'green' except possibly the 2 masters in a permamnent "wait" state ("Waiting for 3 kube-system pods to start"), you may continue.

Deploy PostgreSQL (Juju sorts out Master and Replicating servers automatically). Note; when lxd was set up, storage space was also set up on the local SSD.

`juju deploy -n 2 postgresql --storage pgdata=lxd,50G`

Deploy Redis master and slave, make the master contactable, and relate them:

`juju deploy redis redis-mas`

`juju deploy redis redis-slav`

`juju expose redis-mas`

`juju add-relation redis-mas:master redis-slav:slave`

Follow the instructions here:
https://www.tensorflow.org/install/pip to install TensorFlow onto a machine of your choice.

Choose your machine and `juju ssh <machine-number>`

Follow the above instructions carefully inside this virtual machine. Passthrough is natively enabled to the Accelerator GPU.

Note; you are user 'ubuntu' here, so if you need a new password, just

`sudo passwd ubuntu`

___________________________________________________________________________________________

 ## DATABASE & REDIS:- Set Up:

NOTE: As yet Redis is not programmed to act as a Query Cache Server. This requires investment of time and effort in analysis of your DApp's requirements.

________________________________________________________________________________________



 _________________________________________________________________
 

## KUBEFLOW and Machine Learning (Artificial Intelligence & Statistical Learning)

On juju you will need to have available, and allow for, 16GB of RAM at least, and 4 cpu cores in your 'kubeflow' virtual machine.

For genuine processing capacity, also necessary is at least 10GB of GPU Accelerator Card RAM. The card needs to be CUDA Architecture-compatible.

Good luck! (see either https://statlearning.com/ (the Authors' own website) - or -  https://dokumen.pub/introduction-to-statistical-learning-7th-printingnbsped-9781461471370-9781461471387-2013936251.html -  download "An Introduction to Statistical Learning"; Gareth James et al.). 

Read it slowly, carefully and repeatedly. This represents only the theoretical framework for the more general field of TensorFlow and Machine Learning. One develops, builds, trains, tests and finally deploys Machine Learning "models". 

AI (Artificial Intelligence) involves further technical solutions to involve the results of the deployment of models in industrial and commercial production, to achieve economic benefits.

_____________________________________________________________________

## DATABASE

__________________________________________________________________


## Copy sql scripts; Build Database Schema:

From primary, in /elastos-smartweb-service/grpc_adenine/database/scripts folder:

`juju scp create_table_scripts.sql <machine number of postgresql master>:/var/lib/postgresql/10/main/`

`juju scp insert_rows_scripts.sql <machine number of postgresql master>:/var/lib/postgresql/10/main/`

`juju scp reset_database.sql <machine number of postgresql master>:/var/lib/postgresql/10/main/`

## The following 3 commands would be possible only after you are positively identified, gain our trust, and sign an agreement to work with us, in order to obtain these backup files. Or, develop your own!

`juju scp ../../cheirrs_backup.sql <machine number of postgresql master>:/var/lib/postgresql/10/main/`

`juju scp ../../cheirrs_oseer_backup.sql <machine number of postgresql master>:/var/lib/postgresql/10/main/`

`juju scp ../../a_horse_backup.sql <machine number of postgresql master>:/var/lib/postgresql/10/main/`

exec into master db container:

`juju ssh <machine number of postgresql master>`

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
____________________________________________________________________________________________

## Blockchains-Database Server (Smart-web) 

Now we turn to setting up the Blockchain/Database gRPC Server Deployment,

In a Host terminal,

`git clone https://gitlab.com/john_olsenjohn-itcsolutions/cheirrs`

`cd path/to/cheirrs`

`sudo apt-get update`

`sudo apt-get install -y curl openssh-server ca-certificates tzdata perl`

`sudo apt-get install -y postfix`

Gitlab offers a container registry, along with a code repository. Sign up for your own.

Once set up in gitlab, create a blank repo, then in Host terminal:

`sudo docker build -t registry.gitlab.com/<your_gitlab_name>/smart:1 .`

`ssh-keygen -t ed25519 -C "your-key"`

`cat ~/.ssh/id_ed25519.pub`

`docker push registry.gitlab.com/<your_gitlab_name>/smart:1`

From cheirrs directory:

`sudo docker build -t registry.gitlab.com/<your_gitlab_name>/smart:1 .`

`ssh-keygen -t ed25519 -C "your-key"`

`cat ~/.ssh/id_ed25519.pub`

`git remote add origin git@gitlab.com:<your_gitlab_name>/smart.git`

`git push -u origin --all`

`git push -u origin --tags`

Next, in Host terminal:

`cd path/to/cheirrs`

Now, you need to ensure the image tags in the .yml files you are about to build from are in sync with the actual last image tag you built (+1). This comment always applies to smart-web  Docker-built images, as you progress. This means you have to "bump" along the image tags in both the tag given for the Dockerfile build target, and the kubernetes smart-web.yml file that references that image (smart-web.yml is in the root directory of "smart").

`kubectl apply -f smart-web.yml`

`watch kubectl get pods`

_____________________________________________________________

## TESTING



# To be continued ..
