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

##calculate young and old and calculate discounted Salary
##val df = Seq(("Alice", 25, 1500), ("Bob", 30, 2000), ("Charlie", 35, 3000)).toDF("name", "age", "salary")
##<18 --YOUNG AND REST ALL PEOPLE AS OLD
##SOMEONES SALRY <1000 * 200                 -----------------------2000 * 0.5
# Create data as a list of tuples
data = [("Alice", 25, 1500), ("Bob", 30, 2000), ("Charlie", 35, 3000)]

# Create DataFrame from the list of tuples
df = spark.createDataFrame(data, ["name", "age", "salary"])

# Apply transformation to categorize based on age
#df.withColumn("AgeStatus", when(col("age") > 18, "OLD").otherwise("YOUNG"))
df1 = df.withColumn("AgeStatus", when(col("age") > 18, "OLD").otherwise("YOUNG")) \
        .withColumn("DiscountedSalary", when(col("salary") < 1000, col("salary")*2.0) \
        .when(col("salary") > 2000, col("salary")*0.5) \
        .otherwise(col("salary")))


df1.show()
# Write transformed DataFrame to S3
df1.write.format("csv").option("header", True).save("s3://bucketfortesters/june24_2")
