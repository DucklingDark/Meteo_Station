using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using MongoDB.Bson;
using MongoDB.Driver;

using IniParser;
using IniParser.Model;

namespace real_time_sharp {
    public class SensorData {
        public ObjectId _id { get; set; }
        public string sensor { get; set; }
        public string data { get; set; }
        public string date { get; set; }
        public string time { get; set; }
    }

    class Mongo {
        private FileIniDataParser parser;

        public void connect(string ini_Path) {
            parser = new FileIniDataParser();
            IniData data = parser.ReadFile("..\\..\\..\\python\\configs\\");
        }

        //public SensorData read_sensor(string sensor) {

        //}

        public void disconnect() {

        }
    }
}
