

# Req:
DevOps Exam - Interview Task
Task: Kafka-Enabled HealthCheckService Deployment on Kubernetes

Scenario:
You are working for a company that is building a microservices architecture with Kafka as the
messaging backbone. The team is responsible for deploying and managing these services on a
Kubernetes cluster.

Task Requirements:
## done - Set up Local Kubernetes Cluster:
Install and set up a local Kubernetes cluster using a tool like Minikube. Ensure that kubectl is properly configured to
interact with the local cluster.

## done - Set up Kafka Cluster on Kubernetes:
Use Helm or Kubernetes manifests to deploy a Kafka cluster with at least 3 nodes within the Kubernetes
environment.

## done - Create a topic named health_checks_topic with appropriate configurations.
## done - Python HealthCheckService:
Write a Python service named HealthCheckService that periodically performs health checks on various
microservices in the system.
The service should have a REST API endpoint /check_health that retrieves the health status of different
microservices from the Kafka topic (health_checks_topic) and prints the results along with some text to the logs.
JSON Payload example:
{
"service_name": "MyService",
"status": "OK",
"timestamp": "2024-01-01T12:30:45Z"
}

ConsumerHealthCheckService:
Write another Python service named ConsumerHealthCheckService that consumes health check messages from
the health_checks_topic.
The service should have a REST API endpoint /get_latest_health_check that retrieves and prints the latest health
check results from the Kafka topic.

## done - Deployment Automation:
Create Kubernetes deployment manifests for both the HealthCheckService and ConsumerHealthCheckService.
Implement a rolling deployment strategy for these services.

## done - Use ConfigMaps/Secrets to manage any configuration that needs to be externalized. Ensure that the services can
scale horizontally.
## done partially - Monitoring and Logging
Set up monitoring for the Kafka cluster, HealthCheckService, and ConsumerHealthCheckService.
Implement logging for both services, including printing health check results along with some text.

Share a GitHub repository with the code and Kubernetes manifests.
Upload all code files, including Python scripts, deployment manifests, and any configuration files, to the
repository.
Include a directory or folder for screenshots or documentation images.
Provide a link to the repository, ensuring that it is set to public.

Good Luck!









# 1. Ubuntu Minikube (https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)


curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64

  sudo usermod -aG docker $USER
  newgrp docker

minikube start

minikube dashboard

minikube stop   ( pause / unpause )


# 2. Set up Kafka Cluster on Kubernetes:
Use Helm or Kubernetes manifests to deploy a Kafka cluster with at least 3 nodes within the Kubernetes
environment.
Create a topic named health_checks_topic with appropriate configurations.

## Install helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh    # rm get_helm.sh

## Install zookeeper
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

helm install zookeeper bitnami/zookeeper --set replicaCount=3
  NAME: zookeeper
  LAST DEPLOYED: Mon Jun  3 10:08:38 2024
  NAMESPACE: default
  STATUS: deployed
  REVISION: 1
  TEST SUITE: None
  NOTES:
  CHART NAME: zookeeper
  CHART VERSION: 13.4.0
  APP VERSION: 3.9.2
  ** Please be patient while the chart is being deployed **

  ZooKeeper can be accessed via port 2181 on the following DNS name from within your cluster:

      zookeeper.default.svc.cluster.local

  To connect to your ZooKeeper server run the following commands:

      export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=zookeeper,app.kubernetes.io/instance=zookeeper,app.kubernetes.io/component=zookeeper" -o jsonpath="{.items[0].metadata.name}")
      kubectl exec -it $POD_NAME -- zkCli.sh

  To connect to your ZooKeeper server from outside the cluster execute the following commands:

      kubectl port-forward --namespace default svc/zookeeper 2181:2181 &
      zkCli.sh 127.0.0.1:2181

  WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
    - resources
    - tls.resources
  +info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/


