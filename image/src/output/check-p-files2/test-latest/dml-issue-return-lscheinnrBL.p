
DEF INPUT PARAMETER lscheinnr AS CHAR.
DEF OUTPUT PARAMETER err-code AS LOGICAL INIT NO.

FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
    AND l-ophdr.op-typ = "STI" NO-LOCK NO-ERROR. 
IF AVAILABLE l-ophdr THEN err-code = YES.
