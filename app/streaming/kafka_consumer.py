from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("FraudTransactionConsumer")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:29092")
    .option("subscribe", "fraud.public.transactions")
    .option("startingOffsets", "earliest")
    .load()
)

transactions = kafka_df.selectExpr(
    "CAST(key AS STRING) AS key",
    "CAST(value AS STRING) AS value",
    "timestamp"
)

query = (
    transactions.writeStream
    .format("console")
    .option("truncate", "false")
    .outputMode("append")
    .start()
)

query.awaitTermination()