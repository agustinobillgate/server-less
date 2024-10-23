
DEF INPUT PARAMETER curr-lager AS INT.
DEF OUTPUT PARAMETER avail-l-lager AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER l-lager-bezeich AS CHAR.

FIND FIRST l-lager WHERE l-lager.lager-nr = curr-lager NO-LOCK NO-ERROR. 
IF AVAILABLE l-lager THEN 
DO:
    l-lager-bezeich = l-lager.bezeich.
    avail-l-lager = YES.
END.
    
