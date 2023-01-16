EXPOSE_PORT=8690 \
    CONTAINER_IMAGE=sheet-server \
    CONFIG_SET=prod \
    BUILD_IMAGE_TAG=latest \
    CONTAINER_NAME=sheet-server-$EXPOSE_PORT \
    docker-compose down --remove-orphans

EXPOSE_PORT=8690 \
    CONTAINER_IMAGE=sheet-server \
    CONFIG_SET=prod \
    BUILD_IMAGE_TAG=latest \
    CONTAINER_NAME=sheet-server-$EXPOSE_PORT \
    docker-compose build --force-rm

EXPOSE_PORT=8690 \
    CONTAINER_IMAGE=sheet-server \
    CONFIG_SET=prod \
    BUILD_IMAGE_TAG=latest \
    CONTAINER_NAME=sheet-server-$EXPOSE_PORT \
    docker-compose up -d 