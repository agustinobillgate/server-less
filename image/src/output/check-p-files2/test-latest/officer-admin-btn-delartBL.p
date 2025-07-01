
DEF INPUT  PARAMETER rec-id   AS INT.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.

/*Alder - Serverless - Issue 808 - Start*/
FIND FIRST queasy WHERE RECID(queasy) EQ rec-id NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FIND FIRST nation WHERE nation.untergruppe EQ queasy.number3 NO-LOCK NO-ERROR. 
    IF AVAILABLE nation THEN 
    DO: 
        err-code = 1.
        RETURN NO-APPLY. 
    END. 
    DO: 
        FIND CURRENT queasy EXCLUSIVE-LOCK. 
        DELETE queasy.
        RELEASE queasy.
    END.
END.
/*Alder - Serverless - Issue 808 - End*/
