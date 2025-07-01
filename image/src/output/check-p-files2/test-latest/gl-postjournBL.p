
DEF INPUT PARAMETER refno AS CHAR.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.
DEF OUTPUT PARAMETER datum AS DATE.
DEF OUTPUT PARAMETER bezeich AS CHAR.

DEFINE BUFFER gbuff FOR gl-jouhdr. 

FIND FIRST gbuff WHERE gbuff.refno = refno NO-LOCK NO-ERROR. 
IF AVAILABLE gbuff THEN 
DO: 
    fl-code = 1.
    datum = gbuff.datum.
    bezeich = gbuff.bezeich.
END. 
