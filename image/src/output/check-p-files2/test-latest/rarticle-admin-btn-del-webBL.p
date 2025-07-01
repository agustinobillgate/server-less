
DEF INPUT  PARAMETER h-artnr AS INT.
DEF INPUT  PARAMETER h-dept  AS INT.
DEF OUTPUT PARAMETER flag    AS INT INIT 0.

FIND FIRST h-artikel WHERE h-artikel.artnr = h-artnr 
    AND h-artikel.departement = h-dept NO-LOCK.
FIND FIRST h-umsatz WHERE h-umsatz.artnr = h-artnr
    AND h-umsatz.departement = h-dept NO-LOCK NO-ERROR. 
IF AVAILABLE h-umsatz THEN
DO: 
    flag = 1.
END. 
ELSE 
DO: 
    flag = 2.
    FIND CURRENT h-artikel EXCLUSIVE-LOCK. 
    DELETE h-artikel.

    /*FDL Oct 31, 2024: Ticket 9EBEF5*/
    FIND FIRST queasy WHERE queasy.KEY EQ 222 
         AND queasy.number1 EQ 2 
         AND queasy.number2 EQ h-artnr
         AND queasy.number3 EQ h-dept NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        DELETE queasy.
        RELEASE queasy.
    END.
END.
