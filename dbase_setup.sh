#!/bin/bash

# dbase_setup.sh script

createdb house && psql house < a_horse_backup.sql && sleep 15 && psql house < cheirrs_backup.sql && sleep 15 && psql house < cheirrs_oseer_backup.sql && sleep 15 && psql house < chubba_morris_backup.sql && sleep 15 && psql house < chubba_morris_oseer_backup.sql && sleep 15 && psql house < convey_it_backup.sql && sleep 15 && psql house < convey_it_oseer_backup.sql && sleep 15 && psql house < the_general_backup.sql && sleep 15 && psql house < the_general_oseer_backup.sql
 
