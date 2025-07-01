
DEF INPUT PARAMETER lief-nr AS INT.
DEF OUTPUT PARAMETER a-firma AS CHAR.
DEF OUTPUT PARAMETER avail-l-lieferant AS LOGICAL INIT NO.

FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK NO-ERROR. 
IF AVAILABLE l-lieferant THEN 
DO:
    a-firma = l-lieferant.firma.
    avail-l-lieferant = YES.
END.
