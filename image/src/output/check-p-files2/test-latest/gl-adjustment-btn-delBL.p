
DEF INPUT  PARAMETER jnr          AS INT.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST gl-journal WHERE gl-journal.jnr = jnr NO-LOCK NO-ERROR. 
IF AVAILABLE gl-journal THEN 
    RETURN NO-APPLY. 
ELSE
DO:
    FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = jnr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE gl-jouhdr THEN
    DO:
        delete gl-jouhdr.
        success-flag = YES.
    END.
END.
