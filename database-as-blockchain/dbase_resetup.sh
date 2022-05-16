 #!/bin/bash

# dbase_resetup.sh script

createuser gmu && createdb haus && psql haus < das_fuhrwerk_backup.sql && sleep 2 && psql haus < member_class_0_backup.sql && sleep 2 && psql haus < member_class_0_oseer_backup.sql && sleep 2 && psql haus < member_class_1_backup.sql && sleep 2 && psql haus < member_class_1_oseer_backup.sql && sleep 2 && psql haus < member_class_2_backup.sql && sleep 2 && psql haus < member_class_2_oseer_backup.sql && sleep 2 && psql haus < iot_backup.sql && sleep 2 && psql haus < member_class_3_backup.sql && sleep 2 && psql haus < member_class_3_oseer_backup.sql
