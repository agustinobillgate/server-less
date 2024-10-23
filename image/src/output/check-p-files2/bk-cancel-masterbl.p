DEFINE INPUT PARAMETER blockId          AS CHARACTER.
DEFINE INPUT PARAMETER cancelReason     AS CHARACTER.
DEFINE INPUT PARAMETER cancelComments   AS CHARACTER.
DEFINE INPUT PARAMETER cancelPenalty    AS DECIMAL.

FIND FIRST bk-master WHERE bk-master.block-id EQ blockId EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN
DO:
    FIND FIRST bk-queasy WHERE bk-queasy.key EQ 1
        AND bk-queasy.number2 EQ 7 NO-LOCK NO-ERROR.
    IF AVAILABLE bk-queasy THEN
    DO:
        ASSIGN 
            cancel-flag     = YES
            cancel-reason   = cancelReason + "|" + cancelComments
            cancel-penalty  = cancelPenalty
            bk-master.resstatus = bk-queasy.number1.
    END.    
    
    RELEASE bk-master.           
END.
