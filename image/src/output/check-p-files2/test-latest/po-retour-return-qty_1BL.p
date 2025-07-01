DEF TEMP-TABLE t-queasy LIKE queasy.

DEF INPUT PARAMETER transdate  AS DATE.
DEF INPUT PARAMETER closedate  AS DATE.
DEF INPUT PARAMETER s-artnr    AS INT.
DEF INPUT PARAMETER curr-lager AS INT.
DEF INPUT PARAMETER qty        AS DECIMAL.
DEF INPUT PARAMETER content    AS INTEGER.
DEF OUTPUT PARAMETER err-code  AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

DEFINE buffer l-oh FOR l-bestand.
DEFINE VARIABLE qty1 AS DECIMAL.

IF transdate LE closedate THEN 
DO:
    ASSIGN qty1 = qty * content.
    FIND FIRST l-oh WHERE l-oh.artnr = s-artnr
      AND l-oh.lager-nr = curr-lager NO-LOCK NO-ERROR. 
    IF AVAILABLE l-oh THEN 
    DO: 
      IF (l-oh.anz-anf-best + l-oh.anz-eingang - l-oh.anz-ausgang) LT qty1 THEN 
      DO:
        err-code = 1.
        RETURN.
      END. 
    END.
END. 

FIND FIRST queasy WHERE queasy.KEY = 20 AND queasy.number1 = s-artnr 
    NO-LOCK NO-ERROR. 
IF AVAILABLE queasy THEN 
DO:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.
