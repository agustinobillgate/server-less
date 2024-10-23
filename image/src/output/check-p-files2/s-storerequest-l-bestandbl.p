
DEF INPUT PARAMETER curr-lager AS INT.
DEF INPUT PARAMETER s-artnr AS INT.
DEF INPUT PARAMETER transdate AS DATE.
DEF OUTPUT PARAMETER avail-l-bestand AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER avail-l-op AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER stock-oh AS DECIMAL.

FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager
    AND l-bestand.artnr = s-artnr NO-LOCK NO-ERROR.
IF AVAILABLE l-bestand THEN
DO:
    avail-l-bestand = YES.
    stock-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 

    FIND FIRST l-op WHERE l-op.artnr = s-artnr AND 
        l-op.datum = transdate AND (l-op.op-art = 13 OR l-op.op-art = 14) 
        AND SUBSTR(l-op.lscheinnr,4, (length(l-op.lscheinnr) - 3)) = 
        SUBSTR(lscheinnr,4, (length(lscheinnr) - 3)) NO-LOCK NO-ERROR. 
    IF AVAILABLE l-op THEN avail-l-op = YES.
END.
    
