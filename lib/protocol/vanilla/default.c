
int vanilla_default_getDataType(char data[])
{
}
/**
 * @return true if a response-message should be sent
 */
int vanilla_default_concatMessage(char response[], char data[], int type)
{
    switch (type)
    {
    case T_HANDSHAKE:
        return 0;
    case T_REQUEST:
        //response == responsemessage
        return 1;
    case T_PING:
        //response == pong
        return 1;
    default:
        break;
    }
}