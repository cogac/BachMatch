from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StringType, TimestampType, IntegerType
# for environment variables
import os

windowDuration = '10 seconds'
slidingDuration = '10 seconds'

# Create a Spark Session
spark = SparkSession.builder \
    .config('spark.jars', 'spark-connector-assembly-1.3.2.jar')\
    .appName("BachMatch") \
    .getOrCreate()

# spark logging level
spark.sparkContext.setLogLevel('WARN')
# Define the schema for the Kafka messages
schema = (
    StructType()
    .add("topic", StringType())
    .add("title", StringType())
    .add("abstract", StringType())
    .add("timestamp", IntegerType())
)

# Read the Kafka topic as a streaming DataFrame
kafka_stream = spark \
    .readStream.format("kafka") \
    .option("kafka.bootstrap.servers", 'bachmatch-kafka-bootstrap:9092') \
    .option("subscribe", "bachmatch") \
    .option("startingOffsets", "latest") \
    .load()

# get the correct format for the dataframe
user_abstract_df = kafka_stream.select(
    from_json(
        column("value").cast("string"),
        schema
    ).alias("json")
).select(
    from_unixtime(column('json.timestamp'))
    .cast(TimestampType())
    .alias("parsed_timestamp"),
    column("json.*")
) \
    .withColumnRenamed('json.title', 'title') \
    .withColumnRenamed('json.topic', 'topic') \
    .withColumnRenamed('json.abstract', 'abstract')\
    .withWatermark("parsed_timestamp", windowDuration)


weav_options = {
    "host": os.environ['WEAVSERVERHOST'],
    "className": "UserAbstract",
}
# only dataframes can be written to weaviate, no streaming dataframes -- but we don't need any aggregation
abstract_batch = user_abstract_df.groupBy(
    column("topic"),
    column("title"),
    column("abstract")
).count() \
 .select(column('topic'), column('title'), column('abstract'))\

# write the batch to
consoleDump = abstract_batch\
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

# function to write batches to weaviate to


def saveToDatabase(batchDF, batchId):
    print(f"Writing batchID {batchId} to database ")
    batchDF.distinct().write\
        .format("io.weaviate.spark.Weaviate")\
        .option("batchSize", 10)\
        .option("scheme", "http")\
        .option("host", weav_options['host'])\
        .option("className", weav_options['className'])\
        .mode("append")
    print('Written to database')


# theoretically write the data to weaviate (it does not get there though)
dbInsertStream = abstract_batch\
    .writeStream \
    .outputMode("complete") \
    .foreachBatch(saveToDatabase) \
    .start()

# wait until spark wants pyspark to stop
spark.streams.awaitAnyTermination()
