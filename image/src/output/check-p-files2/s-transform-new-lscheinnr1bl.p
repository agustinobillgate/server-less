
DEF INPUT-OUTPUT PARAMETER lscheinnr AS CHAR.
DEF INPUT PARAMETER rec-id    AS INT.
DEF INPUT PARAMETER transdate AS DATE.
DEF INPUT PARAMETER req-str   AS CHAR.

DEFINE buffer l-ophdr1 FOR l-ophdr.
DEFINE VARIABLE i AS INTEGER INITIAL 1. 

FIND FIRST l-ophdr1 WHERE SUBSTR(l-ophdr1.lscheinnr,1,3) =  lscheinnr 
  AND l-ophdr1.op-typ = "STT" AND l-ophdr1.datum = transdate 
  NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE l-ophdr1: 
  i = i + 1. 
  lscheinnr = STRING(i, "999"). 
  FIND FIRST l-ophdr1 WHERE SUBSTR(l-ophdr1.lscheinnr,1,3) = lscheinnr 
    AND l-ophdr1.op-typ = "STT" AND l-ophdr1.datum = transdate 
    NO-LOCK NO-ERROR. 
END. 
lscheinnr = lscheinnr + "-" + req-str. 
FIND FIRST l-ophdr WHERE RECID(l-ophdr) = rec-id.
DO transaction: 
  FIND CURRENT l-ophdr EXCLUSIVE-LOCK. 
  l-ophdr.docu-nr = lscheinnr. 
  l-ophdr.lscheinnr = lscheinnr. 
  l-ophdr.op-typ = "STT". 
  FIND CURRENT l-ophdr NO-LOCK. 
END.
