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

import sys,os,time
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

    print("\nList blobs in the container")
    generator = block_blob_service.list_blobs(containerStaging)
    for blob in generator:
        print("\t Blob name: " + blob.name)
        blobs.append(blob.name)


    partitions = 4
    n = 100000 * partitions

    def getCount(blob):
        filepath = os.path.join("~/tmp", blob)
        block_blob_service.get_blob_to_path(containerStaging, blob, filepath)

        dataframe = spark.read.csv(filepath, mode="DROPMALFORMED",schema="name,count,meta")
        print(dataframe.select("count").collect())

        return dataframe.select("count").collect()

    def sumup(a,b):
        return a+b


    sum = spark.sparkContext.parallelize(blobs, partitions).map(getCount).reduce(sumup)
    print("Sum is: " % sum)

    spark.stop()
