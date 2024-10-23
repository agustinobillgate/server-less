
DEF INPUT PARAMETER dept AS INT.
DEF OUTPUT PARAMETER avail-h-artikel AS LOGICAL INIT NO.

FIND FIRST h-artikel WHERE h-artikel.departement = dept NO-LOCK NO-ERROR. 
IF AVAILABLE h-artikel THEN
DO:
    avail-h-artikel = YES.
END.
