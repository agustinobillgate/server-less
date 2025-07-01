
DEF INPUT PARAMETER lscheinnr AS CHAR.
DEF INPUT PARAMETER docu-nr AS CHAR.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.

FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
    AND l-ophdr.op-typ = "STI" AND l-ophdr.docu-nr = docu-nr 
    NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-ophdr THEN 
DO: 
    err-code  = 1.
    RETURN NO-APPLY. 
END. 