## Install kafka
helm install kafka bitnami/kafka --set replicaCount=3
  NAME: kafka
  LAST DEPLOYED: Mon Jun  3 10:18:15 2024
  NAMESPACE: default
  STATUS: deployed
  REVISION: 1
  TEST SUITE: None
  NOTES:
  CHART NAME: kafka
  CHART VERSION: 29.2.0
  APP VERSION: 3.7.0

  ** Please be patient while the chart is being deployed **

  Kafka can be accessed by consumers via port 9092 on the following DNS name from within your cluster:

      kafka.default.svc.cluster.local

  Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:

      kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092
      kafka-controller-1.kafka-controller-headless.default.svc.cluster.local:9092
      kafka-controller-2.kafka-controller-headless.default.svc.cluster.local:9092

  The CLIENT listener for Kafka client connections from within your cluster have been configured with the following security settings:
      - SASL authentication

  To connect a client to your Kafka, you need to create the 'client.properties' configuration files with the content below:

  security.protocol=SASL_PLAINTEXT
  sasl.mechanism=SCRAM-SHA-256
  sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
      username="user1" \
      password="$(kubectl get secret kafka-user-passwords --namespace default -o jsonpath='{.data.client-passwords}' | base64 -d | cut -d , -f 1)";

  To create a pod that you can use as a Kafka client run the following commands:

      kubectl run kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.7.0-debian-12-r6 --namespace default --command -- sleep infinity
      kubectl cp --namespace default /path/to/client.properties kafka-client:/tmp/client.properties
      kubectl exec --tty -i kafka-client --namespace default -- bash

      PRODUCER:
          kafka-console-producer.sh \
              --producer.config /tmp/client.properties \
              --broker-list kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-1.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-2.kafka-controller-headless.default.svc.cluster.local:9092 \
              --topic test

      CONSUMER:
          kafka-console-consumer.sh \
              --consumer.config /tmp/client.properties \
              --bootstrap-server kafka.default.svc.cluster.local:9092 \
              --topic test \
              --from-beginning

  WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
    - controller.resources
  +info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/


  ## Create a Kafka Topic

kubectl port-forward svc/kafka 9092:9092
kubectl exec -it $(kubectl get pods --selector=app.kubernetes.io/name=kafka -o jsonpath='{.items[0].metadata.name}') -- bash
kafka-topics.sh --create --topic health_checks_topic --bootstrap-server localhost:9092 --partitions=3 --replication-factor=3


### ISSUES: timeout error, 
    kafka-topics.sh --bootstrap-server kafka-controller-1.kafka-controller-headless.default.svc.cluster.local:9093 --list
    [2024-06-04 09:23:40,022] WARN [AdminClient clientId=adminclient-1] The remote node is not a BROKER that supports the METADATA api. (org.apache.kafka.clients.admin.internals.AdminMetadataManager)
    org.apache.kafka.common.errors.UnsupportedVersionException: The node does not support METADATA
    kafka-topics.sh --bootstrap-server kafka-controller-1.kafka-controller-headless.default.svc.cluster.local:9092 --list
    ..
    k logs kafka-controller-2
    ..
    [2024-06-04 08:40:22,801] INFO [NodeToControllerChannelManager id=2 name=registration] Node 0 disconnected. (org.apache.kafka.clients.NetworkClient)
    [2024-06-04 08:57:36,077] INFO [SocketServer listenerType=BROKER, nodeId=2] Failed authentication with /10.244.0.12 (channelId=10.244.0.14:9092-10.244.0.12:60642-0) (Unexpected Kafka r
    equest of type METADATA during SASL handshake.) (org.apache.kafka.common.network.Selector)

cata@think:~/all$ k get cm kafka-controller-configuration -o yaml    # edit..
apiVersion: v1
data:
  server.properties: |-
    # Listeners configuration
    listeners=CLIENT://:9092,INTERNAL://:9094,CONTROLLER://:9093
    advertised.listeners=CLIENT://advertised-address-placeholder:9092,INTERNAL://advertised-address-placeholder:9094
    listener.security.protocol.map=CLIENT:PLAINTEXT,INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT
    #listener.security.protocol.map=CLIENT:SASL_PLAINTEXT,INTERNAL:SASL_PLAINTEXT,CONTROLLER:SASL_PLAINTEXT
    
k rollout restart sts kafka-controller

k exec -it kafka-controller-2 -- bash
I have no name!@kafka-controller-2:/$ kafka-topics.sh --bootstrap-server localhost:9092 --list
health_checks_topic


    [2024-06-04 08:30:26,118] INFO KafkaConfig values: advertised.listeners = CLIENT://kafka-controller-2.kafka-controller-headless.default.svc.cluster.local:9092,INTERNAL://kafka-controller-2.kafka-controller-headless.default.svc.cluster.local:9094



