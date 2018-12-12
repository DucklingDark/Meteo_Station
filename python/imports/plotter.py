import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Plotter():
    def __init__(self):
        plt.grid(linestyle = '-', alpha = 150)
        plt.xlabel = 'Datetime'
        #plt.style.use('presentation')
        print('Plotter created')

    def show_plotter(self, x, y, plotLabel = 'Plot',
                     yLabel = '.'):
        yMax = max(y)
        yMaxInd = y.index(yMax)

        yMin = min(y)
        yMinInd = y.index(yMin)

        sMin = 'Min value = ' + str(yMin) + '( ' + str(x[yMinInd]) + ' )'
        sMax = 'Max value = ' + str(yMax) + '( ' + str(x[yMaxInd]) + ' )'

        plt.plot([], [])
        plt.scatter(x, y, c = 'r', label = 'Values')
        plt.scatter(x[yMinInd], yMin, c = 'lime', label = sMin)
        plt.scatter(x[yMaxInd], yMax, c = 'yellow', label = sMax)

        plt.gcf().autofmt_xdate()
        myFmt = mdates.DateFormatter('%Y_%m_%d_%H:%M:%S.%f')
        plt.gca().xaxis.set_major_formatter(myFmt)
        plt.legend()
        plt.show()