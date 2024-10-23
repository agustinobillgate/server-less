
DEF INPUT PARAMETER d-artnr AS INT.
DEF OUTPUT PARAMETER s-artnr AS INT.
DEF OUTPUT PARAMETER description AS CHAR.
DEF OUTPUT PARAMETER avail-l-artikel AS LOGICAL INIT NO.

FIND FIRST l-artikel WHERE l-artikel.artnr = d-artnr NO-LOCK NO-ERROR.
IF AVAILABLE l-artikel THEN
DO: 
    avail-l-artikel = YES.
    ASSIGN
        s-artnr     = l-artikel.artnr 
        description = TRIM(l-artikel.bezeich) + " - " 
                    + STRING(l-artikel.masseinheit,"x(3)"). 
END.

