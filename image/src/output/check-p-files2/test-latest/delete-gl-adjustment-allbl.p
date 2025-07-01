DEFINE INPUT PARAMETER refno    AS CHARACTER.
DEFINE INPUT PARAMETER jnr      AS INTEGER.
DEFINE INPUT PARAMETER bezeich  AS CHARACTER.
DEFINE INPUT PARAMETER user-init AS CHARACTER.
DEFINE INPUT PARAMETER to-date  AS DATE.
DEFINE OUTPUT PARAMETER flag    AS LOGICAL.
DEFINE OUTPUT PARAMETER msg     AS CHARACTER.

DEFINE VARIABLE close-year AS DATE NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr EQ 795 NO-LOCK NO-ERROR.
ASSIGN close-year = htparam.fdate.

FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr EQ jnr NO-LOCK NO-ERROR.
IF AVAILABLE gl-jouhdr THEN
DO:    
    IF gl-jouhdr.activeflag EQ 0 AND gl-jouhdr.jtype EQ 0 THEN
    DO:        
        IF gl-jouhdr.datum EQ to-date THEN
        DO:
            FOR EACH gl-journal WHERE gl-journal.jnr EQ gl-jouhdr.jnr:
                DELETE gl-journal.
            END.
            FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK.
            DELETE gl-jouhdr.
            ASSIGN flag = YES.
        END.
        ELSE
        DO:
            ASSIGN flag = NO.
            msg = "Wrong Year Closing Date.".
            RETURN.
        END.        
    END.       
END.

FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN
DO:
    CREATE res-history. 
    ASSIGN 
        res-history.nr          = bediener.nr     
        res-history.datum       = TODAY 
        res-history.zeit        = TIME 
        res-history.aenderung   = "Deleted Last Year Adjustment With Reference No: " 
                                + refno + "|Desc: " + bezeich + "|By:" + bediener.username    
        res-history.action      = "JournalTransactionDelete".
    FIND CURRENT res-history NO-LOCK.
    RELEASE res-history.
END.

