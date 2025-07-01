DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER t-raum AS CHAR.
DEF OUTPUT PARAMETER err AS INT INIT 0.

FIND FIRST bk-rset WHERE bk-rset.raum = t-raum NO-LOCK NO-ERROR. 
IF AVAILABLE bk-rset THEN 
DO: 
    err = 1.
    RETURN NO-APPLY. 
END.

/*Alder - Serverless - Issue 778 - Start*/
FIND FIRST bk-raum WHERE RECID(bk-raum) EQ rec-id NO-LOCK NO-ERROR.
IF AVAILABLE bk-raum THEN
DO:
    FIND CURRENT bk-raum EXCLUSIVE-LOCK.
    DELETE bk-raum.
    RELEASE bk-raum.
END.
/*Alder - Serverless - Issue 778 - End*/

