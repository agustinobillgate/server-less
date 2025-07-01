
DEFINE TEMP-TABLE ba-list LIKE bk-setup. 

DEF INPUT  PARAMETER TABLE FOR ba-list.
DEF INPUT  PARAMETER iCase AS INT.
DEF INPUT  PARAMETER recid-bk-setup AS INT.

FIND FIRST ba-list NO-LOCK NO-ERROR.
IF iCase = 1 THEN
DO:
    CREATE bk-setup. 
    RUN fill-new-bk-setup. 
    RELEASE bk-setup.
END.
ELSE
DO:
    /*FIND FIRST bk-setup WHERE RECID(bk-setup) = recid-bk-setup
        EXCLUSIVE-LOCK.
    bk-setup.bezeich = ba-list.bezeich.
    FIND CURRENT bk-setup NO-LOCK.*/

    /*Alder - Serverless - Issue 829 - Start*/
    FIND FIRST bk-setup WHERE RECID(bk-setup) EQ recid-bk-setup NO-LOCK NO-ERROR.
    IF AVAILABLE bk-setup THEN
    DO:
        FIND CURRENT bk-setup EXCLUSIVE-LOCK.
        ASSIGN bk-setup.bezeichnung = ba-list.bezeichnung.
        FIND CURRENT bk-setup NO-LOCK.
        RELEASE bk-setup.
    END.
    /*Alder - Serverless - Issue 829 - End*/
END.


PROCEDURE fill-new-bk-setup: 
    bk-setup.setup-id = ba-list.setup-id. 
    bk-setup.bezeichnung = ba-list.bezeichnung. /*Alder - Serverless - Issue 829*/ /*bezeich -> bezeichnung*/
END. 
