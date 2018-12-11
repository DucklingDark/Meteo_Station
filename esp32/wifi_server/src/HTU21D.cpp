#include "..\include\HTU21D.h"
/***************************************************************************/
HTU21D::HTU21D(HTU21D_RESOLUTION sensorResolution) {
	_resolution = sensorResolution;
}
/***************************************************************************/
#if defined(ESP8266)
bool HTU21D::begin(uint8_t sda, uint8_t scl) {
	Wire.begin(sda, scl);
	Wire.setClock(100000UL);
	Wire.setClockStretchLimit(230);
#else
bool HTU21D::begin(void) {
	Wire.begin();
	Wire.setClock(100000UL);
#endif

	Wire.beginTransmission(HTU21D_ADDRESS);

	if (Wire.endTransmission(true) != 0) {
#ifdef HTU21D_DEBUG_INFO
		Serial.println("HTU21D: can't find the sensor on the bus");
#endif
		return false;
	}

	setResolution(_resolution);
	setHeater(HTU21D_OFF);
	return true;
}
/***************************************************************************/
void HTU21D::setResolution(HTU21D_RESOLUTION sensorResolution) {
	uint8_t userRegisterData = 0;

	userRegisterData = read8(HTU21D_USER_REGISTER_READ);
	userRegisterData &= 0x7E;
	userRegisterData |= sensorResolution;

	write8(HTU21D_USER_REGISTER_WRITE, userRegisterData);

	_resolution = sensorResolution;
}
/***************************************************************************/
void HTU21D::softReset(void) {
	uint8_t pollCounter = HTU21D_POLL_LIMIT;

	do {
		pollCounter--;

		if (pollCounter == 0) {
#ifdef HTU21D_DEBUG_INFO
			Serial.println("HTU21D: can't send soft reset command");
#endif
		}

		Wire.beginTransmission(HTU21D_ADDRESS);
#if ARDUINO >= 100
		Wire.write(HTU21D_SOFT_RESET);
#else
		Wire.send(HTU21D_SOFT_RESET);
#endif
	} while (Wire.endTransmission(true) != 0);

	delay(HTU21D_SOFT_RESET_DELAY);
}
/***************************************************************************/
bool HTU21D::batteryStatus(void) {
	uint8_t userRegisterData = 0;

	userRegisterData = read8(HTU21D_USER_REGISTER_READ);
	userRegisterData &= 0x40;

	if (userRegisterData == 0x00) {
		return true;
	}
	return false;
}
/***************************************************************************/
void HTU21D::setHeater(HTU21D_HEATER_SWITCH heaterSwitch) {
	uint8_t userRegisterData = 0;

	userRegisterData = read8(HTU21D_USER_REGISTER_READ);

	switch (heaterSwitch) {
	case HTU21D_ON:
		userRegisterData |= heaterSwitch;
		break;
	case HTU21D_OFF:
		userRegisterData &= heaterSwitch;
		break;
	}
	write8(HTU21D_USER_REGISTER_WRITE, userRegisterData);
}
/***************************************************************************/
float HTU21D::readHumidity(HTU21D_HUMD_OPERATION_MODE sensorOperationMode) {
	uint8_t  pollCounter = HTU21D_POLL_LIMIT;
	uint8_t  checksum = 0;
	uint16_t rawHumidity = 0;
	float    humidity = 0;

	do {
		pollCounter--;
		if (pollCounter == 0)
		{
#ifdef HTU21D_DEBUG_INFO
			Serial.println("HTU21D: can't send humidity measurement command");
#endif
			return HTU21D_ERROR;
		}
		Wire.beginTransmission(HTU21D_ADDRESS);
#if ARDUINO >= 100
		Wire.write(sensorOperationMode);
#else
		Wire.send(sensorOperationMode);
#endif
	} while (Wire.endTransmission(true) != 0);

	switch (_resolution) {
    	case HTU21D_RES_RH12_TEMP14:
    		delay(16);
    		break;
    	case HTU21D_RES_RH8_TEMP12:
    		delay(3);
    		break;
    	case HTU21D_RES_RH10_TEMP13:
    		delay(5);
    		break;
    	case HTU21D_RES_RH11_TEMP11:
    		delay(8);
    		break;
	}

	pollCounter = HTU21D_POLL_LIMIT;

	do {
		pollCounter--;

		if (pollCounter == 0)  {
#ifdef HTU21D_DEBUG_INFO
			Serial.println("HTU21D: can't read humidity measurement result");
#endif
			return HTU21D_ERROR;
		}

		if (pollCounter < (HTU21D_POLL_LIMIT - 1)){
            delay(8);
        }

		Wire.requestFrom(HTU21D_ADDRESS, 3, true);
	} while (Wire.available() != 3);

#if ARDUINO >= 100
	rawHumidity = Wire.read() << 8;
	rawHumidity |= Wire.read();
	checksum = Wire.read();
#else
	rawHumidity = Wire.receive() << 8;
	rawHumidity |= Wire.receive();
	checksum = Wire.receive();
#endif

	if (checkCRC8(rawHumidity) != checksum){
#ifdef HTU21D_DEBUG_INFO
		Serial.println("HTU21D: humidity CRC8 doesn't match");
#endif
		return HTU21D_ERROR;
	}

	rawHumidity ^= 0x02;
	humidity = 0.001907 * (float)rawHumidity - 6;

	if (humidity < 0) {
		humidity = 0;
	} else {
        if (humidity > 100) {
		          humidity = 100;
        }
	}
	return humidity;
}
/***************************************************************************/
float HTU21D::readTemperature(HTU21D_TEMP_OPERATION_MODE sensorOperationMode) {
	uint8_t  pollCounter = HTU21D_POLL_LIMIT;
	uint8_t  checksum = 0;
	uint16_t rawTemperature = 0;

	do {
		pollCounter--;

		if (pollCounter == 0){
#ifdef HTU21D_DEBUG_INFO
			Serial.println("HTU21D: can't send temperature measurement command");
#endif
			return HTU21D_ERROR;
		}

		Wire.beginTransmission(HTU21D_ADDRESS);
#if ARDUINO >= 100
		Wire.write(sensorOperationMode);
#else
		Wire.send(sensorOperationMode);
#endif
	} while (Wire.endTransmission(true) != 0);

	if (sensorOperationMode != SI70xx_TEMP_READ_AFTER_RH_MEASURMENT) {
		switch (_resolution) {
		case HTU21D_RES_RH12_TEMP14:
			delay(11);
			break;
		case HTU21D_RES_RH8_TEMP12:
			delay(4);
			break;
		case HTU21D_RES_RH10_TEMP13:
			delay(7);
			break;
		case HTU21D_RES_RH11_TEMP11:
			delay(3);
			break;
		}
	}

	pollCounter = HTU21D_POLL_LIMIT;

	do {
		pollCounter--;

		if (pollCounter == 0){
#ifdef HTU21D_DEBUG_INFO
			Serial.println("HTU21D: can't read temperature measurement result");
#endif
			return HTU21D_ERROR;
		}

		if (pollCounter < (HTU21D_POLL_LIMIT - 1)){
            delay(16);
        }

		Wire.requestFrom(HTU21D_ADDRESS, 3, true);
	} while (Wire.available() != 3);

#if ARDUINO >= 100
	rawTemperature = Wire.read() << 8;
	rawTemperature |= Wire.read();
	checksum = Wire.read();
#else
	rawTemperature = Wire.receive() << 8;
	rawTemperature |= Wire.receive();
	checksum = Wire.receive();
#endif

	if (checkCRC8(rawTemperature) != checksum){
#ifdef HTU21D_DEBUG_INFO
		Serial.println("HTU21D: temperature CRC8 doesn't match");
#endif
		return HTU21D_ERROR;
	}

	return 0.002681 * (float)rawTemperature - 46.85;
}
/***************************************************************************/
float HTU21D::readCompensatedHumidity(void) {
	float humidity = 0;
	float temperature = 0;

	humidity = readHumidity();
	temperature = readTemperature();

	if (humidity == HTU21D_ERROR || temperature == HTU21D_ERROR){
		return HTU21D_ERROR;
	}

	if (temperature > 0 && temperature < 80) {
		humidity = humidity + (25 - temperature) * HTU21D_TEMP_COEFFICIENT;
	}

	return humidity;
}
/***************************************************************************/
uint16_t HTU21D::readDeviceID(void) {
	uint16_t deviceID = 0;
	uint8_t  checksum = 0;

	Wire.beginTransmission(HTU21D_ADDRESS);
#if ARDUINO >= 100
	Wire.write(HTU21D_SERIAL2_READ1);
	Wire.write(HTU21D_SERIAL2_READ2);
#else
	Wire.send(HTU21D_SERIAL2_READ1);
	Wire.send(HTU21D_SERIAL2_READ2);
#endif
	Wire.endTransmission(true);

	Wire.requestFrom(HTU21D_ADDRESS, 3, true);
#if ARDUINO >= 100
	deviceID = Wire.read() << 8;
	deviceID |= Wire.read();
	checksum = Wire.read();
#else
	deviceID = Wire.receive() << 8;
	deviceID |= Wire.receive();
	checksum = Wire.receive();
#endif
	if (checkCRC8(deviceID) != checksum) {
#ifdef HTU21D_DEBUG_INFO
		Serial.println("HTU21D: device ID CRC8 doesn't match");
#endif
		return HTU21D_ERROR;
	}

	deviceID = deviceID >> 8;

	switch (deviceID) {
    	case HTU21D_CHIPID:
    		deviceID = 21;
    		break;
    	case SI7013_CHIPID:
    		deviceID = 7013;
    		break;
    	case SI7020_CHIPID:
    		deviceID = 7020;
    		break;
    	case SI7021_CHIPID:
    		deviceID = 7021;
    		break;
    	default:
    		deviceID = HTU21D_ERROR;
    		break;
	}
	return deviceID;
}
/***************************************************************************/
uint8_t HTU21D::readFirmwareVersion(void) {
	uint8_t firmwareVersion = 0;

	Wire.beginTransmission(HTU21D_ADDRESS);
#if ARDUINO >= 100
	Wire.write(HTU21D_FIRMWARE_READ1);
	Wire.write(HTU21D_FIRMWARE_READ2);
#else
	Wire.send(HTU21D_FIRMWARE_READ1);
	Wire.send(HTU21D_FIRMWARE_READ2);
#endif
	Wire.endTransmission(true);

	Wire.requestFrom(HTU21D_ADDRESS, 1, true);
#if ARDUINO >= 100
	firmwareVersion = Wire.read();
#else
	firmwareVersion = Wire.read();
#endif

	switch (firmwareVersion) {
    	case HTU21D_FIRMWARE_V1:
    		firmwareVersion = 1;
    		break;
    	case HTU21D_FIRMWARE_V2:
    		firmwareVersion = 2;
    		break;
    	default:
    		firmwareVersion = HTU21D_ERROR;
    		break;
	}

	return firmwareVersion;
}
/**************************************************************************/
void HTU21D::write8(uint8_t reg, uint8_t value) {
	uint8_t pollCounter = HTU21D_POLL_LIMIT;

	do {
		pollCounter--;

		if (pollCounter == 0){
#ifdef HTU21D_DEBUG_INFO
			Serial.println("HTU21D: can't write a byte");
#endif
			return;
		}

		Wire.beginTransmission(HTU21D_ADDRESS);
#if ARDUINO >= 100
		Wire.write(reg);
		Wire.write(value);
#else
		Wire.send(reg);
		Wire.send(value);
#endif
	} while (Wire.endTransmission(true) != 0);
}
/**************************************************************************/
uint8_t HTU21D::read8(uint8_t reg) {
	uint8_t pollCounter = HTU21D_POLL_LIMIT;

	do {
		pollCounter--;

		if (pollCounter == 0){
#ifdef HTU21D_DEBUG_INFO
			Serial.println("HTU21D: can't request a byte");
#endif
			return HTU21D_ERROR;
		}

		Wire.beginTransmission(HTU21D_ADDRESS);
#if ARDUINO >= 100
		Wire.write(reg);
#else
		Wire.send(reg);
#endif
	} while (Wire.endTransmission(true) != 0);

	pollCounter = HTU21D_POLL_LIMIT;

	do {
		pollCounter--;

		if (pollCounter == 0){
#ifdef HTU21D_DEBUG_INFO
			Serial.println("HTU21D: can't read a byte");
#endif
			return HTU21D_ERROR;
		}

		Wire.requestFrom(HTU21D_ADDRESS, 1, true);
	} while (Wire.available() != 1);

#if ARDUINO >= 100
	return Wire.read();
#else
	return Wire.receive();
#endif
}
/**************************************************************************/
uint8_t HTU21D::checkCRC8(uint16_t data) {
	for (uint8_t bit = 0; bit < 16; bit++) {
		if (data & 0x8000) {
			data = (data << 1) ^ HTU21D_CRC8_POLYNOMINAL;
		} else {
			data <<= 1;
		}
	}

	return data >>= 8;
}
