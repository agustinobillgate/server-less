

DEF TEMP-TABLE queasy-list LIKE queasy.

DEF INPUT  PARAMETER TABLE FOR queasy-list.
DEF INPUT  PARAMETER iCase AS INT.
DEF INPUT  PARAMETER recid-queasy AS INT.

FIND FIRST queasy-list.

IF iCase = 1 THEN
DO:
    create queasy. 
    RUN fill-new-queasy. 
END.
ELSE
DO:
    FIND FIRST queasy WHERE RECID(queasy) = recid-queasy EXCLUSIVE-LOCK.
    queasy.char3 = queasy-list.char3.
    FIND CURRENT queasy NO-LOCK.
END.

PROCEDURE fill-new-queasy: 
  queasy.key = 150. 
  queasy.char1 = queasy-list.char1. 
  queasy.char3 = queasy-list.char3. 
END. 


