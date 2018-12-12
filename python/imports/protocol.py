from imports.mongo import Mongo
from datetime import datetime
import logging

class Protocol():
	class Commands():
		client_ready 	= 'OK'

	class Bytes():
		first_byte  	= '$'
		end_byte		= '\n'

	class RxMessages():
		BMP_TEMPERATURE	= 2
		HTU_TEMPERATURE	= 3
		PRESSURE 		= 4
		HUMIDITY 		= 5

	def __init__(self, mongo):
		self.mongo 	= mongo

	def prepare_command(self, cmd):
		command = self.Bytes.first_byte + cmd + self.Bytes.end_byte
		return command

	def parse_message(self, msg):
		res 			= ''
		tmp 			= ''
		charCnt 		= 0
		cmd 			= 0

		if (msg[0] == self.Bytes.first_byte):
			print(str(msg))
			cmd = int(msg[1])
			tmp = msg[2] + msg[3]
			charCnt = int(tmp)

			for i in range(charCnt):
				res += msg[i + 4]

			return cmd, res
		return 0, 0

	def prepare_rx(self, data):
		data = str(data)
		data = data.replace('b','')
		data = data.replace('\'','')
		msgs = data.split('\\n')
		return msgs

	def process_message(self, cmd, data):
		#self.logger.write_log('Command: ' + str(cmd))
		#self.logger.write_log('Message: ' + str(data))
		date = datetime.now().strftime("%Y_%m_%d")
		time = datetime.now().strftime("%H:%M:%S.%f")

		if (cmd == self.RxMessages.BMP_TEMPERATURE):
			sensor = 'BMP Temperature '
			msg = sensor + data + ' C'
		elif (cmd == self.RxMessages.HTU_TEMPERATURE):
			sensor = 'HTU Temperature '
			msg = sensor + data + ' C'
		elif (cmd == self.RxMessages.PRESSURE):
			sensor = 'BMP Pressure '
			msg = sensor + data + ' mm'
		elif (cmd == self.RxMessages.HUMIDITY):
			sensor = 'HTU Humiidity '
			msg = sensor + data + ' %'

		dict = {"sensor": sensor, "data": str(data),
				"date": date, "time": time}

		self.mongo.write(dict)
		#self.logger.write_log('Data: ' + msg)
		tm = datetime.now().strftime("%H:%M:%S.%f")
		print (msg)
		print (tm)
		return 1

