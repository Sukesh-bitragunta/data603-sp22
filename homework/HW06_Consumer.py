import time

import matplotlib.pyplot as plt
from pyspark.sql import SparkSession

Sukesh = (SparkSession
         .builder
         .appName("issStreamer")
         .getOrCreate()
        )

lines = (
	Sukesh.readStream
	.format("socket")
	.option("host", "localhost")
	.option("port", 22225)
	.load()
)

df_S = lines.selectExpr("CAST(value AS STRING) AS payload")

writer = (
	df_S.writeStream
	.queryName('iss')
	.format('memory')
	.outputMode('append')
)

streamer = writer.start()

for i in range(5):
	df_ALL = spark.sql("select * from iss")
	df_ALL.show()
	df = spark.sql("""
SELECT
	get_json_object(payload, '$.iss_position.latitude') AS latitude,
	get_json_object(payload, '$.iss_position.longitude') AS longitude
FROM iss
""").toPandas()

	print(df)
	time.sleep(5)

streamer.awaitTermination(timeout=30)
print('streaming done')
df.plot.line(x='latitude', y='longitude')
plt.show()



