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
using System.Windows.Shapes;
using OxyPlot;
using OxyPlot.Series;

namespace real_time_sharp {
    /// <summary>
    /// Interaction logic for Plotter.xaml
    /// </summary>
    public partial class Plotter : Window {
        private LineSeries series_temp;
        private LineSeries series_humi;
        private LineSeries series_press;
        private int count_t;
        private int count_h;
        private int count_p;

        public Plotter() {
            InitializeComponent();
            series_temp = new LineSeries();
            series_humi = new LineSeries();
            series_press = new LineSeries();

            plot_temp.Model = new PlotModel();
            plot_humi.Model = new PlotModel();
            plot_press.Model = new PlotModel();

            plot_temp.Model.TextColor = OxyColors.DarkRed;
            plot_humi.Model.TextColor = OxyColors.DarkMagenta;
            plot_press.Model.TextColor = OxyColors.DarkCyan;

            plot_temp.Model.DefaultColors = new List<OxyColor>{
                OxyColors.Red
            };

            plot_humi.Model.DefaultColors = new List<OxyColor>{
                OxyColors.Magenta
            };

            plot_press.Model.DefaultColors = new List<OxyColor>{
                OxyColors.Cyan
            };

            plot_temp.Model.Series.Add(series_temp);
            plot_humi.Model.Series.Add(series_humi);
            plot_press.Model.Series.Add(series_press);

            count_h = 0;
            count_t = 0;
            count_p = 0;
        }

        private void Window_MouseLeftButtonDown(object sender, MouseButtonEventArgs e) {
            base.OnMouseLeftButtonDown(e);
            this.DragMove();
        }

        private void btn_Exit_Click(object sender, RoutedEventArgs e) {
            this.Close();
        }

        public void RefreshPlot(int sens, double data) {
            switch (sens) {
                case 0:
                    series_temp.Points.Add(new DataPoint(count_t, data));
                    count_t++;
                    plot_temp.InvalidatePlot(true);
                    break;
                case 1:
                    series_humi.Points.Add(new DataPoint(count_h, data));
                    count_h++;
                    plot_humi.InvalidatePlot(true);
                    break;
                case 2:
                    series_press.Points.Add(new DataPoint(count_p, data));
                    count_p++;
                    plot_press.InvalidatePlot(true);
                    break;
            }
        }
    }
}
