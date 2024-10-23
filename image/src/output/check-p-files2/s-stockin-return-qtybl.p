
DEF INPUT PARAMETER curr-lager AS INT.
DEF INPUT PARAMETER s-artnr AS INT.
DEF INPUT PARAMETER qty AS DECIMAL.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.
DEF OUTPUT PARAMETER rest AS DECIMAL.

DEFINE buffer l-oh FOR l-bestand. 

FIND FIRST l-oh WHERE l-oh.artnr = s-artnr AND l-oh.lager-nr = curr-lager NO-LOCK NO-ERROR. 
IF AVAILABLE l-oh AND (anz-anf-best + anz-eingang - anz-ausgang + qty) LT 0 
THEN DO:
  err-code = 1.
  rest = (anz-anf-best + anz-eingang - anz-ausgang + qty). 
  RETURN NO-APPLY. 
END. 
