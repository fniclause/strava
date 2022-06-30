from pyspark.sql import SparkSession

spark = SparkSession \
  .builder \
  .master("local[1]") \
  .appName("myApp") \
  .getOrCreate()

df = spark.read.csv("./health.csv", header=True)
df.printSchema()
df.show()


