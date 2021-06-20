create role cheirrs_user with login password 'passwd';

create role cheirrs_admin with superuser login password 'passwd';

create role cheirrs_oseer_admin with superuser login password 'passwd';

create role a_horse_admin with superuser login password 'passwd';

create role chubba_morris_user with login password 'passwd';

create role chubba_morris_admin with superuser login password 'passwd';

create role chubba_morris_oseer_admin with superuser login password 'passwd';

create role convey_it_user with login password 'passwd';

create role convey_it_admin with superuser login password 'passwd';

create role convey_it_oseer_admin with superuser login password 'passwd';

create role the_general_user with login password 'passwd';

create role the_general_admin with superuser login password 'passwd';

create role the_general_oseer_admin with superuser login password 'passwd';

create role gmu with login password 'gmu';

GRANT USAGE ON SCHEMA a_horse TO 'gmu';

GRANT USAGE ON SCHEMA cheirrs TO 'gmu';

GRANT USAGE ON SCHEMA cheirrs_oseer TO 'gmu';

GRANT USAGE ON SCHEMA chubba_morris_oseer TO 'gmu';

GRANT USAGE ON SCHEMA chubba_morris TO 'gmu';

GRANT USAGE ON SCHEMA convey_it_oseer TO 'gmu';

GRANT USAGE ON SCHEMA convey_it TO 'gmu';

GRANT USAGE ON SCHEMA the_general_oseer TO 'gmu';

GRANT USAGE ON SCHEMA the_general TO 'gmu';

GRANT USAGE ON SCHEMA topology TO 'gmu';

GRANT USAGE ON SCHEMA public TO 'gmu';

ALTER ROLE gmu SET search_path TO public, a_horse, cheirrs, cheirrs_oseer, chubba_morris, chubba_morris_oseer, convey_it, convey_it_oseer, the_general, the_general_oseer, topology;
