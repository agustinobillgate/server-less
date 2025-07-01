DEF INPUT-OUTPUT PARAMETER lscheinnr AS CHAR.
DEF INPUT PARAMETER billdate AS DATE.
DEF INPUT PARAMETER s        AS CHAR.

DEF VAR i AS INTEGER NO-UNDO.

/* DEFINE buffer l-ophdr1 FOR l-ophdr. */

/* FIND FIRST l-ophdr1 WHERE l-ophdr1.datum =  billdate 
AND l-ophdr1.op-typ = "STI" 
AND SUBSTR(l-ophdr1.lscheinnr, 1, 10) = lscheinnr NO-LOCK NO-ERROR. 

DO WHILE AVAILABLE l-ophdr1: 
    i = i + 1. 
    lscheinnr = s + STRING(i, "999"). 

    FIND FIRST l-ophdr1 WHERE l-ophdr1.datum = billdate 
    AND l-ophdr1.op-typ = "STI" 
    AND SUBSTR(l-ophdr1.lscheinnr, 1, 10) = lscheinnr NO-LOCK NO-ERROR.
END. */

FOR EACH l-ophdr WHERE l-ophdr.datum EQ billdate 
AND l-ophdr.op-typ EQ "STI" 
AND SUBSTR(l-ophdr.lscheinnr, 1, 7) EQ s
NO-LOCK BY l-ophdr.lscheinnr DESCENDING:
    lscheinnr = s + STRING(INT(SUBSTR(l-ophdr.lscheinnr, 8, 3)) + 1, "999").
    LEAVE.
END.

IF NOT AVAILABLE l-ophdr THEN 
    lscheinnr = s + STRING(1, "999").

