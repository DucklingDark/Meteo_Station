from datetime import datetime, date, timedelta

class ArgsParser():
    def parse_first_arg(self, arg):
        sensor = ''
        y_label = ''
        plot_label = ''
        mode = 'all'

        if (arg == '-bmp_temp'):
            sensor = 'BMP Temperature '
            y_label = '°C'
            plot_label = 'Temperature (BMP180)'
        elif (arg == '-htu_temp'):
            sensor = 'HTU Temperature '
            y_label = '°C'
            plot_label = 'Temperature (HTU21D)'
        elif (arg == '-bmp_press'):
            sensor = 'BMP Pressure '
            y_label = 'mm Hg'
            plot_label = 'Pressure'
        elif (arg == '-htu_humi'):
            sensor = 'HTU Humiidity '
            y_label = '%'
            plot_label = 'Humidity'
        else: 
            print('---Incorrect first parameter---')
            sensor = 'ERROR'
            mode = 'ERROR'

        return sensor, y_label, plot_label, mode

    def parse_second_arg(self, arg):
        dateFrom        = ''
        mode            = ''
        date            = datetime.now().strftime("%Y_%m_%d")
        UNIX_EPOCH      = '1970_01_01'

        if (arg == '--all'):
            dateFrom = UNIX_EPOCH
            mode = 'all'
        elif (arg == '--today'):
            dateFrom = date
            mode = 'today'
        elif (arg == '--yesterday'):
            dateFrom = (datetime.today() - timedelta(1)).strftime("%Y_%m_%d")
            mode = 'yesterday'
        elif ('--from' in arg):
            dateFrom = arg.split(':')[1]
            mode = 'from_to'
        elif ('--date' in arg):
            dateFrom = arg.split(':')[1]
            mode = 'date'
        else: 
            print('---Incorrect second parameter---')
            dateFrom = 'ERROR'
            mode = 'ERROR'
        
        return dateFrom, mode

    def parse_third_arg(self, arg):
        dateTo  = ''
        date    = datetime.now().strftime("%Y_%m_%d")

        if ('--to' in arg):
            dateTo = arg.split(':')[1]
            mode = 'from_to'
        elif (arg == '--today'):
            deteTo = date
            mode = 'from_to'
        else: 
            print('---Incorrect third parameter---')
            dateTo = 'ERROR'
            mode = 'ERROR'
        
        return dateTo, mode