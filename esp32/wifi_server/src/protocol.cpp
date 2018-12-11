#include "..\include\protocol.h"
/***************************************************************************/
String prepareMessage(String msg, uint8_t num){
    String result = "$";

    result += num;

    if (msg.length() < 10){
        result += "0";
    }

    result += msg.length();
    result += msg;
    result += '\n';

    return result;
}
/***************************************************************************/
