
DEF INPUT PARAMETER h-recid AS INT.
DEF INPUT PARAMETER invoice-nr AS CHAR.

FIND FIRST l-ophdr WHERE RECID(l-ophdr) = h-recid EXCLUSIVE-LOCK. 
IF AVAILABLE l-ophdr THEN
DO:
    l-ophdr.fibukonto = TRIM(invoice-nr). 
    FIND CURRENT l-ophdr NO-LOCK. 
END.
