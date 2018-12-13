using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using MongoDB.Bson;
using MongoDB.Driver;
using System.Windows.Threading;

namespace real_time_sharp {
    public partial class MainWindow : Window {
        private Mongo mongo = new Mongo();
        private DispatcherTimer timer;
        private SensorData sens;
        private int state;

        public MainWindow() {
            InitializeComponent();

            state = 0;

            timer = new DispatcherTimer();
            timer.Tick += new EventHandler(timer_tick);
            timer.Interval = new TimeSpan(250);

            mongo.connect(host: "mongodb://localhost:27017",
                          db: "meteo_station",
                          collect: "outside");

            timer.Start();
        }

        private void btn_Exit_Click(object sender, RoutedEventArgs e) {
            this.Close();
        }

        private void Window_MouseLeftButtonDown(object sender, MouseButtonEventArgs e) {
            base.OnMouseLeftButtonDown(e);
            this.DragMove();
        }

        private void timer_tick(object sender, EventArgs e) {
            switch (state) {
                case 0:
                    sens = mongo.read_sensor("HTU Temperature ");
                    lb_temp.Content = sens.data;
                    state++;
                    break;
                case 1:
                    sens = mongo.read_sensor("HTU Humiidity ");
                    lb_humi.Content = sens.data;
                    state++;
                    break;
                case 2:
                    sens = mongo.read_sensor("BMP Pressure ");
                    lb_atmo.Content = sens.data;
                    state = 0;
                    break;
            }
        }
    }
}
