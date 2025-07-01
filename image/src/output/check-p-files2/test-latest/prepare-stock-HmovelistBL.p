
DEF INPUT-OUTPUT PARAMETER s-bezeich AS CHAR.
DEF INPUT  PARAMETER user-init AS CHAR.
DEF INPUT  PARAMETER inp-artnr AS INT.

DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER close-date AS DATE.
DEF OUTPUT PARAMETER mm AS INT INIT ?.
DEF OUTPUT PARAMETER yy AS INT INIT ?.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0 NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 

IF inp-artnr NE 0 THEN 
DO: 
  FIND FIRST l-artikel WHERE l-artikel.artnr = inp-artnr NO-LOCK NO-ERROR. 
  IF AVAILABLE l-artikel THEN 
  DO: 
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
    fl-code = 1.
  END. 
END. 
