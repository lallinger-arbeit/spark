#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Add dependencies as needed then place this file in /PathToSpark/kubernetes/dockerfiles/spark/bindings/python rename existing Dockerfile.
# cd into /PathToSpark and run ./bin/docker-image-tool.sh -t latest -b HTTP_PROXY=$http_proxy -b HTTPS_PROXY=$http_proxy build
# docker tag spark-py:latest dockerNamespace/spark-py:latest
# docker push dockerNamespace/spark-py:latest

ARG base_img
FROM $base_img
WORKDIR /
RUN mkdir ${SPARK_HOME}/python
# TODO: Investigate running both pip and pip3 via virtualenvs
RUN apk add --no-cache python && \
    apk add --no-cache python3 && \
	apk add --no-cache python2-dev && \
	apk add --no-cache python3-dev && \
	apk add --no-cache gcc libc-dev libffi-dev openssl-dev && \
    python -m ensurepip && \
    python3 -m ensurepip && \
    # We remove ensurepip since it adds no functionality since pip is
    # installed on the image and it just takes up 1.6MB on the image
    rm -r /usr/lib/python*/ensurepip && \
    pip install --upgrade pip setuptools && \
	pip install azure-storage && \
    # You may install with python3 packages by using pip3.6
    # Removed the .cache to save space
    rm -r /root/.cache

COPY python/lib ${SPARK_HOME}/python/lib
ENV PYTHONPATH ${SPARK_HOME}/python/lib/pyspark.zip:${SPARK_HOME}/python/lib/py4j-*.zip

WORKDIR /opt/spark/work-dir
ENTRYPOINT [ "/opt/entrypoint.sh" ]
