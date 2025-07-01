
DEF INPUT  PARAMETER s-artnr1       AS INT.
DEF INPUT  PARAMETER avail-out-list AS LOGICAL.
DEF OUTPUT PARAMETER l-artikel-artnr AS INT.
DEF OUTPUT PARAMETER descript1      AS CHAR.
DEF OUTPUT PARAMETER err-flag       AS INT INIT 0.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr1 NO-LOCK NO-ERROR.
IF NOT AVAILABLE l-artikel THEN 
DO: 
    err-flag = 1.
    RETURN NO-APPLY. 
END. 
l-artikel-artnr = l-artikel.artnr.
IF l-artikel.betriebsnr = 0 THEN 
DO: 
    IF avail-out-list THEN 
    DO:
      err-flag = 2.
      RETURN NO-APPLY. 
    END. 
    descript1 = l-artikel.bezeich + " - " + l-artikel.masseinheit. 
    err-flag = 3.
    RETURN NO-APPLY. 
END. 
