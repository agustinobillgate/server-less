
DEF INPUT  PARAMETER s-artnr    AS INT.
DEF INPUT  PARAMETER qty        AS DECIMAL.
DEF INPUT  PARAMETER stock-oh   AS DECIMAL.
DEF OUTPUT PARAMETER err-flag   AS INT INIT 0.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK NO-ERROR. 

IF qty GT stock-oh AND l-artikel.betriebsnr = 0 THEN 
DO: 
  err-flag = 1.
  RETURN NO-APPLY. 
END. 
ELSE 
DO: 
  FIND FIRST htparam WHERE paramnr = 232 NO-LOCK. 
  IF htparam.flogical THEN 
  DO: 
    err-flag = 2.
    RETURN NO-APPLY. 
  END. 
  ELSE 
  DO: 
    err-flag = 99.
  END. 
END. 
