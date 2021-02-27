
# install pip and psycopg2
sudo apt-get update
sudo apt-get install -y python-pip

# now use pip to install psycopg2 to be usedin small batch programs
pip install psycopg2-binary

python upsertSmallBatches.py 'postgresql://root@35.231.31.13:26257/defaultdb?sslmode=disable'

#python insertSmallBatches.py 'postgresql://root@35.231.31.13:26257/defaultdb?sslmode=disable'

cd /mnt/data1/
~/cockroach debug pebble lsm MANIFEST-000001 > lsm.html
