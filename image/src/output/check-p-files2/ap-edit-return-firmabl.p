
DEF INPUT  PARAMETER firma   AS CHAR.
DEF OUTPUT PARAMETER lief-nr AS INT.
DEF OUTPUT PARAMETER fl-temp AS INT INIT 0.

FIND FIRST l-lieferant WHERE l-lieferant.firma = firma NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-lieferant THEN 
DO: 
    fl-temp = 1.
    RETURN NO-APPLY. 
END. 
lief-nr = l-lieferant.lief-nr. 
fl-temp = 0.
