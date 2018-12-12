import configparser
import os

class Configer():
    class Settings:
        class mongo:
            client      = ''
            db          = ''
            collection  = ''
        
        class socket:
            ip          = ''
            port        = ''

    def __init__(self, path = ''):
        self.path = path

        if (self.path != ''):
            self.load_config()

    def create_config(self):
        config = configparser.ConfigParser()

        config.add_section('Mongo_settings')
        config.set('Mongo_settings', 'client', 'mongodb://localhost:27017/')
        config.set('Mongo_settings', 'db','meteo_station')
        config.set('Mongo_settings', 'collection', 'outside')

        config.add_section('Socket_settings')
        config.set('Socket_settings', 'ip', '192.168.1.128')
        config.set('Socket_settings', 'port', '90')

        with open(self.path, 'w') as config_file:
            config.write(config_file)

    def load_config(self):
        if not (os.path.exists(self.path)):
            self.create_config()
        
        config = configparser.ConfigParser()
        config.read(self.path)

        self.Settings.mongo.client      = config.get('Mongo_settings', 'client')
        self.Settings.mongo.db          = config.get('Mongo_settings', 'db')
        self.Settings.mongo.collection  = config.get('Mongo_settings', 'collection') 
        self.Settings.socket.ip         = config.get('Socket_settings', 'ip')
        self.Settings.socket.port       = config.get('Socket_settings', 'port')

        print('Config loaded')