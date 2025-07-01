
DEF INPUT  PARAMETER recid-queasy AS INT.
DEF OUTPUT PARAMETER err AS INT INIT 0.

FIND FIRST queasy WHERE RECID(queasy) = recid-queasy NO-LOCK.

FIND FIRST bediener WHERE bediener.user-group = int(queasy.char1) 
  AND bediener.flag = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE bediener THEN 
DO: 
    err = 1.
    RETURN.
END. 
ELSE 
DO: 
    FIND CURRENT queasy EXCLUSIVE-LOCK. 
    DELETE queasy. 
    RELEASE queasy.
END.
