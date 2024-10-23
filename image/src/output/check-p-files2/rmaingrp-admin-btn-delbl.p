
DEF INPUT PARAMETER wgrpgen-eknr AS INT.
DEF OUTPUT PARAMETER flag AS INT INIT 0.

FIND FIRST artikel WHERE artikel.endkum = wgrpgen-eknr NO-LOCK NO-ERROR. 
IF AVAILABLE artikel THEN 
DO: 
    flag = 1.
END. 
ELSE 
DO:
  FIND FIRST wgrpgen WHERE wgrpgen.eknr = wgrpgen-eknr.
  FIND CURRENT wgrpgen EXCLUSIVE-LOCK. 
  delete wgrpgen. 
END.
