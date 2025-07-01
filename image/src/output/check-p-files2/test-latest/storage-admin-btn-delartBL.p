
DEF INPUT  PARAMETER lager-nr AS INT.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.

FIND FIRST l-lager WHERE l-lager.lager-nr = lager-nr.

FIND FIRST l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr 
  NO-LOCK NO-ERROR.
IF AVAILABLE l-bestand THEN err-code = 1.
ELSE 
DO: 
    FIND CURRENT l-lager EXCLUSIVE-LOCK.
    delete l-lager.
END.
