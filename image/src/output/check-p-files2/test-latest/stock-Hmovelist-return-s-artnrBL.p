
DEF INPUT-OUTPUT PARAMETER s-bezeich AS CHAR.
DEF INPUT PARAMETER s-artnr AS INT.

DEF OUTPUT PARAMETER close-date AS DATE.
DEF OUTPUT PARAMETER mm AS INT INIT ?.
DEF OUTPUT PARAMETER yy AS INT INIT ?.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK NO-ERROR. 
IF AVAILABLE l-artikel THEN 
DO: 
    IF l-artikel.endkum LE 2 THEN FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
    ELSE FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
    ASSIGN
      close-date = htparam.fdate /* current INV close date */
      mm = MONTH(close-date) - 1
      yy = YEAR(close-date)
    .
    IF mm = 0 THEN
    ASSIGN
      mm = 12
      yy = yy - 1
    .
    s-bezeich = l-artikel.bezeich. 
END.
