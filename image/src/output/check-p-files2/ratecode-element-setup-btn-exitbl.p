DEFINE TEMP-TABLE temp-list LIKE queasy.

DEFINE INPUT PARAMETER TABLE FOR temp-list.
DEFINE INPUT PARAMETER icase AS INT.
DEFINE INPUT PARAMETER user-init AS CHAR.

DEFINE VARIABLE ratecode AS CHAR.
DEFINE VARIABLE ratecode2 AS CHAR.

FIND FIRST temp-list.
IF icase EQ 1 THEN
DO :
    CREATE queasy.
    ASSIGN
        queasy.KEY      = 287
        queasy.number1  = temp-list.number1
        queasy.char1    = temp-list.char1
        ratecode        = temp-list.char1.
    FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        CREATE res-history.
        ASSIGN
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.aenderung   = "Add Ratecode Element, Code: " + ratecode
            res-history.action      = "Ratecode Element".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.
    END.
END.
ELSE
DO:
    FIND FIRST queasy WHERE queasy.KEY = 287 
        AND queasy.number1 = temp-list.number1 NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ratecode = queasy.char1.
        BUFFER-COPY temp-list TO queasy.
        ratecode2 = temp-list.char1.
        FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = bediener.nr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.aenderung   = "Change Ratecode Element, From: " + ratecode + " To: " + ratecode2
                res-history.action      = "Ratecode Element".
            FIND CURRENT res-history NO-LOCK.
            RELEASE res-history.
        END.
    END.
END.
