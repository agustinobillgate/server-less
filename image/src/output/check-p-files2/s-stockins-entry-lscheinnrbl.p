
DEF INPUT  PARAMETER lief-nr  AS INT.
DEF INPUT  PARAMETER curr-lager AS INT.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.
DEF OUTPUT PARAMETER err-code1 AS INT INIT 0.
DEF OUTPUT PARAMETER lager-bezeich AS CHAR.
DEF OUTPUT PARAMETER a-firma AS CHAR.

FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-lieferant /* AND lief-nr NE 0 */ THEN 
DO: 
    err-code = 1.
    RETURN NO-APPLY. 
END. 
ELSE IF AVAILABLE l-lieferant THEN 
DO: 
    err-code = 2.
    a-firma = l-lieferant.firma.
END. 

FIND FIRST l-lager WHERE l-lager.lager-nr = curr-lager NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-lager THEN 
DO: 
    err-code1 = 1.
    RETURN NO-APPLY. 
END. 
ELSE 
DO: 
    err-code1 = 2.
    lager-bezeich = l-lager.bezeich. 
END. 