# Testing, validation

update config_maps.yaml with kafka outputs(as above)
./build-deploy.sh

cata@think:~/all/prj/00demos/kafka-minikube$ k port-forward svc/health-check-service 8123:80
Forwarding from 127.0.0.1:8123 -> 5000
Forwarding from [::1]:8123 -> 5000
^Z
[2]+  Stopped                 kubectl port-forward svc/health-check-service 8123:80
cata@think:~/all/prj/00demos/kafka-minikube$ bg
[2]+ kubectl port-forward svc/health-check-service 8123:80 &
cata@think:~/all/prj/00demos/kafka-minikube$ curl localhost:8123/check_health
Handling connection for 8123
{"service_name":"MyService","status":"OK","timestamp":"2024-06-04T11:39:35.014965Z"}



cata@think:~/all$ k exec -it kafka-controller-2 -- bash
Defaulted container "kafka" out of: kafka, kafka-init (init)
I have no name!@kafka-controller-2:/$ kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic health_checks_topic --from-beginning
{"service_name": "MyService", "status": "OK", "timestamp": "2024-06-04T11:05:39.063762Z"}
{"service_name": "MyService", "status": "OK", "timestamp": "2024-06-04T11:06:39.205193Z"}
{"service_name": "MyService", "status": "OK", "timestamp": "2024-06-04T11:07:39.273099Z"}
{"service_name": "MyService", "status": "OK", "timestamp": "2024-06-04T11:08:39.341066Z"}
{"service_name": "MyService", "status": "OK", "timestamp": "2024-06-04T11:08:40.318927Z"}
{"service_name": "MyService", "status": "OK", "timestamp": "2024-06-04T11:09:39.410234Z"}
..



# Logging (tbd)

With propper resources and time I would set up the endpoint to recieve a fluentd configured sidecar, as bellow:

https://kubernetes.io/docs/concepts/cluster-administration/logging/#sidecar-container-with-logging-agent


