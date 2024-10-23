/*****************************************************************
Author          : Irfan Fadhillah
Created Date    : July 16, 2019
Purpose         : Check Block ID
*****************************************************************/

DEFINE INPUT PARAMETER blockID      AS CHARACTER.
DEFINE OUTPUT PARAMETER availFlag   AS LOGICAL      INITIAL NO.

FIND FIRST bk-master WHERE bk-master.block-id EQ blockID NO-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN
DO:
    availFlag = YES.
END.
