-- create table
-- Is int a good data type for key? What's PK?
create table ref ( key int, value float, index (key));
create table fact ( key int, value float, index (key));

-- Insert test dataset
-- 1M rows in fact table, and 1B rows in ref table
upsert into fact select generate_series(1,1000000), random();
-- For each rows in fact table, it generates 1000 rows
-- We comment the sql below because it mostly likely won't finish successfully and may even crash the cluster
--upsert into ref select key, random() from fact, generate_series(1,1000);


--import
--set cluster settings
set cluster setting sql.stats.automatic_collection.enabled=false;
import into ref(key, value) csv data ('gs://lin-bucket--acl/ref1.csv', 'gs://lin-bucket--acl/ref2.csv', 'gs://lin-bucket--acl/ref3.csv');
--create stats after import
create statistics initial_stats from ref;


drop table ref;
-- import without secondary index
create table ref ( key int, value float);
import into ref (key, value) csv data ('gs://lin-bucket--acl/ref1.csv', 'gs://lin-bucket--acl/ref2.csv', 'gs://lin-bucket--acl/ref3.csv');
create statistics initial_stats from ref;
create index ref_idx on ref (key);

--change schema
drop table ref;
create table ref ( newkey UUID primary key default gen_random_uuid(), key int, value float, index(key));
import into ref (key, value) csv data ('gs://lin-bucket--acl/ref.csv');
import into ref(key, value) csv data ('gs://lin-bucket--acl/ref1.csv', 'gs://lin-bucket--acl/ref2.csv', 'gs://lin-bucket--acl/ref3.csv');


--backup
backup table defaultdb.ref to 'gs://lin-bucket--acl/backup';
--restore
restore defaultdb.ref from 'gs://lin-bucket--acl/backup';
show statistics for table ref;


-- test performance of different joins
select count(*) from fact INNER MERGE JOIN ref on fact.key = ref.key where fact.key = 1;
select count(*) from fact INNER LOOKUP JOIN ref on fact.key = ref.key where fact.key = 1;
select count(*) from fact INNER HASH JOIN ref on fact.key = ref.key where fact.key = 1;

-- which type of join does the optimizer select?
explain select count(*) from fact MERGE JOIN ref on fact.key = ref.key where fact.key = 1;
