
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
    delete h-artikel.
END.
