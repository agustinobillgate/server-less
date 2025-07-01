
DEF INPUT  PARAMETER rec-id         AS INT.
DEF OUTPUT PARAMETER t-depn-wert    AS INT.
DEF OUTPUT PARAMETER err-flag       AS INT INIT 0.

FIND FIRST fa-op WHERE RECID(fa-op) = rec-id.
FIND FIRST fa-artikel WHERE fa-artikel.nr = fa-op.nr NO-LOCK. 
IF fa-artikel.depn-wert NE 0 THEN 
DO: 
  t-depn-wert = fa-artikel.depn-wert.
  err-flag = 1.
END. 
ELSE 
DO: 
  FIND FIRST l-kredit WHERE l-kredit.name = fa-op.lscheinnr 
    AND l-kredit.lief-nr = fa-op.lief-nr 
    AND l-kredit.opart GE 1 NO-LOCK NO-ERROR. 
  IF AVAILABLE l-kredit THEN 
  DO: 
    err-flag = 2.
  END. 
  ELSE 
  DO: 
    err-flag = 3.
  END. 
END. 
