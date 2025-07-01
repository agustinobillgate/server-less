DEFINE TEMP-TABLE email-list LIKE queasy. 

DEF INPUT PARAMETER TABLE FOR email-list.
DEF INPUT PARAMETER iCase           AS INT.
DEF INPUT PARAMETER recid-queasy    AS INT.

FIND FIRST email-list.
IF iCase = 1 THEN
DO:
    create queasy. 
    RUN fill-new-email-setup. 
END.
ELSE
DO:
    FIND FIRST queasy WHERE RECID(queasy) = recid-queasy EXCLUSIVE-LOCK.
    queasy.char1 = email-list.char1. 
    queasy.char2 = email-list.char2. 
    FIND CURRENT queasy NO-LOCK.
END.

PROCEDURE fill-new-email-setup: 
  queasy.KEY = 138.
  queasy.number1 = email-list.number1. 
  queasy.char1 = email-list.char1.
  queasy.char2 = email-list.char2.
END. 
 

