DEFINE INPUT PARAMETER billdate AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER s        AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER lscheinnr AS CHAR NO-UNDO.

DEFINE VARIABLE i         AS INTEGER INITIAL 1. 

s = "FA" + SUBSTR(STRING(year(billdate)),3,2) + STRING(month(billdate), "99") 
     + STRING(day(billdate), "99"). 
lscheinnr = s + STRING(i, "999").

FIND FIRST fa-op WHERE fa-op.datum =  billdate 
    AND SUBSTR(fa-op.lscheinnr, 1, 11) = lscheinnr NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE fa-op: 
    i = i + 1. 
    lscheinnr = s + STRING(i, "999"). 
    FIND FIRST fa-op WHERE fa-op.datum =  billdate 
      AND SUBSTR(fa-op.lscheinnr, 1, 11) = lscheinnr NO-LOCK NO-ERROR.
END.
