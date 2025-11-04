#!/bin/bash
set -e

# === Resolve paths ===
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
PROJECT_ROOT="$SCRIPT_DIR/.."
DOCKERFILE_PATH="$PROJECT_ROOT/docker/Dockerfile"

# === Config ===
IMAGE_NAME="django-web"
VERSION=${1:-latest}

# === Auto-detect Docker Hub username ===
detect_docker_user() {
  local user
  # Try standard method first
  user=$(docker info --format '{{.Username}}' 2>/dev/null || true)

  # If that fails, try from config.json
  if [ -z "$user" ] && [ -f "$HOME/.docker/config.json" ]; then
    user=$(grep -o '"auths":{[^}]*}' "$HOME/.docker/config.json" | grep -o '"https://index.docker.io/v1/":{' || true)
    if [ -n "$user" ]; then
      user=$(grep -o '"credsStore"[^,}]*' "$HOME/.docker/config.json" | cut -d'"' -f4 || true)
    fi
  fi

  # Still empty? Try with environment variable or ask user
  if [ -z "$user" ]; then
    read -rp "🧑‍💻 Enter your Docker Hub username: " user
  fi

  echo "$user"
}

DOCKER_USER=$(detect_docker_user)
if [ -z "$DOCKER_USER" ]; then
  echo "❌ Unable to determine Docker Hub username."
  echo "   Please check 'docker login' or specify it manually."
  exit 1
fi

LOCAL_TAG="${IMAGE_NAME}:${VERSION}"
REMOTE_TAG="${DOCKER_USER}/${IMAGE_NAME}:${VERSION}"
REMOTE_LATEST="${DOCKER_USER}/${IMAGE_NAME}:latest"

echo "📁 Project root: $PROJECT_ROOT"
echo "🐳 Dockerfile: $DOCKERFILE_PATH"
echo "👤 Docker Hub user: $DOCKER_USER"
echo "🏷️  Tags to publish:"
echo "   - $REMOTE_TAG"
echo "   - $REMOTE_LATEST"
echo

# === Build ===
echo "🔨 Building Docker image..."
docker build -f "$DOCKERFILE_PATH" -t "$LOCAL_TAG" "$PROJECT_ROOT"

# === Tag ===
echo "🏷️  Tagging image..."
docker tag "$LOCAL_TAG" "$REMOTE_TAG"
docker tag "$LOCAL_TAG" "$REMOTE_LATEST"

# === Push ===
echo "🚀 Pushing to Docker Hub..."
docker push "$REMOTE_TAG"
docker push "$REMOTE_LATEST"

echo
echo "✅ Published successfully!"
echo "   - $REMOTE_TAG"
echo "   - $REMOTE_LATEST"
echo "🎉 Done!"
