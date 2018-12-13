import sys
import argparse

from pymongo import MongoClient
from datetime import datetime, date, timedelta

from imports.mongo import Mongo
from imports.configer import Configer
from imports.plotter import Plotter
from imports.args_parser import ArgsParser

def main(argv):
    iniPath         = '..\\configs\\config.ini'
    configer        = Configer(iniPath)
    plotter         = Plotter()
    mongo           = Mongo(configer.Settings.mongo.client, 
                            configer.Settings.mongo.db, 
                            configer.Settings.mongo.collection)
    date            = datetime.now().strftime("%Y_%m_%d")
    time            = datetime.now().strftime("%H:%M:%S")
    #reportFile      = 'reports\\' + date + '_' + time + '.report'
    UNIX_EPOCH      = '1970_01_01'
    y               = []
    x               = []
    ylabel          = ''
    plotlabel       = ''
    sensor          = '' 
    dateFrom        = UNIX_EPOCH
    dateTo          = date
    mode            = 'all'

    print()
    if (len(argv) >= 1):
        sensor, ylabel, plotlabel, mode = ArgsParser().parse_first_arg(argv[0])

    if (len(argv) >= 2):
        dateFrom, mode = ArgsParser().parse_second_arg(argv[1])

    if (len(argv) >= 3):
        dateTo, mode = ArgsParser().parse_third_arg(argv[2])
        '''
        if ('--to' in argv[2]):
            dateTo = argv[2].split(':')[1]
            mode = 'from_to'
        else: 
            print('---Incorrect third parameter---')
            dateTo = 'ERROR'
            mode = 'ERROR'
            '''

    print()
    print('--> MODE\t: ' + mode)
    print('--> SENSOR\t: ' + sensor)
    print('--> DATE FROM\t: ' + dateFrom)
    print('--> DATE TO\t: ' + dateTo)
    print()
    
    if (mode == 'all'):
        xxx = mongo.collection.find({'sensor': sensor})
    elif (mode == 'today' or 
          mode == 'date' or
          mode == 'yesterday'):
        xxx = mongo.collection.find({'sensor': sensor,
                                     'date': dateFrom})
    elif (mode == 'from_to'):
        xxx = mongo.collection.find({'sensor': sensor,
                                     'date': {'$gt': dateFrom, '$lt': dateTo}})

    if (mode == 'ERROR'):
        print('Error in query')
    else:
        for xx in xxx:
            y.append(float(xx['data']))

            date = xx['date']
            time = xx['time']
            dtime = date + '_' + time

            try:
                xdtime = datetime.strptime(dtime, '%Y_%m_%d_%H:%M:%S')
            except:
                xdtime = datetime.strptime(dtime, '%Y_%m_%d_%H:%M:%S.%f')
            
            x.append(xdtime)

        print('-->Data count\t: ' + str(len(x)))

        plotter.show_plotter(x, y, plotLabel = plotlabel, yLabel = ylabel)    

if (__name__ == '__main__'):
    main(sys.argv[1:])