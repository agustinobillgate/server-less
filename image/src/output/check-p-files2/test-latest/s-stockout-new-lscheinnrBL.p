
DEFINE buffer l-ophdr1 FOR l-ophdr. 
DEFINE buffer l-ophdr2 FOR l-ophdr. 

DEF INPUT-OUTPUT PARAMETER lscheinnr AS CHAR.
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER transdate AS DATE.
DEF INPUT PARAMETER req-str AS CHAR.
DEF INPUT PARAMETER s AS CHAR.
DEF VAR i AS INT.
DEF VAR j AS INT.

FIND FIRST l-ophdr WHERE RECID(l-ophdr) = rec-id.

IF case-type = 1 THEN
DO:
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
    DO TRANSACTION: 
      FIND CURRENT l-ophdr EXCLUSIVE-LOCK. 
      l-ophdr.docu-nr = lscheinnr. 
      l-ophdr.lscheinnr = lscheinnr. 
      l-ophdr.op-typ = "STT". 
      FIND CURRENT l-ophdr NO-LOCK. 
    END. 
END.
ELSE IF case-type = 2 THEN
DO: 
    FIND FIRST l-ophdr1 WHERE l-ophdr1.lscheinnr =  lscheinnr 
      AND l-ophdr1.op-typ = "STT" NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE l-ophdr1: 
          i = i + 1. 
      lscheinnr = s + STRING(i, "999"). 
      FIND FIRST l-ophdr1 WHERE l-ophdr1.lscheinnr = lscheinnr 
        AND l-ophdr1.op-typ = "STT" NO-LOCK NO-ERROR. 
    END. 
    FIND LAST l-ophdr2 WHERE SUBSTR(l-ophdr2.lscheinnr,1,7) = s 
      AND l-ophdr2.op-typ = "STT" NO-LOCK NO-ERROR.
    IF AVAILABLE l-ophdr2 THEN
    DO:
      j = INT(SUBSTR(l-ophdr2.lscheinnr,LENGTH(l-ophdr2.lscheinnr) - 2)) + 1.
      IF RECID(l-ophdr2) NE RECID(l-ophdr1) THEN lscheinnr = s + STRING(j, "999").
    END.                                                                          
    DO TRANSACTION: 
      FIND CURRENT l-ophdr EXCLUSIVE-LOCK. 
      l-ophdr.docu-nr = lscheinnr. 
      l-ophdr.lscheinnr = lscheinnr. 
      l-ophdr.op-typ = "STT". 
      FIND CURRENT l-ophdr NO-LOCK. 
    END.
END.
