
DEFINE TEMP-TABLE p-list
  FIELD bezeich AS CHAR FORMAT "x(30)" 
  FIELD code AS CHAR FORMAT "x(2)" 
  FIELD num AS INTEGER FORMAT ">>9"
  FIELD usr-init AS CHAR FORMAT "x(6)". 

DEF INPUT PARAMETER TABLE FOR p-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER t-recid AS INT INIT 0.

FIND FIRST p-list.
IF case-type = 1 THEN   /*MT add */
DO :
    create queasy. 
    RUN fill-new-queasy.
    FIND CURRENT queasy.
    t-recid = RECID(queasy).
END.
ELSE IF case-type = 2 THEN   /*MT chg */
DO:
    FIND FIRST queasy WHERE RECID(queasy) = rec-id.
    FIND CURRENT queasy EXCLUSIVE-LOCK. 
    queasy.char1 = p-list.code. 
    queasy.char2 = p-list.bezeich.
    queasy.char3 = p-list.usr-init.
    FIND CURRENT queasy NO-LOCK.
END.

PROCEDURE fill-new-queasy: 
  queasy.key = 10. 
  queasy.number1 = p-list.num. 
  queasy.char1 = p-list.code. 
  queasy.char2 = p-list.bezeich.
  queasy.char3 = p-list.usr-init.
END. 

