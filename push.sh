docker build -t lallinger/batch . --build-arg HTTP_PROXY=$http_proxy --build-arg HTTPS_PROXY=$http_proxy
docker push lallinger/batch
oc project spark-operator
oc delete -f spark.yaml
oc create -f spark.yaml