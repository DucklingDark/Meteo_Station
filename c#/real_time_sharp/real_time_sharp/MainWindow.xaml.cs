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

namespace real_time_sharp {
    public partial class MainWindow : Window {
        public MainWindow() {
            InitializeComponent();
            string[] args = Environment.GetCommandLineArgs();
            string connectionString = "mongodb://localhost:27017";
            var client = new MongoClient(connectionString);
            var database = client.GetDatabase("meteo_station");
            var collection = database.GetCollection<SensorData>("outside");
            var filter = Builders<SensorData>.Filter.Eq("sensor", "BMP Pressure ");

            var result = collection
                        .Find(filter)
                        .Limit(1)
                        .Sort(Builders<SensorData>.Sort.Descending(x => x._id))
                        .ToList();

            foreach (var rs in result) {

            }
        }

        private void btn_Exit_Click(object sender, RoutedEventArgs e) {
            this.Close();
        }

        private void Window_MouseLeftButtonDown(object sender, MouseButtonEventArgs e) {
            base.OnMouseLeftButtonDown(e);
            this.DragMove();
        }
    }
}
