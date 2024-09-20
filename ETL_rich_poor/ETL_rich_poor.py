import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


df=spark.read.format("csv").option("header",True).load("s3://5sep2024/details.csv")

df2=df.select(col("id"),col("salary"),when(col("salary")>500,"Rich").otherwise("poor"))

df2.write.format("csv").option("header",True).save("s3://sep09newbucket/17Sep24/")
df.show()
job.commit()