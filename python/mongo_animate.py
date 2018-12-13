import sys
import pymongo
import numpy                as np
import matplotlib.pyplot    as plt
import matplotlib.dates     as mdates

from pymongo                import MongoClient
from datetime               import datetime, date, timedelta
from imports.mongo          import Mongo
from imports.configer       import Configer
from imports.args_parser    import ArgsParser
from matplotlib.animation   import FuncAnimation

def main(argv):
    sensor      = ''
    ylabel      = ''
    plotlabel   = ''
    x           = []
    y           = []

    if (len(argv) >= 1):
        sensor, ylabel, plotlabel, mode = ArgsParser().parse_first_arg(argv[0])
        sValues = plotlabel + ' in ' + ylabel

    def init():
        line.set_data([], [])
        return line,
    
    def update(i):
        last = mongo.collection.find_one({'sensor': sensor},sort = [('_id', pymongo.DESCENDING)])        
        dat = float(last['data'])
        print('New data: ' + str(dat))
        x.append(i)
        y.append(dat)
        plt.ylim(y[0] - .2, y[0] + .2)
        plt.xlim(0, i)
        line.set_data(x, y)
        return line,

    iniPath         = '..\\configs\\config.ini'
    configer        = Configer(iniPath)
    mongo           = Mongo(configer.Settings.mongo.client, 
                            configer.Settings.mongo.db, 
                            configer.Settings.mongo.collection)

    fig     = plt.figure(num = 1)

    ax      = plt.axes()
    ax.set_title(plotlabel)

    line,   = ax.plot([], [], lw=2, c = 'r', label = sValues)
    ani     = FuncAnimation(fig, update, init_func = init,
                            interval = 200, blit = True, frames = 100000)

    plt.xticks([])
    plt.grid(linestyle = '-', alpha = 150)
    plt.legend()

    plt.show()

if (__name__ == '__main__'):
    main(sys.argv[1:])