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

-- test performance of different joins
select count(*) from fact INNER MERGE JOIN ref on fact.key = ref.key where fact.key = 1;
select count(*) from fact INNER LOOKUP JOIN ref on fact.key = ref.key where fact.key = 1;
select count(*) from fact INNER HASH JOIN ref on fact.key = ref.key where fact.key = 1;

-- which type of join does the optimizer select?
explain select count(*) from fact MERGE JOIN ref on fact.key = ref.key where fact.key = 1;
