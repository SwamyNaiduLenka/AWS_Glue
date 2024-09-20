import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from datetime import date

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

database = "sb5demodatabase"
table = "sb5demo2024"
# dynamicFrame = glueContext.getCatalogSource(database=database, tableName=table).getDynamicFrame()

dynamicFrame = glueContext.create_dynamic_frame.from_catalog(
   database = database,
   table_name = table) 

df = dynamicFrame.toDF()

# Get today's date in formatted string
today = date.today().strftime('%Y%m%d')

# Build the S3 path with formatted date
s3_path = f"s3://crawlerbucketdataa/{today}/"

# Save the dataframe to S3
df.write.format("csv").option("header", "true").save(s3_path)

# Write transformed DataFrame to S3
#df.write.format("csv").option("header", "true").save("s3://crawlerbucketdataa/$today/")

job.commit()
