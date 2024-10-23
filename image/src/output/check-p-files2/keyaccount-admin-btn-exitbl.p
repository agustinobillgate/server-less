DEF TEMP-TABLE temp-list LIKE queasy.

DEF INPUT PARAMETER TABLE FOR temp-list.
DEF INPUT PARAMETER icase       AS INT.
DEF INPUT PARAMETER user-init   AS CHAR.

DEFINE VARIABLE category    AS CHARACTER.
DEFINE VARIABLE category2   AS CHARACTER.

FIND FIRST temp-list.
IF icase = 1 THEN
DO:
    CREATE queasy.
    ASSIGN
        queasy.KEY     = 211
        queasy.number1 = temp-list.number1
        queasy.char1   = temp-list.char1
        category       = temp-list.char1.

    FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        CREATE res-history.
        ASSIGN
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.aenderung   = "Add KeyAccount, Name: " + category
            res-history.action      = "Key Account".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.
    END.
END.
ELSE
DO:
    FIND FIRST queasy WHERE queasy.KEY = 211 AND 
        queasy.number1 = temp-list.number1 NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        category  = queasy.char1.
        BUFFER-COPY temp-list TO queasy.
        category2 = temp-list.char1.

        FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = bediener.nr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.aenderung   = "Change KeyAccount, From: " + category + " To: " + category2
                res-history.action      = "Key Account".
            FIND CURRENT res-history NO-LOCK.
            RELEASE res-history.
        END.
    END.
END.
