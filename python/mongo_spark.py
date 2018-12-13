from pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from datetime import datetime, date, timedelta

from imports.plotter import Plotter

import time
import sys

def main(argv):
    plotter    = Plotter()

    y = []
    x = []

    uri_conf = 'mongodb://localhost:27017/meteo_station.outside'
    spark = SparkSession \
                .builder \
                .appName("Meteo_Station") \
                .config("spark.mongodb.input.uri", uri_conf) \
                .config("spark.executor.memory", "4g") \
                .config("spark.executor.number", "4") \
                .config("spark.executor.cores", "4") \
                .config("spark.network.timeout", "800s") \
                .config('spark.yarn.executor.memoryOverhead', "4096m") \
                .config("spark.driver.memoryOverhead",) \
                .getOrCreate()

    df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    df.registerTempTable('temp')
    pressure = spark.sql('SELECT * FROM temp WHERE sensor = \'BMP Pressure \' ')
    coll = pressure.collect()

    for c in coll:
        y.append(float(c['data']))

        date = c['date']
        xtime = c['time']
        dtime = date + '_' + xtime

        try:
            xdtime = datetime.strptime(dtime, '%Y_%m_%d_%H:%M:%S')
        except:
            xdtime = datetime.strptime(dtime, '%Y_%m_%d_%H:%M:%S.%f')
        
        x.append(xdtime)

    print('-->Data count\t: ' + str(len(x)))

    plotter.show_plotter(x, y, plotLabel = 'Pressure (BMP180)', yLabel = 'mm Hg')

if (__name__ == '__main__'):
    main(sys.argv[1:])