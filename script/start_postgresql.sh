#!/bin/sh

sudo docker run -d \
	--name postgres \
	--log-opt max-size=10m \
	-e POSTGRES_PASSWORD=postgres \
	-v /usr/share/zoneinfo/Asia/Taipei:/etc/localtime:ro \
	-v ~/docker/volumes/postgres/data:/var/lib/postgresql/data \
	-p 5432:5432 \
	postgres:15.5