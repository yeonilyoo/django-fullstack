#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
K8S_DIR="${SCRIPT_DIR}/../k8s"
K8S_DEFAULT_DIR="${SCRIPT_DIR}/../k8s-default"
NGINX_DIR="${SCRIPT_DIR}/../docker/nginx"

SECRETS_FILE="${K8S_DIR}/02_secrets.yaml"

# Optional: read MySQL passwords interactively
# read -sp "Enter MySQL root password: " ROOT_PASS; echo
# read -sp "Enter MySQL user password: " USER_PASS; echo
# sed -i "s/MYSQL_ROOT_PASSWORD: .*/MYSQL_ROOT_PASSWORD: \"$ROOT_PASS\"/" "$SECRETS_FILE"
# sed -i "s/MYSQL_PASSWORD: .*/MYSQL_PASSWORD: \"$USER_PASS\"/" "$SECRETS_FILE"

kubectl apply -f "${K8S_DEFAULT_DIR}/pv.yaml"

# Apply namespace and secrets
kubectl apply -f "${K8S_DIR}/01_namespace.yaml"
kubectl apply -f "$SECRETS_FILE"

# Apply volumes and database
kubectl apply -f "${K8S_DIR}/03_volumes.yaml"
kubectl apply -f "${K8S_DIR}/04_db-deployment.yaml"

# Wait for DB pod to be ready
echo "Waiting for DB pod to be ready..."
kubectl wait --for=condition=ready pod -l app=myweb-db -n myweb --timeout=120s

# Apply web deployment
kubectl apply -f "${K8S_DIR}/05_web-deployment.yaml"

# Wait for web pod to be ready
echo "Waiting for Web pod to be ready..."
kubectl wait --for=condition=ready pod -l app=myweb-app -n myweb --timeout=180s

# ConfigMap and Secret for Nginx
# kubectl create configmap myweb-nginx-config \
#   --from-file="${NGINX_DIR}/default.conf" \
#   -n myweb --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f "${K8S_DIR}/06_nginx-configmap.yaml"

# kubectl create secret generic myweb-ssl \
#   --from-file="${NGINX_DIR}/selfsigned.crt" \
#   --from-file="${NGINX_DIR}/selfsigned.key" \
#   -n myweb --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f "${K8S_DIR}/06_nginx-secret.yaml"

# Apply Nginx deployment
kubectl apply -f "${K8S_DIR}/07_nginx-deployment.yaml"

# Optional: Wait for Nginx to be ready
echo "Waiting for Nginx pod to be ready..."
kubectl wait --for=condition=ready pod -l app=myweb-nginx -n myweb --timeout=120s

kubectl apply -f "${K8S_DIR}/08_ingress.yaml"

echo "Deployment complete!"
