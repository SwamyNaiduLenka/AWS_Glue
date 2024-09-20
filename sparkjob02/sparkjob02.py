import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

df = spark.read.format("csv").option("header",True).load("s3://bucketfortesters/info.csv")

# Apply transformation to categorize based on age
df1 = df.withColumn("Pensionable", when(col("Age") > 55, "SENIOR").otherwise("JUNIOR"))

# Write transformed DataFrame to S3
df1.write.format("csv").option("header", True).save("s3://bucketfortesters/june24")
