DEF TEMP-TABLE akt-code-list LIKE akt-code. 

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER TABLE FOR akt-code-list.

FIND FIRST akt-code-list.
IF case-type = 1 THEN       /* add */
DO :
    create akt-code. 
    RUN fill-akt-code. 
END.
ELSE IF case-type = 2 THEN       /* chg */
DO:
    FIND FIRST akt-code WHERE RECID(akt-code) = rec-id.
    FIND CURRENT akt-code EXCLUSIVE-LOCK. 
    RUN fill-akt-code. 
    FIND CURRENT akt-code NO-LOCK. 
END.

PROCEDURE fill-akt-code: 
  akt-code.aktiongrup = 5.
  akt-code.aktionscode = akt-code-list.aktionscode. 
  akt-code.bezeich = akt-code-list.bezeich. 
  akt-code.bemerkung = akt-code-list.bemerkung. 
END. 
