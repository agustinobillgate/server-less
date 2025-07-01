DEFINE INPUT PARAMETER orderID        AS CHAR.
DEFINE INPUT PARAMETER changeStatusTo AS CHAR.

DEFINE VARIABLE param1 AS CHAR.
DEFINE VARIABLE param2 AS CHAR.
DEFINE VARIABLE param3 AS CHAR.

FIND FIRST queasy WHERE queasy.KEY EQ 271 
    AND queasy.betriebsnr EQ 1 
    AND queasy.number2 EQ INT(orderID) NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK.

    param1 = ENTRY(1,queasy.char1,"|").
    param2 = ENTRY(2,queasy.char1,"|").
    param3 = ENTRY(3,queasy.char1,"|").

    queasy.char1 = param1 + "|" + changeStatusTo + "|" + param3. 

    FIND CURRENT queasy NO-LOCK.
    RELEASE queasy.
END.
