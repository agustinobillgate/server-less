
DEFINE TEMP-TABLE p-list 
  FIELD bezeich AS CHAR FORMAT "x(24)" 
  FIELD num AS INTEGER FORMAT ">>9". 

DEF INPUT PARAMETER TABLE FOR p-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST p-list.
IF case-type = 1 THEN   /*MT add */
DO :
    create queasy. 
    RUN fill-new-queasy.
END.
ELSE IF case-type = 1 THEN   /*MT chg */
DO:
    FIND FIRST queasy WHERE RECID(queasy) = rec-id.
    FIND CURRENT queasy EXCLUSIVE-LOCK. 
    queasy.char1 = p-list.bezeich.
    FIND CURRENT queasy NO-LOCK. 
END.


PROCEDURE fill-new-queasy: 
  queasy.key = 11. 
  queasy.number1 = p-list.num. 
  queasy.char1 = p-list.bezeich. 
END. 
