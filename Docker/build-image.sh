#!/bin/sh

docker -H 0.0.0.0:2375 build --no-cache -t neterraproxy .
