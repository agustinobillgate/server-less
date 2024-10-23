
DEFINE TEMP-TABLE akt-code-list LIKE akt-code. 

DEF INPUT PARAMETER TABLE FOR akt-code-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT  PARAMETER recid-akt-code         AS INT.

FIND FIRST akt-code-list.
IF case-type = 1 THEN
DO :
    create akt-code. 
    RUN fill-akt-code. 
END.
ELSE
DO:
    FIND FIRST akt-code WHERE RECID(akt-code) = recid-akt-code NO-LOCK.
    FIND CURRENT akt-code EXCLUSIVE-LOCK. 
    RUN fill-akt-code. 
END.

PROCEDURE fill-akt-code: 
  akt-code.aktiongrup = 1.
  akt-code.aktionscode = akt-code-list.aktionscode. 
  akt-code.bezeich = akt-code-list.bezeich. 
  akt-code.bemerkung = akt-code-list.bemerkung. 
END. 
