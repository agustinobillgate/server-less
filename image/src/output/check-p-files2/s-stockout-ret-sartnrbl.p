
DEF INPUT PARAMETER s-artnr AS INT.
DEF INPUT PARAMETER transdate AS DATE.

DEF OUTPUT PARAMETER avail-l-op AS LOGICAL INIT NO.

FIND FIRST l-op WHERE l-op.artnr = s-artnr AND 
    l-op.datum = transdate AND (l-op.op-art = 3 OR l-op.op-art = 4) 
    AND SUBSTR(l-op.lscheinnr,4, (length(l-op.lscheinnr) - 3)) = 
    SUBSTR(lscheinnr,4, (length(lscheinnr) - 3)) NO-LOCK NO-ERROR. 
IF AVAILABLE l-op THEN avail-l-op = YES.
