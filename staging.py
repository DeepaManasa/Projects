# Databricks notebook source
application_id="38ef420a-2ea5-4336-9ebe-71ed745351fd"
directory_id="f3e00db4-0a83-491b-bce4-7ba2fa1212ea"
service_credential = dbutils.secrets.get('projectscope','service-credential')

spark.conf.set("fs.azure.account.auth.type.projectstorage997.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.projectstorage997.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.projectstorage997.dfs.core.windows.net", application_id)
spark.conf.set("fs.azure.account.oauth2.client.secret.projectstorage997.dfs.core.windows.net", service_credential)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.projectstorage997.dfs.core.windows.net", f"https://login.microsoftonline.com/{directory_id}/oauth2/token")

# COMMAND ----------

display(dbutils.fs.ls("abfss://curated@projectstorage997.dfs.core.windows.net/curated_renamed"))

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import *

sales_schema = StructType([
    StructField("TransactionID",StringType(), True),
    StructField("CustomerName",StringType(), True),
    StructField("Product", StringType(), True),
    StructField("Quantity",DoubleType(), True),
    StructField("Region", StringType(), True),
    StructField("UnitPrice", DoubleType(), True),
    StructField("TransactionDate", DateType(), True)
])

df = spark.read.csv(
    "abfss://curated@projectstorage997.dfs.core.windows.net/curated_renamed/curated_sales_data.csv",
    header=True,
    schema=sales_schema
)
df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import expr, year,col

# Clean Price Per Unit and derive Total Amount
df = df.withColumn("TotalAmount", col("Quantity") * col("UnitPrice"))

# Add Transaction Year
df = df.withColumn("TransactionYear", year(col("TransactionDate")))

#df.write.format("csv").mode("overwrite").option("header", "true").save("abfss://staging@projectstorage997.dfs.core.windows.net/staging_sales_data.csv")
display(df)

# COMMAND ----------

df.write.mode("overwrite").partitionBy("Product").parquet("abfss://staging@projectstorage997.dfs.core.windows.net/staging_sales_data.parquet")
display(df)
