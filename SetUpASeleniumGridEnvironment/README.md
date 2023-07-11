### Setting up Selenium-hub and Selenium-chrome-nodes

*Images Used*
[Selenium-hub](https://hub.docker.com/r/selenium/hub)
[Selenium-chrome-nodes](https://hub.docker.com/r/selenium/node-chrome)

If we know what selenium grid is then following the documentation right from docker-hub page is very easy.
I didn't know about selenium grid, but setting up it was very easy.

Run this command and you are ready to go. (Make sure docker is installed.)

`docker network create grid`

`docker run -d -p 4442-4444:4442-4444 --net grid --name selenium-hub selenium/hub:latest`

For Setting up selenium-chrome-node with selenium-hub
```
docker run -d --net grid -e SE_EVENT_BUS_HOST=selenium-hub \
    --shm-size="2g" \
    -e SE_EVENT_BUS_PUBLISH_PORT=4442 \
    -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 \
    selenium/node-chrome:latest
```

---

### Converting Above command to docker-compose

I refer to this [GitHub selenium account](https://github.com/SeleniumHQ/docker-selenium/blob/trunk/docker-compose-v2.yml) to make sure docker-compose is written correctly.

```yaml

version: '3'

services:
  selenium-hub:
    image: selenium/hub
    ports:
      - 4442-4444:4442-4444
    networks:
      grid-network:
        ipv4_address: 172.40.0.2

  selenium-chrome-node1:
    image: selenium/node-chrome
    depends_on:
      - selenium-hub
    shm_size: "2g"
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
    networks:
      - grid-network

  selenium-chrome-node2:
    image: selenium/node-chrome
    depends_on:
      - selenium-hub
    shm_size: "2g"
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
    networks:
      - grid-network

  selenium-chrome-node3:
    image: selenium/node-chrome
    depends_on:
      - selenium-hub
    shm_size: "2g"
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
    networks:
      - grid-network

  selenium-chrome-node4:
    image: selenium/node-chrome
    depends_on:
      - selenium-hub
    shm_size: "2g"
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
    networks:
      - grid-network

  selenium-chrome-node5:
    image: selenium/node-chrome
    depends_on:
      - selenium-hub
    shm_size: "2g"
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
    networks:
      - grid-network
  
  selenium-chrome-node6:
    image: selenium/node-chrome
    depends_on:
      - selenium-hub
    shm_size: "2g"
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
    networks:
      - grid-network

networks:
  grid-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.40.0.0/16

```

If we will add more code for selenium-chrome-nodes it will scale up our environment for web-scraping. Simply add more code and use `docker compose up` command.