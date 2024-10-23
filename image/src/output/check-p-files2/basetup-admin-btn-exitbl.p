
DEFINE TEMP-TABLE ba-list LIKE bk-setup. 

DEF INPUT  PARAMETER TABLE FOR ba-list.
DEF INPUT  PARAMETER iCase AS INT.
DEF INPUT  PARAMETER recid-bk-setup AS INT.

FIND FIRST ba-list NO-LOCK.
IF iCase = 1 THEN
DO:
    create bk-setup. 
    RUN fill-new-bk-setup. 
END.
ELSE
DO:
    FIND FIRST bk-setup WHERE RECID(bk-setup) = recid-bk-setup
        EXCLUSIVE-LOCK.
    bk-setup.bezeich = ba-list.bezeich.
    FIND CURRENT bk-setup NO-LOCK. 
END.


PROCEDURE fill-new-bk-setup: 
  bk-setup.setup-id = ba-list.setup-id. 
  bk-setup.bezeich = ba-list.bezeich. 
END. 
