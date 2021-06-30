#ifndef protocol_h
#define protocol_h
//Define all functions, including those in the protocol folders
struct messageInfoData
{
    int empty;
    int (*getType)(char data[]);
    int (*getResponse)(char response[], char data[], int type);
};
struct messageInfoData getMessageInfoData(char data[], struct messageInfoData previusData);

#define T_HANDSHAKE 0
#define T_REQUEST 1
#define T_PING 2

#define P_VANILLA 0
#endif