# Monitoring setup
minikube addons enable metrics-server
(https://maxat-akbanov.com/prometheus-and-grafana-setup-in-minikube)

## Prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus
cata@think:~/all/prj/00demos/kafka-minikube$ helm install prometheus prometheus-community/prometheus
        NAME: prometheus
        LAST DEPLOYED: Tue Jun  4 23:41:23 2024
        NAMESPACE: default
        STATUS: deployed
        REVISION: 1
        TEST SUITE: None
        NOTES:
        The Prometheus server can be accessed via port 80 on the following DNS name from within your cluster:
        prometheus-server.default.svc.cluster.local

        Get the Prometheus server URL by running these commands in the same shell:
        export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/instance=prometheus" -o jsonpath="{.items[0].metadata.name}")
        kubectl --namespace default port-forward $POD_NAME 9090

        The Prometheus alertmanager can be accessed via port 9093 on the following DNS name from within your cluster:
        prometheus-alertmanager.default.svc.cluster.local

        Get the Alertmanager URL by running these commands in the same shell:
        export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=alertmanager,app.kubernetes.io/instance=prometheus" -o jsonpath="{.items[0].metadata.name}")
        kubectl --namespace default port-forward $POD_NAME 9093
        #################################################################################
        ######   WARNING: Pod Security Policy has been disabled by default since    #####
        ######            it deprecated after k8s 1.25+. use                        #####
        ######            (index .Values "prometheus-node-exporter" "rbac"          #####
        ###### .          "pspEnabled") with (index .Values                         #####
        ######            "prometheus-node-exporter" "rbac" "pspAnnotations")       #####
        ######            in case you still need it.                                #####
        #################################################################################

        The Prometheus PushGateway can be accessed via port 9091 on the following DNS name from within your cluster:
        prometheus-prometheus-pushgateway.default.svc.cluster.local

        Get the PushGateway URL by running these commands in the same shell:
        export POD_NAME=$(kubectl get pods --namespace default -l "app=prometheus-pushgateway,component=pushgateway" -o jsonpath="{.items[0].metadata.name}")
        kubectl --namespace default port-forward $POD_NAME 9091

kubectl expose service prometheus-server --type=NodePort --target-port=9090 --name=prometheus-server-np
kubectl get svc
minikube service prometheus-server-np --url
    http://192.168.49.2:30960

## grafana
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana
    NAME: grafana
    LAST DEPLOYED: Tue Jun  4 23:45:12 2024
    NAMESPACE: default
    STATUS: deployed
    REVISION: 1
    NOTES:
    1. Get your 'admin' user password by running:

    kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo


    2. The Grafana server can be accessed via port 80 on the following DNS name from within your cluster:

    grafana.default.svc.cluster.local

    Get the Grafana URL to visit by running these commands in the same shell:
        export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
        kubectl --namespace default port-forward $POD_NAME 3000

    3. Login with the password from step 1 and the username: admin
    #################################################################################
    ######   WARNING: Persistence is disabled!!! You will lose your data when   #####
    ######            the Grafana pod is terminated.                            #####
    #################################################################################
kubectl expose service grafana --type=NodePort --target-port=3000 --name=grafana-np
kubectl get svc
kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
minikube service grafana-np --url
manual : Add Prometheus data source (use prometheus-server:80 URL)


Code instrumentation:
    cata@think:~/all/prj/00demos/kafka-minikube$ k port-forward consumer-health-check-service-694d5dd949-mj777 8000:8000
    Forwarding from 127.0.0.1:8000 -> 8000
    Forwarding from [::1]:8000 -> 8000
    ^Z
    [3]+  Stopped                 kubectl port-forward consumer-health-check-service-694d5dd949-mj777 8000:8000
    cata@think:~/all/prj/00demos/kafka-minikube$ bg
    [3]+ kubectl port-forward consumer-health-check-service-694d5dd949-mj777 8000:8000 &
    cata@think:~/all/prj/00demos/kafka-minikube$ curl localhost:8000/metrics
    Handling connection for 8000
    # HELP python_gc_objects_collected_total Objects collected during gc
    # TYPE python_gc_objects_collected_total counter
    python_gc_objects_collected_total{generation="0"} 362.0
    python_gc_objects_collected_total{generation="1"} 0.0
    python_gc_objects_collected_total{generation="2"} 0.0
    # HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
    # TYPE python_gc_objects_uncollectable_total counter
    python_gc_objects_uncollectable_total{generation="0"} 0.0
    python_gc_objects_uncollectable_total{generation="1"} 0.0
    python_gc_objects_uncollectable_total{generation="2"} 0.0
    # HELP python_gc_collections_total Number of times this generation was collected
    # TYPE python_gc_collections_total counter
    python_gc_collections_total{generation="0"} 38.0
    python_gc_collections_total{generation="1"} 3.0
    python_gc_collections_total{generation="2"} 0.0
    # HELP python_info Python platform information
    # TYPE python_info gauge
    python_info{implementation="CPython",major="3",minor="8",patchlevel="19",version="3.8.19"} 1.0
    # HELP process_virtual_memory_bytes Virtual memory size in bytes.
    # TYPE process_virtual_memory_bytes gauge
    process_virtual_memory_bytes 1.7588224e+08
    # HELP process_resident_memory_bytes Resident memory size in bytes.
    # TYPE process_resident_memory_bytes gauge
    process_resident_memory_bytes 2.0660224e+07
    # HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
    # TYPE process_start_time_seconds gauge
    process_start_time_seconds 1.71756072733e+09
    # HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
    # TYPE process_cpu_seconds_total counter
    process_cpu_seconds_total 0.39
    # HELP process_open_fds Number of open file descriptors.
    # TYPE process_open_fds gauge
    process_open_fds 6.0
    # HELP process_max_fds Maximum number of open file descriptors.
    # TYPE process_max_fds gauge
    process_max_fds 1.048576e+06
    # HELP http_requests_total Total HTTP Requests
    # TYPE http_requests_total counter
    http_requests_total 1085.0
    # HELP http_requests_created Total HTTP Requests
    # TYPE http_requests_created gauge
    http_requests_created 1.7175607284747682e+09


Todo, couple of things to be further enhanced:
  - docs, to be more clear
  - grafana/prometheus metrics and dashboards
  - logging actual implementation
