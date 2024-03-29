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

from __future__ import print_function

import sys,os,time,uuid
from random import random
from operator import add

from pyspark.sql import SparkSession
from pyspark import SparkContext
from azure.storage.blob import BlockBlobService, PublicAccess

if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    spark = SparkSession\
        .builder\
        .appName("PythonPi")\
        .getOrCreate()

    
    user=os.environ['STORAGE_USERNAME']
    password=os.environ['STORAGE_PASSWORD']
    containerStaging = "staging"
    containerAnalytics = "analytics"
    
    block_blob_service = BlockBlobService(account_name=user, account_key=password)

    blobs = []

    generator = block_blob_service.list_blobs(containerStaging)
    for blob in generator:
        blobs.append(blob.name)

    if len(blobs)==0:
        print("No blobs in staging, shutting down")
        spark.stop()
        quit()

    partitions = 4
    n = 100000 * partitions

    def getCount(blobName):
        print(blobName)
        blob = block_blob_service.get_blob_to_text(containerStaging,blobName)
        print(blob.content)
        
        ret=int(blob.content.split(",")[1])

        block_blob_service.delete_blob(containerStaging,blobName,delete_snapshots='include')

        return ret

    sum = spark.sparkContext.parallelize(blobs, partitions).map(getCount).reduce(add)
    
    block_blob_service.create_blob_from_text(containerAnalytics,"sum"+str(uuid.uuid4())+".csv",str(sum))
    
    print("Sum is: " + str(sum))

    spark.stop()
