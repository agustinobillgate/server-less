
DEF INPUT PARAMETER lief-nr AS INT.
DEF OUTPUT PARAMETER err-flag AS INT INIT 0.
DEF OUTPUT PARAMETER lief-bezeich AS CHAR.

FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-lieferant /* AND lief-nr NE 0 */ THEN 
DO: 
    err-flag = 1.
    RETURN NO-APPLY. 
END. 
ELSE IF AVAILABLE l-lieferant THEN 
DO: 
    err-flag = 2.
    lief-bezeich = l-lieferant.firma.
END. 
