#!/bin/sh

docker -H 0.0.0.0:2375 run \
	--name=neterraproxy \
	--rm \
	--volume=<local_neterra_folder>:/usr/local/lib/neterraproxy \
	--publish=8081:8080 \
	--env=DATADIR=/usr/local/lib/neterraproxy \
	--env=USER=<neterra_username> \
	--env=PASSWORD=<neterra_password> \
