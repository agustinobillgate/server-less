
DEF INPUT PARAMETER s-list-s-recid AS INT.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.

FIND FIRST l-op WHERE RECID(l-op) = s-list-s-recid NO-LOCK.
FIND FIRST l-kredit WHERE l-kredit.lief-nr = l-op.lief-nr 
  AND l-kredit.name = l-op.docu-nr 
  AND l-kredit.lscheinnr = l-op.lscheinnr 
  AND l-kredit.opart GE 1 AND l-kredit.zahlkonto GT 0 NO-LOCK NO-ERROR. 
IF AVAILABLE l-kredit THEN 
DO: 
  err-code = 1.
  RETURN NO-APPLY. 
END. 
