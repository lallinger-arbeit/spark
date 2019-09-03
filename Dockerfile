 # Use the official Python image.
# https://hub.docker.com/_/python
FROM gcr.io/spark-operator/spark-py:v2.4.0

# Copy local code to the container image.
ENV APP_HOME /extract_transform
WORKDIR $APP_HOME
COPY . .

# Install production dependencies.
RUN apk add gcc
RUN pip install --upgrade pip
RUN pip install Flask gunicorn azure-storage-blob

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 batch:app