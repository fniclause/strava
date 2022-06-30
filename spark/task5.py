
from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct


#task 5 store data into MongoDB

spark = SparkSession \
    .builder \
    .master("local[1]") \
    .appName("myApp2") \
    .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/prcp.hpcp") \
    .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/prcp.stncnt") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

df = spark.read.format("mongo").load()

df_station_counts = df2.groupBy('STATION_NAME').count()
df_station_counts.witre.format("mongo").mode("append").save()

df = spark.read.format("mongo").option("uri","mongodb://127.0.0.1/prcp.stncnt").load()
df.show(58,truncate=False)