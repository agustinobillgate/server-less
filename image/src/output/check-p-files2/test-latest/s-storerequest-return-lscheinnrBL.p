
DEF INPUT PARAMETER lscheinnr AS CHAR.
DEF OUTPUT PARAMETER avail-l-ophdr AS LOGICAL INIT NO.

FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
  AND l-ophdr.op-typ = "REQ" NO-LOCK NO-ERROR.
IF AVAILABLE l-ophdr THEN avail-l-ophdr = YES.
