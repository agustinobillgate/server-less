
DEF INPUT PARAMETER lief-nr AS INT.
DEF OUTPUT PARAMETER lief-bezeich AS CHAR.
DEF OUTPUT PARAMETER avail-lieferant AS LOGICAL INIT NO.

FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-lieferant /* AND lief-nr NE 0 */ THEN 
DO: 
    RETURN NO-APPLY. 
END. 
ELSE IF AVAILABLE l-lieferant THEN 
DO: 
    lief-bezeich = l-lieferant.firma.
    avail-lieferant = YES.
END. 
