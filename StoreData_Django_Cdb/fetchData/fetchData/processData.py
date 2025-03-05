import os

#os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.datastax.spark:spark-cassandra-connector_2.12:3.5.0 pyspark-shell'

from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType


def fetchRecords():
    

    #READS WITH CASSANDRA ARE VERYY INEFFICIENT, THEY TAKE A LOT OF TIME, MEMORY, CPU AND CASSANDRA CONTAINER KEEPS SHUTTING DOWN
    # 

    # spark = SparkSession.builder \
    #     .appName("CassandraSparkIntegration") \
    #     .master("spark://sparkapp:7077") \
    #     .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.5.0") \
    #     .config("spark.cassandra.connection.host", "cassdb") \
    #     .config("spark.cassandra.connection.port", "9042") \
    #     .config("spark.cassandra.auth.username", "admin") \
    #     .config("spark.cassandra.auth.password", "admin") \
    #     .config("spark.executor.memory", "512m") \
    #     .config("spark.driver.memory", "512m") \
    #     .config("spark.executor.cores", "1") \
    #     .getOrCreate()

    # df = spark.read.format('org.apache.spark.sql.cassandra') \
    #     .options(table='pm25', keyspace='aqdata') \
    #     .load()

    # df.show()

    #SO SHIFTED TO READING IT FROM CSV FILE 

     
    spark = SparkSession.builder.appName("RecordsFetch").getOrCreate()

    df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("data.csv")



    df = df.withColumn("avg_pm25", df["avg_pm25"].cast(DoubleType()))
    df = df.withColumn("max_pm25", df["max_pm25"].cast(DoubleType()))
    df = df.withColumn("min_pm25", df["min_pm25"].cast(DoubleType()))

    avg_pm25 = df.groupBy("location").avg("avg_pm25")
    max_pm25= df.groupBy("location").max("max_pm25")
    min_pm25= df.groupBy("location").min("min_pm25")
    print("avg_pm25")
    avg_pm25.show()
    print("max_pm25")
    max_pm25.show()
    print("min_pm25")
    min_pm25.show()
    df = df.drop("location")  
    data = df.toPandas().to_dict(orient="records")

    return data
 




