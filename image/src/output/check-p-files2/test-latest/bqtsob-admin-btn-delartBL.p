
DEF INPUT  PARAMETER recid-queasy AS INT.
DEF OUTPUT PARAMETER err AS INT INIT 0.
/*
FIND FIRST queasy WHERE RECID(queasy) = recid-queasy NO-LOCK.

/* Rd, if available/recid, #371, 12-Des-24 */
/* 
FIND FIRST bediener WHERE bediener.user-group = int(queasy.char1) 
      AND bediener.flag = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE bediener THEN 
DO: 
    err = 1.
END. 
ELSE 
DO: 
    FIND CURRENT queasy EXCLUSIVE-LOCK. 
    delete queasy.
    RELEASE queasy.
END.
*/

IF NOT AVAILABLE queasy THEN RETURN.
FIND FIRST bediener WHERE bediener.user-group = int(queasy.char1) 
      AND bediener.flag = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE bediener THEN 
DO: 
    err = 1.
END. 
ELSE 
DO: 
    FIND CURRENT queasy EXCLUSIVE-LOCK. 
    IF AVAILABLE queasy THEN DO:
        delete queasy.
        RELEASE queasy.
    END.
END.
*/

FIND FIRST queasy WHERE RECID(queasy) EQ recid-queasy NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FIND FIRST bediener WHERE bediener.user-group EQ int(queasy.char1) AND bediener.flag EQ 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE bediener THEN 
    DO: 
        err = 1.
    END. 
    ELSE 
    DO: 
        FIND CURRENT queasy EXCLUSIVE-LOCK. 
        IF AVAILABLE queasy THEN 
        DO:
            DELETE queasy.
        END.
    END.
END.
