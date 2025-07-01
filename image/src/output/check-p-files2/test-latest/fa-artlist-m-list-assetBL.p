DEFINE INPUT PARAMETER asset        AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER avail-asset AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER mathis-name AS CHAR    NO-UNDO.

DEFINE buffer mathis1 FOR mathis.

FIND FIRST mathis1 WHERE mathis1.asset = asset NO-LOCK NO-ERROR. 
IF AVAILABLE mathis1 THEN 
DO: 
  FIND FIRST fa-artikel WHERE fa-artikel.nr = mathis1.nr NO-LOCK.
  IF fa-artikel.loeschflag = 0 THEN
  DO:
     ASSIGN avail-asset = YES
            mathis-name = mathis1.NAME.
  END.
END. 
