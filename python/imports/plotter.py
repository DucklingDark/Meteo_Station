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

        sValues = plotLabel + ' in ' + yLabel

        yMin = min(y)
        yMinInd = y.index(yMin)

        sMin = 'Min value = ' + str(yMin) + ' ' + yLabel + ' ( ' + str(x[yMinInd]) + ' )'
        sMax = 'Max value = ' + str(yMax) + ' ' + yLabel + ' ( ' + str(x[yMaxInd]) + ' )'

        avg = sum(y) / float(len(y))
        xAvg = [x[0], x[len(x)-1]]
        yAvg = [avg, avg]

        sAvg = 'Average value = ' + str('{0:.2f}'.format(avg)) + ' ' + yLabel

        plt.plot([], [])
        plt.scatter(x, y, c = 'r', label = sValues)
        plt.scatter(x[yMinInd], yMin, c = 'lime', label = sMin)
        plt.scatter(x[yMaxInd], yMax, c = 'yellow', label = sMax)
        plt.plot(xAvg, yAvg, c = 'magenta', label = sAvg)

        plt.gcf().autofmt_xdate()
        myFmt = mdates.DateFormatter('%Y_%m_%d_%H:%M:%S.%f')
        plt.gca().xaxis.set_major_formatter(myFmt)
        plt.legend()
        plt.show()