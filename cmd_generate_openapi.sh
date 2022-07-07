#!/bin/bash 
sudo docker run --rm -v "${PWD}:/local" \
openapitools/openapi-generator-cli generate \
-i /local/resources/schema.yaml \
-g python-flask \
-o /local/openapi/.
