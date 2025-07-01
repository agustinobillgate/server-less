
DEFINE TEMP-TABLE p-list 
  FIELD bezeich AS CHAR FORMAT "x(16)" 
  FIELD zeit1 AS INTEGER FORMAT "9999" 
  FIELD zeit2 AS INTEGER FORMAT "9999" 
  FIELD shift AS INTEGER FORMAT "9   ". 

DEF INPUT PARAMETER TABLE FOR p-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST p-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE p-list THEN RETURN.

IF case-type = 1 THEN   /* add */
DO:
   create queasy. 
   RUN fill-new-queasy. 
END.
ELSE IF case-type = 2 THEN   /* chg */
DO:
   FIND FIRST queasy WHERE RECID(queasy) = rec-id.
   FIND CURRENT queasy EXCLUSIVE-LOCK. 
   queasy.char1 = p-list.bezeich. 
   queasy.number1 = p-list.zeit1. 
   queasy.number2 = p-list.zeit2. 
   queasy.number3 = p-list.shift.
   FIND CURRENT queasy NO-LOCK.
END.

PROCEDURE fill-new-queasy: 
  queasy.key = 5. 
  queasy.char1 = p-list.bezeich. 
  queasy.number1 = p-list.zeit1. 
  queasy.number2 = p-list.zeit2. 
  queasy.number3 = p-list.shift. 
END. 

