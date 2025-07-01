define TEMP-TABLE category like queasy.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id    AS INT.
DEF INPUT PARAMETER TABLE FOR category.

FIND FIRST category.
IF case-type = 1 THEN
DO :
    CREATE  queasy.
    RUN fill-new-queasy.
END.
ELSE IF case-type = 2 THEN
DO :
    FIND FIRST queasy WHERE RECID(queasy) = rec-id.
    FIND CURRENT queasy EXCLUSIVE-LOCK. 
    queasy.number1 = category.number1.
    queasy.char1 = category.char1.  
    FIND CURRENT queasy NO-LOCK .  
END.

PROCEDURE fill-new-queasy:  
  queasy.KEY = 132.  
  queasy.number1 = category.number1.  
  queasy.char1 = category.char1.  
END.  

