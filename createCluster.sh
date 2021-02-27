roachprod create lin-test -c gce -n 3
roachprod stage lin-test release v20.2.4
roachprod start lin-test

### Create jump
roachprod create lin-jump -n 1 -c gce
roachprod stage lin-jump release v20.2.4


# ssh into jump host
# roachprod ssh lin-jump:1
