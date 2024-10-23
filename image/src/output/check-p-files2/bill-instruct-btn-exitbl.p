DEF TEMP-TABLE t-queasy LIKE queasy.

DEF INPUT  PARAMETER TABLE FOR t-queasy.
DEF INPUT  PARAMETER case-type    AS INTEGER.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-queasy.
IF case-type = 1 THEN   /* add */
DO:
    create queasy.
    RUN fill-new-queasy.
    success-flag = YES.
END.
ELSE IF case-type = 2 THEN   /* chg */
DO:
    FIND FIRST queasy WHERE queasy.KEY = 9 
        AND queasy.number1 = t-queasy.number1 EXCLUSIVE-LOCK.
    IF AVAILABLE queasy THEN
    DO:
        queasy.char1 = t-queasy.char1. 
        queasy.logi1 = t-queasy.logi1.
        FIND CURRENT queasy NO-LOCK.
        success-flag = YES.
    END.
END.


PROCEDURE fill-new-queasy: 
  queasy.key = 9. 
  queasy.number1 = t-queasy.number1. 
  queasy.char1 = t-queasy.char1. 
  queasy.logi1 = t-queasy.logi1. 
END. 

