#!/bin/bash

export $(cat .env | xargs)

container_name="$PROXY_CONTAINER"

if [[ -n "$container_name" ]]; then
	docker rm -f $container_name
fi
