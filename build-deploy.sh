eval $(minikube docker-env)

pushd health_check_service
docker build -t local-registry/health-check-service:latest -f Dockerfile .
# docker push local-registry/health-check-service:latest
popd

pushd consumer_health_check_service/
docker build -t local-registry/consumer-health-check-service:latest -f Dockerfile .
# docker push local-registry/consumer-health-check-service:latest
popd

pushd prometheus/
docker build -t local-registry/prometheus:latest -f Dockerfile .
popd


pushd k8s
OP=delete
OP=apply  # comment for cleaning up

kubectl $OP -f config_maps.yaml
kubectl $OP -f health_check_service_deployment.yaml
kubectl $OP -f consumer_health_check_service_deployment.yaml
popd


kubectl rollout restart deploy/consumer-health-check-service
kubectl rollout restart deploy/health-check-service
