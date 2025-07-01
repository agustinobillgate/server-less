
DEF INPUT PARAMETER qty         AS DECIMAL.
DEF INPUT PARAMETER s-artnr     AS INT.
DEF INPUT PARAMETER curr-lager  AS INT.
DEF OUTPUT PARAMETER rest       AS DECIMAL.
DEF OUTPUT PARAMETER err-code   AS INT INIT 0.

DEFINE buffer l-oh FOR l-bestand. 

IF qty LT 0 THEN 
DO:
    FIND FIRST l-oh WHERE l-oh.artnr = s-artnr AND l-oh.lager-nr 
      = curr-lager NO-LOCK NO-ERROR. 
    IF AVAILABLE l-oh AND (anz-anf-best + anz-eingang - anz-ausgang + qty) LT 0 
    THEN 
    DO: 
      err-code = 1.
      rest = (anz-anf-best + anz-eingang - anz-ausgang + qty). 
      RETURN NO-APPLY. 
    END.
END.
  
FIND FIRST htparam WHERE paramnr = 402 NO-LOCK. 
IF htparam.paramgruppe = 15 THEN 
DO: 
    err-code = 2.
    RETURN NO-APPLY. 
END. 

IF NOT htparam.flogical THEN 
DO: 
    err-code = 3.
    RETURN NO-APPLY. 
END.
