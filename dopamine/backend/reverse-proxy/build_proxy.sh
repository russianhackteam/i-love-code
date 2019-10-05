#!/bin/bash

export $(cat .env | xargs)

image_name="$PROXY_CONTAINER"
container_name="$PROXY_CONTAINER"

if [[ -n "$image_name" ]]; then
	docker build -f proxy_dockerfile -t $image_name . && docker run --name $container_name -d -p 8800:80 $image_name
fi