'''

/* PS D:\MajorProject\fullstackProject> docker exec -it  280ba4f3f1fd bash
I have no name!@1e496dac3573:/opt/bitnami/spark$ spark-shell
//mount local folder on docker spark container
docker run -d --name nameofcontainer -v localfolder:containerpath imagename 
docker run -d --name sparkapp -v "D:/MajorProject/fullstackProject:/mnt/docs" bitnami/spark master
 
 :load is for scala, to run in spark-shell

 python scripts run in linux terminal
python /mnt/docs/processData_Spark_Cdb/processData.py

//connect sparkapp, cassdb to ntw
 docker network connect aqinet sparkapp
docker network connect aqinet cassdb

//check if conn is successful
PS D:\MajorProject\fullstackProject> docker exec -it sparkapp python3 -c "import socket; s = socket.socket(); print(s.connect_ex(('cassdb', 9042)))"
0 #conn is successful :)
 docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
NAMES      STATUS          PORTS
sparkapp   Up 10 minutes

PS D:\MajorProject\fullstackProject> docker exec -it sparkapp sh

$ getent hosts cassdb
172.22.0.3      cassdb




OUTPUTTTTTT:
PS D:\MajorProject\fullstackProject> docker exec -it sparkapp bash                    
I have no name!@280ba4f3f1fd:/opt/bitnami/spark$ python /mnt/docs/processData_Spark_Cdb/processData.py
  
:: loading settings :: url = jar:file:/opt/bitnami/spark/jars/ivy-2.5.1.jar!/org/apache/ivy/core/settings/ivysettings.xml
Ivy Default Cache set to: /opt/bitnami/spark/.ivy2/cache
The jars for the packages stored in: /opt/bitnami/spark/.ivy2/jars
com.datastax.spark#spark-cassandra-connector_2.12 added as a dependency
:: resolving dependencies :: org.apache.spark#spark-submit-parent-cbf19b8a-9d14-4413-9b7c-c0412820dd0c;1.0
        
:: resolution report :: resolve 856ms :: artifacts dl 16ms
        
        ---------------------------------------------------------------------
        |                  |            modules            ||   artifacts   |
        |       conf       | number| search|dwnlded|evicted|| number|dwnlded|
        ---------------------------------------------------------------------
        |      default     |   19  |   0   |   0   |   0   ||   19  |   0   |
        ---------------------------------------------------------------------
:: retrieving :: org.apache.spark#spark-submit-parent-cbf19b8a-9d14-4413-9b7c-c0412820dd0c
        confs: [default]
        0 artifacts copied, 19 already retrieved (0kB/18ms)
25/03/03 08:35:20 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
+----------+--------+--------------------+--------+--------+
|      date|avg_pm25|            location|max_pm25|min_pm25|
+----------+--------+--------------------+--------+--------+
|2025-03-06|      89|Hyderabad US Cons...|      95|      68|
|2025-03-07|     111|Hyderabad US Cons...|     138|      89|
+----------+--------+--------------------+--------+--------+
only showing top 2 rows

I have no name!@280ba4f3f1fd:/opt/bitnami/spark$ 


+----------+--------+--------------------+--------+--------+
|      date|avg_pm25|            location|max_pm25|min_pm25|
+----------+--------+--------------------+--------+--------+
|2025-03-06|      89|Hyderabad US Cons...|      95|      68|
|2025-03-07|     111|Hyderabad US Cons...|     138|      89|
|2025-03-04|     123|Hyderabad US Cons...|     159|      89|
|2025-03-03|     138|Hyderabad US Cons...|     138|     138|
|2025-03-05|     115|Hyderabad US Cons...|     138|      89|
|2025-03-01|     138|Hyderabad US Cons...|     138|     132|
|2025-02-28|     139|Hyderabad US Cons...|     158|     138|
|2025-03-08|     131|Hyderabad US Cons...|     138|      89|
|2025-03-02|     138|Hyderabad US Cons...|     138|     138|
+----------+--------+--------------------+--------+--------+


avg_pm25
+--------------------+------------------+
|            location|     avg(avg_pm25)|
+--------------------+------------------+
|Hyderabad US Cons...|124.66666666666667|
+--------------------+------------------+

max_pm25
+--------------------+-------------+
|            location|max(max_pm25)|
+--------------------+-------------+
|Hyderabad US Cons...|          159|
+--------------------+-------------+

min_pm25
+--------------------+-------------+
|            location|min(min_pm25)|
+--------------------+-------------+
|Hyderabad US Cons...|           68|
+--------------------+-------------+


PS D:\MajorProject\fullstackProject> docker exec -it cassdb cqlsh -u admin -p admin

Warning: Using a password on the command line interface can be insecure.
Recommendation: use the credentials file to securely provide the password.

Connected to My Cluster at 127.0.0.1:9042
[cqlsh 6.2.0 | Cassandra 5.0.3 | CQL spec 3.4.7 | Native protocol v5]
Use HELP for help.
admin@cqlsh> describe keyspaces

aqdata  system_auth         system_schema  system_views
system  system_distributed  system_traces  system_virtual_schema

admin@cqlsh> use aqdata
   ... ;
admin@cqlsh:aqdata> select * from pm25;

 date       | avg_pm25 | location                                                     | max_pm25 | min_pm25
------------+----------+--------------------------------------------------------------+----------+----------
 2025-03-04 |      124 | Hyderabad US Consulate, India (हैदराबाद अमेरिकी वाणिज्य दूतावास) |      138 |       89
 2025-03-10 |       89 | Hyderabad US Consulate, India (हैदराबाद अमेरिकी वाणिज्य दूतावास) |       89 |       89
 2025-03-07 |       96 | Hyderabad US Consulate, India (हैदराबाद अमेरिकी वाणिज्य दूतावास) |      122 |       68
 2025-03-05 |      118 | Hyderabad US Consulate, India (हैदराबाद अमेरिकी वाणिज्य दूतावास) |      138 |       89     
 2025-03-08 |      115 | Hyderabad US Consulate, India (हैदराबाद अमेरिकी वाणिज्य दूतावास) |      138 |       89     
 2025-03-03 |      138 | Hyderabad US Consulate, India (हैदराबाद अमेरिकी वाणिज्य दूतावास) |      138 |      138     
 2025-03-09 |      114 | Hyderabad US Consulate, India (हैदराबाद अमेरिकी वाणिज्य दूतावास) |      138 |       89     
 2025-03-06 |       87 | Hyderabad US Consulate, India (हैदराबाद अमेरिकी वाणिज्य दूतावास) |       89 |       68     
 2025-03-02 |      138 | Hyderabad US Consulate, India (हैदराबाद अमेरिकी वाणिज्य दूतावास) |      138 |      138     

(9 rows)

To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
2025-03-04 17:48:52 
[Stage 0:>                                                          (0 + 0) / 1]

[Stage 0:>                                                          (0 + 1) / 1]

                                                                                

[Stage 1:>                                                          (0 + 4) / 4]

[Stage 1:==============>                                            (1 + 3) / 4]

[Stage 1:=============================>                             (2 + 2) / 4]

[Stage 1:============================================>              (3 + 1) / 4]

                                                                                

[Stage 2:>                                                          (0 + 7) / 7]

[Stage 2:========>                                                  (1 + 6) / 7]

[Stage 2:================>                                          (2 + 5) / 7]

[Stage 2:=========================>                                 (3 + 4) / 7]

[Stage 2:=================================>                         (4 + 3) / 7]

[Stage 2:==========================================>                (5 + 2) / 7]

[Stage 2:==================================================>        (6 + 1) / 7]

                                                                                

[Stage 3:>                                                        (0 + 12) / 27]

[Stage 3:==>                                                      (1 + 12) / 27]

[Stage 3:====>                                                    (2 + 12) / 27]

[Stage 3:========>                                                (4 + 12) / 27]

[Stage 3:==========>                                              (5 + 12) / 27]

[Stage 3:============>                                            (6 + 12) / 27]

[Stage 3:==============>                                          (7 + 12) / 27]

[Stage 3:================>                                        (8 + 12) / 27]

[Stage 3:===================>                                     (9 + 12) / 27]

[Stage 3:======================>                                 (11 + 12) / 27]

[Stage 3:======================>                                 (11 + 13) / 27]

[Stage 3:==========================>                             (13 + 12) / 27]

[Stage 3:=============================>                          (14 + 12) / 27]

[Stage 3:===============================>                        (15 + 12) / 27]

[Stage 3:========================================>                (19 + 8) / 27]

[Stage 3:==========================================>              (20 + 7) / 27]

[Stage 3:============================================>            (21 + 6) / 27]

[Stage 3:==============================================>          (22 + 5) / 27]

[Stage 3:================================================>        (23 + 4) / 27]

[Stage 3:==================================================>      (24 + 3) / 27]

[Stage 3:====================================================>    (25 + 2) / 27]

[Stage 3:======================================================>  (26 + 1) / 27]

[Stage 3:=========================================================(27 + 0) / 27]

[Stage 5:>                                                          (0 + 1) / 1]

                                                                                

[Stage 6:>                                                        (0 + 12) / 27]

[Stage 6:==>                                                      (1 + 12) / 27]

[Stage 6:====>                                                    (2 + 12) / 27]

[Stage 6:======>                                                  (3 + 12) / 27]

[Stage 6:========>                                                (4 + 12) / 27]

[Stage 6:==========>                                              (5 + 12) / 27]

[Stage 6:============>                                            (6 + 12) / 27]

[Stage 6:==============>                                          (7 + 12) / 27]

[Stage 6:================>                                        (8 + 12) / 27]

[Stage 6:===================>                                     (9 + 12) / 27]

[Stage 6:======================>                                 (11 + 12) / 27]

[Stage 6:========================>                               (12 + 12) / 27]

[Stage 6:=============================>                          (14 + 12) / 27]

[Stage 6:===============================>                        (15 + 12) / 27]

[Stage 6:===================================>                    (17 + 10) / 27]

[Stage 6:======================================>                  (18 + 9) / 27]

[Stage 6:========================================>                (19 + 8) / 27]

[Stage 6:==========================================>              (20 + 7) / 27]

[Stage 6:============================================>            (21 + 6) / 27]

[Stage 6:================================================>        (23 + 4) / 27]

[Stage 6:====================================================>    (25 + 2) / 27]

[Stage 6:======================================================>  (26 + 1) / 27]

[Stage 8:>                                                          (0 + 1) / 1]

                                                                                

[Stage 9:>                                                        (0 + 12) / 27]

[Stage 9:==>                                                      (1 + 12) / 27]

[Stage 9:====>                                                    (2 + 12) / 27]

[Stage 9:======>                                                  (3 + 12) / 27]

[Stage 9:========>                                                (4 + 12) / 27]

[Stage 9:==========>                                              (5 + 12) / 27]

[Stage 9:============>                                            (6 + 12) / 27]

[Stage 9:==============>                                          (7 + 12) / 27]

[Stage 9:================>                                        (8 + 12) / 27]

[Stage 9:====================>                                   (10 + 12) / 27]

[Stage 9:========================>                               (12 + 12) / 27]

[Stage 9:=============================>                          (14 + 12) / 27]

[Stage 9:===================================>                    (17 + 10) / 27]

[Stage 9:======================================>                  (18 + 9) / 27]

[Stage 9:========================================>                (19 + 8) / 27]

[Stage 9:==========================================>              (20 + 7) / 27]

[Stage 9:============================================>            (21 + 6) / 27]

[Stage 9:==============================================>          (22 + 5) / 27]

[Stage 9:================================================>        (23 + 4) / 27]

[Stage 9:======================================================>  (26 + 1) / 27]

[Stage 11:>                                                         (0 + 1) / 1]

                                                                                

[Stage 12:>                                                       (0 + 12) / 27]

[Stage 12:==>                                                     (1 + 12) / 27]

[Stage 12:==========>                                             (5 + 12) / 27]

[Stage 12:============>                                           (6 + 12) / 27]

[Stage 12:======================>                                (11 + 12) / 27]

[Stage 12:==========================>                            (13 + 12) / 27]

[Stage 12:============================>                          (14 + 12) / 27]

[Stage 12:==============================>                        (15 + 12) / 27]

[Stage 12:================================>                      (16 + 11) / 27]

[Stage 12:==================================>                    (17 + 10) / 27]

[Stage 12:=====================================>                  (18 + 9) / 27]

[Stage 12:=========================================>              (20 + 7) / 27]

[Stage 12:===========================================>            (21 + 6) / 27]

[Stage 12:=============================================>          (22 + 5) / 27]

[Stage 12:===============================================>        (23 + 4) / 27]

[Stage 12:=================================================>      (24 + 3) / 27]

[Stage 12:===================================================>    (25 + 2) / 27]

[Stage 12:=====================================================>  (26 + 1) / 27]


5 max_pm25
2025-03-04 23:26:55 +--------------------+-------------+
2025-03-04 23:26:55 |            location|max(max_pm25)|
2025-03-04 23:26:55 +--------------------+-------------+
2025-03-04 23:26:55 |Hyderabad US Cons...|        138.0|
2025-03-04 23:26:55 +--------------------+-------------+
2025-03-04 23:26:55 
2025-03-04 23:26:55 min_pm25
2025-03-04 23:26:55 +--------------------+-------------+
2025-03-04 23:26:55 |            location|min(min_pm25)|
2025-03-04 23:26:55 +--------------------+-------------+
2025-03-04 23:26:55 |Hyderabad US Cons...|         68.0|
2025-03-04 23:26:55 +--------------------+-------------+
2025-03-04 23:26:55 
2025-03-04 23:26:55 avg_pm25
2025-03-04 23:26:55 +--------------------+------------------+
2025-03-04 23:26:55 |            location|     avg(avg_pm25)|
2025-03-04 23:26:55 +--------------------+------------------+
2025-03-04 23:26:55 |Hyderabad US Cons...|113.22222222222223|
2025-03-04 23:26:55 +--------------------+------------------+
2025-03-04 23:26:55 
2025-03-04 23:26:55 max_pm25
2025-03-04 23:26:55 +--------------------+-------------+
2025-03-04 23:26:55 |            location|max(max_pm25)|
2025-03-04 23:26:55 +--------------------+-------------+
2025-03-04 23:26:55 |Hyderabad US Cons...|        138.0|
2025-03-04 23:26:55 +--------------------+-------------+
2025-03-04 23:26:55 
2025-03-04 23:26:55 min_pm25
2025-03-04 23:26:55 +--------------------+-------------+
2025-03-04 23:26:55 |            location|min(min_pm25)|
2025-03-04 23:26:55 +--------------------+-------------+
2025-03-04 23:26:55 |Hyderabad US Cons...|         68.0|
2025-03-04 23:26:55 +--------------------+-------------+
 '''


 #docker run -d --name cassdb --network aqiapp-net -p 9042:9042 bitnami/cassandra:latest

    