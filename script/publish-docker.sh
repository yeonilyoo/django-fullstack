# !/bin/bash
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
COMPOSE_FILE="$SCRIPT_DIR/../docker/docker-compose.yml"

# docker compose -f "$COMPOSE_FILE" up -d --build
docker tag my-test-image:latest yourusername/my-test-image:latest
docker push yourusername/my-test-image:latest
