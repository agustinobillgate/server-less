
DEF INPUT  PARAMETER s-artnr AS INT.
DEF OUTPUT PARAMETER s-bezeich AS CHAR.
DEF OUTPUT PARAMETER close-date AS DATE.
DEF OUTPUT PARAMETER mm AS INT.
DEF OUTPUT PARAMETER yy AS INT.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK. 
s-bezeich = l-artikel.bezeich. 
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
