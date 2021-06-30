
struct messageInfoData getMessageInfoData(char data[], struct messageInfoData previusData)
{
    if (previusData.empty)
    {
        //Get protocol, modify previusData
        return previusData;
    }
    // not that much has to be done, refactor?
}

int parseVarInt(char data[])
{
    int i = 0;
    while (1)
    {
        switch (data[i])
        {
        case 0xFD:
            /* code */
            break;
        case 0xFFFF:
            /* code */
            break;
        case 0xFFFFFFFF:
            /* code */
            break;

        default:
            break;
        }
        ++i;
    }
}
int concatVarInt(char data[], int startPoint)
{
    //Stuff
}