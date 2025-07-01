DEFINE TEMP-TABLE tb1 LIKE queasy
    FIELD waehrungsnr   LIKE waehrung.waehrungsnr
    FIELD wabkurz       LIKE waehrung.wabkurz
    FIELD freeze        AS LOGICAL
.

DEFINE INPUT PARAMETER TABLE FOR tb1.

DEFINE BUFFER bqueasy FOR queasy.
    
FOR EACH tb1 NO-LOCK:
    FIND FIRST queasy WHERE queasy.KEY EQ tb1.KEY AND queasy.char1 EQ tb1.char1 NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        BUFFER-COPY tb1 TO queasy.
    END.
    ELSE
    DO:
        ASSIGN
            queasy.char3 = tb1.char3.
    END.
    
    /*freeze ratecode*/
    FIND FIRST bqueasy WHERE bqueasy.KEY = 264
        AND bqueasy.char1 = tb1.char1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE bqueasy AND tb1.freeze = YES THEN DO:
        CREATE bqueasy.
        ASSIGN bqueasy.KEY   = 264
               bqueasy.char1 = tb1.char1
               bqueasy.logi1 = tb1.freeze.
    END.
    ELSE IF AVAILABLE bqueasy THEN DO:
        FIND CURRENT bqueasy EXCLUSIVE-LOCK.
        ASSIGN bqueasy.logi1 = tb1.freeze.
        FIND CURRENT bqueasy NO-LOCK.
        RELEASE bqueasy.
    END.
END.
