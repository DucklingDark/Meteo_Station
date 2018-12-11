#include <Arduino.h>
#include <WString.h>
/***************************************************************************/
#define FIRST_BYTE      '$'
#define END_BYTE        '\n'
/***************************************************************************/
#define TEST_COMMAND    1
#define TEMP_BPM_CMD    2
#define TEMP_HTU_CMD    3
#define PRESSURE_CMD    4
#define HUMIDITY_CMD    5
/***************************************************************************/
String prepareMessage(String msg, uint8_t num);
/***************************************************************************/
