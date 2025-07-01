
DEF INPUT-OUTPUT PARAMETER s-bezeich     AS CHAR.
DEF INPUT  PARAMETER inp-artnr     AS INTEGER.
DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER show-price    AS LOGICAL.
DEF OUTPUT PARAMETER avail-l-artikel AS LOGICAL INIT NO.

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 
 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 

IF inp-artnr NE 0 THEN 
DO: 
  FIND FIRST l-artikel WHERE l-artikel.artnr = inp-artnr NO-LOCK NO-ERROR. 
  IF AVAILABLE l-artikel THEN 
  DO: 
    s-bezeich = l-artikel.bezeich.
    avail-l-artikel = YES.
  END. 
END. 
