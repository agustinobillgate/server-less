DEFINE INPUT-OUTPUT PARAMETER lscheinnr AS CHARACTER.
DEFINE INPUT PARAMETER s AS CHARACTER.
DEFINE INPUT PARAMETER recid-l-ophdr AS INTEGER.

DEFINE buffer l-ophdr1 FOR l-ophdr. 

DEFINE VARIABLE i AS INTEGER INITIAL 1.

/*
FIND FIRST l-ophdr WHERE RECID(l-ophdr) = recid-l-ophdr.

FIND FIRST l-ophdr1 WHERE l-ophdr1.lscheinnr = lscheinnr 
  AND l-ophdr1.op-typ = "REQ" NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE l-ophdr1: 
  i = i + 1. 
  lscheinnr = s + STRING(i, "999"). 
  FIND FIRST l-ophdr1 WHERE l-ophdr1.lscheinnr = lscheinnr 
    AND l-ophdr1.op-typ = "REQ" NO-LOCK NO-ERROR. 
END. 
DO TRANSACTION: 
  FIND CURRENT l-ophdr EXCLUSIVE-LOCK. 
  ASSIGN
    l-ophdr.docu-nr   = lscheinnr 
    l-ophdr.lscheinnr = lscheinnr 
    l-ophdr.op-typ    = "REQ"
  . 
  FIND CURRENT l-ophdr NO-LOCK.

END. 
*/

/*Alder - Serverless - Issue 564 - Start*/
FIND FIRST l-ophdr WHERE RECID(l-ophdr) = recid-l-ophdr NO-LOCK NO-ERROR.

FIND FIRST l-ophdr1 WHERE l-ophdr1.lscheinnr = lscheinnr AND l-ophdr1.op-typ = "REQ" NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE l-ophdr1: 
    i = i + 1. 
    lscheinnr = s + STRING(i, "999"). 
    FIND FIRST l-ophdr1 WHERE l-ophdr1.lscheinnr = lscheinnr AND l-ophdr1.op-typ = "REQ" NO-LOCK NO-ERROR.
END.

DO TRANSACTION: 
    IF AVAILABLE l-ophdr THEN
    DO:
        FIND CURRENT l-ophdr EXCLUSIVE-LOCK. 
        ASSIGN
            l-ophdr.docu-nr   = lscheinnr 
            l-ophdr.lscheinnr = lscheinnr 
            l-ophdr.op-typ    = "REQ". 
        FIND CURRENT l-ophdr NO-LOCK.
        RELEASE l-ophdr.
    END.
END.
/*Alder - Serverless - Issue 564 - End*/
