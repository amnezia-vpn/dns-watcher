### Build an image

docker build . -t dns-watcher

### Run a container

docker run --rm --env DOMAINS_LIST_PATH=/app/domains.yaml --env DNS_SERVER=1.1.1.1 --env RESOLUTION_PROTOCOL=UDP --volume ./domains.yaml:/app/domains.yaml dns-watcher
