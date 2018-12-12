from pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from datetime import datetime, date, timedelta

from imports.plotter import Plotter

import time
import sys

def main(argv):
    start_time = int(round(time.time() * 1000))
    plotter    = Plotter()

    y = []
    x = []

    uri_conf = 'mongodb://localhost:27017/meteo_station.outside'
    spark = SparkSession \
                .builder \
                .appName("Meteo_Station") \
                .config("spark.mongodb.input.uri", uri_conf) \
                .config("spark.executor.memory", "2g") \
                .config("spark.executor.number", "4") \
                .config("spark.executor.cores", "4") \
                .config("spark.network.timeout", "600s") \
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

    plotter.show_plotter(x, y, plotLabel = '', yLabel = '')
    #press_data = pressure.select('data').collect()
    #data_array = [float(i.data) for i in pressure.collect()]

    #press_time = pressure.select('time').collect()
    #time_array = [i.time for i in pressure.collect()]

    #press_date = pressure.select('date').collect()
    #date_array = [i.date for i in pressure.collect()]
    #print(len(coll))

    end_time = int(round(time.time() * 1000))
    total = end_time - start_time
    print(total)

if (__name__ == '__main__'):
    main(sys.argv[1:])