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

##StartsWith and EndsWith  Methods
data = [("Alice", 25, 1500), ("Bob", 30, 2000), ("Charlie", 35, 3000)]

# Create DataFrame from the list of tuples
df = spark.createDataFrame(data, ["name", "age", "salary"])


transformedDF = df.select(col("name"), col("age"), \
                when((col("age") > 30) & (col("name").startswith("C")), "Senior") \
                .when((col("age") > 20) & (col("name").startswith("B")), "Mid-Level") \
                .otherwise("Junior").alias("position")
)


transformedDF.show()

job.commit()