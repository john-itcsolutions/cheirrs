#!/bin/bash

# dbase_setup_2.sh script

sudo apt update && sudo apt-get install -y postgis postgresql-12-postgis-3 && sudo apt-get install postgresql-12-postgis-3-scripts && sudo apt update && sudo apt-get install -y osm2pgrouting