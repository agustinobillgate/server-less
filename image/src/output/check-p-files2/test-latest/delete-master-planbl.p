DEFINE INPUT PARAMETER resnr        AS INTEGER.
DEFINE INPUT PARAMETER user-init    AS CHARACTER.
DEFINE OUTPUT PARAMETER successFlag AS LOGICAL.

DEFINE VARIABLE blockId             AS CHARACTER    NO-UNDO.

FIND FIRST bk-master WHERE bk-master.resnr EQ resnr EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN 
DO:
    blockId     = bk-master.block-id.
    ASSIGN 
        bk-master.cancel-flag[1] = YES.
    
    RELEASE bk-master.
    
    successFlag = YES.    
END.
ELSE 
DO:
    successFlag = NO.
END.

FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN 
DO:
    CREATE res-history.
    ASSIGN 
        res-history.nr          = bediener.nr
        res-history.datum       = TODAY        
        res-history.zeit        = TIME
        res-history.action      = "Banquet"
        res-history.aenderung   = "Delete Master Plan With Block ID " + blockId.
END.


