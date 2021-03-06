﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using MongoDB.Bson;
using MongoDB.Driver;

namespace real_time_sharp {
    public class SensorData {
        public ObjectId _id { get; set; }
        public string sensor { get; set; }
        public string data { get; set; }
        public string date { get; set; }
        public string time { get; set; }
    }

    class Mongo {
        private MongoClient client;
        private IMongoDatabase database;
        private IMongoCollection<SensorData> collection;

        public Mongo() {
        }

        public void connect(string host, string db, string collect) {
            client = new MongoClient(host);
            database = client.GetDatabase(db);
            collection = database.GetCollection<SensorData>(collect);
        }

        public SensorData read_sensor(string sensor) {
            var filter = Builders<SensorData>.Filter.Eq("sensor", sensor);

            var result = collection
                        .Find(filter)
                        .Limit(1)
                        .Sort(Builders<SensorData>.Sort.Descending(x => x._id))
                        .ToList();

            result[0].data = result[0].data.Replace('.', ',');
            return result[0];
        }
    }
}
