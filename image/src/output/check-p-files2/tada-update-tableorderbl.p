DEFINE INPUT PARAMETER orderID  AS CHAR.
DEFINE INPUT PARAMETER tischnr  AS INT.

DEFINE VARIABLE param1 AS CHAR.
DEFINE VARIABLE param3 AS CHAR.
DEFINE VARIABLE param4 AS CHAR.
DEFINE VARIABLE param5 AS CHAR.
DEFINE VARIABLE param6 AS CHAR.

FIND FIRST queasy WHERE queasy.KEY EQ 271 
    AND queasy.betriebsnr EQ 1 
    AND queasy.number2 EQ INT(orderID) NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK.

    param1 = ENTRY(1,queasy.char2,"|").
    param3 = ENTRY(3,queasy.char2,"|").
    param4 = ENTRY(4,queasy.char2,"|").
    param5 = ENTRY(5,queasy.char2,"|").
    param6 = ENTRY(6,queasy.char2,"|").

    queasy.char2 = param1 + "|" + STRING(tischnr) + "|" + param3 + "|" + param4 + "|" + param5 + "|" + param6. 

    FIND CURRENT queasy NO-LOCK.
    RELEASE queasy.
END.
