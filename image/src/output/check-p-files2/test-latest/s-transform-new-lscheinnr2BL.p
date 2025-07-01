
DEF INPUT-OUTPUT PARAMETER lscheinnr AS CHAR.
DEF INPUT PARAMETER rec-id    AS INT.
DEF INPUT PARAMETER transdate AS DATE.
DEF INPUT PARAMETER req-str   AS CHAR.
DEF INPUT PARAMETER s         AS CHAR.

DEFINE VARIABLE i AS INTEGER INITIAL 1.
DEFINE buffer l-ophdr1 FOR l-ophdr.

FIND FIRST l-ophdr1 WHERE l-ophdr1.lscheinnr =  lscheinnr 
  AND l-ophdr1.op-typ = "STT" NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE l-ophdr1: 
  i = i + 1. 
  lscheinnr = s + STRING(i, "999"). 
  FIND FIRST l-ophdr1 WHERE l-ophdr1.lscheinnr = lscheinnr 
    AND l-ophdr1.op-typ = "STT" NO-LOCK NO-ERROR. 
END.
FIND FIRST l-ophdr WHERE RECID(l-ophdr) = rec-id.
DO transaction: 
  FIND CURRENT l-ophdr EXCLUSIVE-LOCK. 
  l-ophdr.docu-nr = lscheinnr. 
  l-ophdr.lscheinnr = lscheinnr. 
  l-ophdr.op-typ = "STT". 
  FIND CURRENT l-ophdr NO-LOCK. 
END.
