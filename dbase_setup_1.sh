#!/bin/bash

# dbase_setup_1.sh script

createuser gmu && createdb haus && psql haus < a_horse_backup.sql && sleep 5 && psql haus < cheirrs_backup.sql && sleep 5 && psql haus < cheirrs_oseer_backup.sql && sleep 5 && psql haus < chubba_morris_backup.sql && sleep 5 && psql haus < chubba_morris_oseer_backup.sql && sleep 5 && psql haus < convey_it_backup.sql && sleep 5 && psql haus < convey_it_oseer_backup.sql && sleep 5 && psql haus < iot_backup.sql && sleep 5 && psql haus < the_general_backup.sql && sleep 5 && psql haus < the_general_oseer_backup.sql && exit
