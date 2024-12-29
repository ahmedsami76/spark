from __future__ import print_function
import sys
from pyspark.sql import SparkSession

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: mnmcount <input_file> <output_dir>", file=sys.stderr)
        sys.exit(-1)

    # Initialize SparkSession
    spark = (SparkSession
             .builder
             .appName("PythonMnMCount")
             .getOrCreate())

    # Get input and output paths from command line
    mnm_file = sys.argv[1]
    output_dir = sys.argv[2]

    # Read the file into a Spark DataFrame
    mnm_df = (spark.read.format("csv")
              .option("header", "true")
              .option("inferSchema", "true")
              .load(mnm_file))

    # Show initial data
    mnm_df.show(n=5, truncate=False)

    # Aggregate count of all colors and group by state and color
    count_mnm_df = (mnm_df.select("State", "Color", "Count")
                    .groupBy("State", "Color")
                    .sum("Count")
                    .orderBy("sum(Count)", ascending=False))

    # Show results and write to HDFS
    count_mnm_df.show(n=60, truncate=False)
    count_mnm_df.write.mode("overwrite").csv(f"{output_dir}/all_states_counts")

    print("Total Rows = %d" % (count_mnm_df.count()))

    # Find the aggregate count for California
    ca_count_mnm_df = (mnm_df.select("*")
                       .where(mnm_df.State == 'CA')
                       .groupBy("State", "Color")
                       .sum("Count")
                       .orderBy("sum(Count)", ascending=False))

    # Show results and write to HDFS
    ca_count_mnm_df.show(n=10, truncate=False)
    ca_count_mnm_df.write.mode("overwrite").csv(f"{output_dir}/ca_state_counts")

    spark.stop()