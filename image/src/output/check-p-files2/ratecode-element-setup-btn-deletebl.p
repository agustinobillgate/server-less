DEFINE INPUT PARAMETER number1 AS INT.
DEFINE INPUT PARAMETER user-init AS CHAR.

DEFINE OUTPUT PARAMETER str-msg AS CHAR.

DEFINE BUFFER bqueasy       FOR queasy.
DEFINE VARIABLE nr          AS INT INIT 0.
DEFINE VARIABLE num1        AS INT.
DEFINE VARIABLE ratecode    AS CHAR.




FIND FIRST queasy WHERE queasy.KEY = 287
    AND queasy.number1 = number1 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO :
    ratecode = queasy.char1.
    /*Alder - add validation - Start*/
    FIND FIRST bqueasy WHERE bqueasy.KEY EQ 289
        AND bqueasy.char2 EQ ratecode NO-LOCK NO-ERROR.
    IF AVAILABLE bqueasy THEN
    DO:
        str-msg = "Rate Code Element is currently being used, cannot be deleted".
    END.
    ELSE
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        DELETE queasy.
        RELEASE queasy.
    
        FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = bediener.nr
                res-history.datum       = TODAY
                res-history.zei         = TIME
                res-history.aenderung   = "Delete Ratecode Element, Code: " + ratecode
                res-history.action      = "Ratecode Element".
            FIND CURRENT res-history NO-LOCK.
            RELEASE res-history.
        END.
    END.
    /*Alder - add validation - End*/
END.
