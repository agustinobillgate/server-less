
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER err AS INT INIT 0.

/*
FIND FIRST akt-code WHERE RECID(akt-code) = rec-id.
FIND FIRST akthdr WHERE akthdr.product[1] = akt-code.aktionscode OR akthdr.product[3] = akt-code.aktionscode
   OR akthdr.product[3] = akt-code.aktionscode NO-LOCK NO-ERROR. 
IF AVAILABLE akthdr THEN err = 1.
ELSE 
DO: 
    FIND CURRENT akt-code EXCLUSIVE-LOCK. 
    delete akt-code.
END. 
*/

/*Alder - Serverless - Issue 780 - Start*/
FIND FIRST akt-code WHERE RECID(akt-code) EQ rec-id NO-LOCK NO-ERROR.
IF AVAILABLE akt-code THEN
DO :
    FIND FIRST akthdr WHERE akthdr.product[1] EQ akt-code.aktionscode
        OR akthdr.product[2] EQ akt-code.aktionscode
        OR akthdr.product[3] EQ akt-code.aktionscode
        NO-LOCK NO-ERROR.
    IF AVAILABLE akthdr THEN
    DO:
        ASSIGN err = 1.
    END.
    ELSE
    DO:
        FIND CURRENT akt-code EXCLUSIVE-LOCK.
        DELETE akt-code.
        RELEASE akt-code.
    END.
END.
/*Alder - Serverless - Issue 780 - End*/
