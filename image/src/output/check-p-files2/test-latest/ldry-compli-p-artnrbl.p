
DEF INPUT PARAMETER artnr AS INT.
DEF INPUT PARAMETER c-list-dept AS INT.
DEF INPUT PARAMETER c-list-rechnr AS INT.
DEF INPUT PARAMETER c-list-datum AS DATE.
DEF OUTPUT PARAMETER flag AS INT INIT 0.
DEF OUTPUT PARAMETER t-bez AS CHAR.

FIND FIRST h-artikel WHERE h-artikel.artnr = artnr 
    AND h-artikel.departement = c-list-dept NO-LOCK NO-ERROR. 
IF NOT AVAILABLE h-artikel THEN 
DO: 
    flag = 1.
    RETURN NO-APPLY. 
END.
flag = 2.
t-bez = h-artikel.bezeich.
FOR EACH h-compli WHERE h-compli.datum = c-list-datum 
    AND c-list-dept = h-compli.departement
    AND c-list-rechnr = h-compli.rechnr: 
    h-compli.p-artnr = artnr.
END.
