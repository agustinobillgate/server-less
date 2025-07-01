
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER err AS INT INIT 0.

FIND FIRST queasy WHERE RECID(queasy) = rec-id NO-LOCK.

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
