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

###Question 1: Finding the count of orders placed by each customer and the total order amount for each customer.
orderData = [
            ("Order1", "John", 100),
            ("Order2", "Alice", 200),
            ("Order3", "Bob", 150),
            ("Order4", "Alice", 300),
            ("Order5", "Bob", 250),
            ("Order6", "John", 400)]

# Create DataFrame from the list of tuples
df = spark.createDataFrame(orderData, ["OrderID", "Customer", "Amount"])

transformedDF = df.groupBy(col("Customer")) \
  .agg(count(col("OrderID")).alias("Orders_Count"),  # Count orders with alias
    sum(col("Amount")).alias("total_order_amount"))  # Sum amount with alias

transformedDF.show()


job.commit()