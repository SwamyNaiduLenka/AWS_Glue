import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
###AmazonS3_node1719211067358 = glueContext.create_dynamic_frame.from_options(format_options={"multiline": False}, connection_type="s3", format="json", connection_options={"paths": ["s3://bucketfortesters/data-test/"], "recurse": True}, transformation_ctx="AmazonS3_node1719211067358")

# Script generated for node Amazon S3
###AmazonS3_node1719211111164 = glueContext.write_dynamic_frame.from_options(frame=AmazonS3_node1719211067358, connection_type="s3", format="json", connection_options={"path": "s3://bucketfortesters/data-test/", "partitionKeys": []}, transformation_ctx="AmazonS3_node1719211111164")

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Demo") \
        .master("local[3]") \
        .getOrCreate()

    flight_time_df1 = spark.read.json("s3://bucketfortesters/data-test/d1/")
    flight_time_df2 = spark.read.json("s3://bucketfortesters/data-test/d2/")

    # join_df = flight_time_df1.join(flight_time_df2.hint("broadcast"), "id", "inner")
    
    join_df = flight_time_df1.join(broadcast(flight_time_df2), "id", "inner") \
        .hint("COALESCE", 5)
    
    join_df.write.format("json").option("header", True).save("s3://bucketfortesters/data-test/output1/")

    join_df.show()
    print("Number of Output Partitions:" + str(join_df.rdd.getNumPartitions()))


job.commit()