import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
##read all the csv files in the aws buckets recursively 

df = spark.read.format("csv").option("header", "true").option("path", "s3://22sep2024/").load()

##write all the data partioned to the aws buckets 

##df.write.format("csv").option("header", "true").option("partitionBy", "City").option("path", "s3://gluepl2209/output/").save()

df.write.format("csv").option("header", "true").partitionBy("City").mode("overwrite").save("s3://gluepl2209/output/")

job.commit()
