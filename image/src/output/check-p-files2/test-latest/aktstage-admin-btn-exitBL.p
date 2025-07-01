
DEF TEMP-TABLE stage-list LIKE akt-code. 

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER TABLE FOR stage-list.

FIND FIRST stage-list.
IF case-type = 1 THEN       /* add */
DO :
    create akt-code. 
    RUN fill-stage-code. 
END.
ELSE IF case-type = 2 THEN       /* chg */
DO:
    FIND FIRST akt-code WHERE RECID(akt-code) = rec-id.
    FIND CURRENT akt-code EXCLUSIVE-LOCK. 
    RUN fill-stage-code. 
    FIND CURRENT akt-code NO-LOCK. 
END.

PROCEDURE fill-stage-code: 
  akt-code.aktiongrup = 2.
  akt-code.aktionscode = stage-list.aktionscode. 
  akt-code.bezeich = stage-list.bezeich. 
  akt-code.bemerkung = stage-list.bemerkung. 
  akt-code.wertigkeit = stage-list.wertigkeit.
END. 
