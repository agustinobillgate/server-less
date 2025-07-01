DEFINE TEMP-TABLE trate-code LIKE queasy
    FIELD active-flag AS LOGICAL INIT NO.

DEFINE INPUT PARAMETER TABLE FOR trate-code.

DEFINE BUFFER bqueasy FOR queasy.

FOR EACH trate-code NO-LOCK:
    FIND FIRST bqueasy WHERE bqueasy.KEY = 264
        AND bqueasy.char1 = trate-code.char1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE bqueasy AND trate-code.active-flag = YES THEN DO:
        CREATE bqueasy.
        ASSIGN bqueasy.KEY   = 264
               bqueasy.char1 = trate-code.char1
               bqueasy.logi1 = trate-code.active-flag.
    END.
    ELSE IF AVAILABLE bqueasy THEN DO:
        FIND CURRENT bqueasy EXCLUSIVE-LOCK.
        ASSIGN bqueasy.logi1 = trate-code.active-flag.
        FIND CURRENT bqueasy NO-LOCK.
        RELEASE bqueasy.
    END.
END.
