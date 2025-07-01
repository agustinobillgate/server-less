
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER htlname-number AS INT.
DEF OUTPUT PARAMETER err-flag AS INT INIT 0.

DEF BUFFER hist FOR history.
    
FIND FIRST queasy WHERE RECID(queasy) = rec-id.
FIND FIRST hist WHERE hist.guestnrcom = htlname-number NO-LOCK NO-ERROR.
IF AVAILABLE hist THEN
DO:
    err-flag = 1.
    RETURN NO-APPLY.  
END.
ELSE
DO:  
    FIND CURRENT queasy EXCLUSIVE-LOCK.  
    DELETE queasy.  
END.
