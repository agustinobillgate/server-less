
## Dengan pgadmin:
1.hapus schema qcserverless2
2.create schema qcserverless2
3.query tools,load & run tables-pk_qcserverless2_collate.sql

## Connect SSH: 
restore: 
1. cd /usr1 (dimana db file berada)
2. psql -U postgres -h psql.staging.e1-vhp.com -d qctest -v ON_ERROR_STOP=1 -c "SET search_path TO qcserverless2;" -f ./qcserverless2_load_tables_pk_20250714.sql

## Create Dump file:
pg_dump -U postgres -h psql.staging.e1-vhp.com -d qctest -F c --schema=qcserverless2 -f "./dump-ec2-db-qctest-qcserverless2.dump"

pg_dump -U postgres -h psql.staging.e1-vhp.com -d qctest -F c --schema=qcserverless3 -f "./dump-ec2-db-qctest-qcserverless3.dump"