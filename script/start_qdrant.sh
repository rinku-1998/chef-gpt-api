#!/bin/bash

docker run -d \
        --name qdrant \
        --log-opt max-size=50m  \
        -p 6333:6333 -p 6334:6334 \
        -v ~/docker_volume//qdrant/:/qdrant/storage \
        qdrant/qdrant