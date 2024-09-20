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

df = spark.read.format("csv").option("header", True).load("s3://crawlerbucketdataa/info.csv")



# Write transformed DataFrame to S3
df.write.format("csv").option("header", True).save("s3://crawlerbucketdataa/june456Data/")

job.commit()