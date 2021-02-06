roachprod create lin-test -c gce -n 4

lin-test: [gce] 12h25m6s remaining
  lin-test-0001	lin-test-0001.us-east1-b.cockroach-ephemeral	10.142.0.9	104.196.170.19
  lin-test-0002	lin-test-0002.us-east1-b.cockroach-ephemeral	10.142.0.6	34.74.232.186
  lin-test-0003	lin-test-0003.us-east1-b.cockroach-ephemeral	10.142.0.15	35.196.199.8
  lin-test-0004	lin-test-0004.us-east1-b.cockroach-ephemeral	10.142.0.11	35.243.216.201

roachprod stage lin-test release v20.2.4

roachprod start lin-test

roachprod sql lin-test:1
