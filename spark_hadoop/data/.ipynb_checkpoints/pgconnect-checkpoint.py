from pyspark.sql import SparkSession

jdbc_driver_path = "/data/postgresql-42.7.4.jar"

spark = SparkSession.builder.appName("PG") \
        .config("spark.jars", "/data/postgresql-42.7.4.jar") \
        .getOrCreate()

jdbc1 = (spark
         .read
         .format("jdbc")
         .option("url", "jdbc:postgresql://pg-db/dvdrental")
         .option("dbtable", "[public].[film]")
         .option("user", "postgres")
         .option("password", "P@ssw0rd")
         .load())