
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER lname AS CHAR.
DEF INPUT PARAMETER liefNo AS INT.
DEF OUTPUT PARAMETER a-firma AS CHAR.
DEF OUTPUT PARAMETER l-supp-lief-nr AS INT.
DEF OUTPUT PARAMETER avail-l-supp AS LOGICAL INIT NO.

DEFINE buffer l-supp FOR l-lieferant. 
IF case-type = 1 THEN
    FIND FIRST l-supp WHERE l-supp.firma = lname NO-LOCK NO-ERROR.
ELSE IF case-type = 2 THEN
    FIND FIRST l-supp WHERE l-supp.lief-nr = liefNo NO-LOCK.

IF AVAILABLE l-supp THEN 
DO:
    a-firma = l-supp.firma.
    avail-l-supp = YES.
    l-supp-lief-nr = l-supp.lief-nr.
END.
