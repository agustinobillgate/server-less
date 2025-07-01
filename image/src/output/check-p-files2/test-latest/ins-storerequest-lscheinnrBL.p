
DEF INPUT  PARAMETER casetype   AS INT.
DEF INPUT  PARAMETER lscheinnr  AS CHAR.
DEF OUTPUT PARAMETER err        AS INT INIT 0.

FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
    AND l-ophdr.op-typ = "REQ" NO-LOCK NO-ERROR. 

IF casetype = 1 THEN
DO :
    FIND CURRENT l-ophdr EXCLUSIVE-LOCK. 
    l-ophdr.docu-nr = lscheinnr. 
    l-ophdr.lscheinnr = lscheinnr. 
    FIND CURRENT l-ophdr NO-LOCK.
END.
ELSE IF casetype = 2 THEN
DO:
    IF AVAILABLE l-ophdr THEN 
    DO: 
      err = 1.
      RETURN NO-APPLY. 
    END. 
END.
