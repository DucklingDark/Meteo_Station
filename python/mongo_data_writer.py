import sys
import socket
import errno
from time import sleep
from imports.protocol import Protocol
from imports.mongo import Mongo
from imports.configer import Configer

iniPath 		= 'configs\\config.ini'
configer        = Configer(iniPath)
mongo           = Mongo(configer.Settings.mongo.client, 
                        configer.Settings.mongo.db, 
                        configer.Settings.mongo.collection)
proto 			= Protocol(mongo)

while (True):
	sock = socket.socket()
	sock.connect((configer.Settings.socket.ip,
				  int(configer.Settings.socket.port)))
	sock.settimeout(0.03)

	message 	= ''
	command 	= ''
	rxCmd		= 0
	rxMsg		= 0

	while (True):
		try:
			command = proto.prepare_command(proto.Commands.client_ready)
			byt=command.encode()
			sock.send(byt)
			sleep(0.01)
			data = sock.recv(1024)
			msgs = proto.prepare_rx(data)
			count = len(msgs)

			for i in range(count - 1):
				rxCmd, rxMsg = proto.parse_message(msgs[i])
				
				if (rxCmd != 0 and rxMsg != 0):
					proto.process_message(rxCmd, rxMsg)
				else:
					print('Incorrect message')		

		except socket.error as e:
			err = e.args[0]

			if (err == errno.EAGAIN) or (err == errno.EWOULDBLOCK):
				continue
			else:
				break

	sock.close()