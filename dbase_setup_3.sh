psql haus -c 'CREATE EXTENSION postgis;' -c 'CREATE EXTENSION postgis_raster;' -c 'CREATE EXTENSION postgis_topology;' -c 'CREATE EXTENSION postgis_sfcgal;' -c 'CREATE EXTENSION fuzzystrmatch;' -c 'CREATE EXTENSION address_standardizer;' -c 'CREATE EXTENSION address_standardizer_data_us;' -c 'CREATE EXTENSION postgis_tiger_geocoder;' -c '\i /home/ubuntu/create_users.sql'