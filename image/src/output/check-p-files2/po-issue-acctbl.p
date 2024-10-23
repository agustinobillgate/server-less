DEFINE INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER cost-acct AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER docu-nr   AS CHAR    NO-UNDO. 
DEFINE INPUT PARAMETER lief-nr   AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER created   AS LOGICAL NO-UNDO.

DEFINE OUTPUT PARAMETER fl-code       AS INTEGER NO-UNDO INIT 0.
DEFINE OUTPUT PARAMETER avail-gl-acct AS LOGICAL NO-UNDO INIT NO.
    
IF case-type = 1 THEN
DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = cost-acct NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE gl-acct THEN 
    DO: 
        fl-code = 1.
        RETURN NO-APPLY. 
    END. 
    
    IF NOT created THEN
    DO:
          FIND FIRST l-op WHERE l-op.op-art = 1 AND l-op.loeschflag LE 1
            AND l-op.lscheinnr = lscheinnr AND l-op.docu-nr NE docu-nr
            NO-LOCK NO-ERROR.
          IF AVAILABLE l-op THEN
          DO:
            fl-code = 3.
            RETURN NO-APPLY. 
          END.
    END.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = cost-acct NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE gl-acct THEN DO:
        avail-gl-acct = NO.
        RETURN NO-APPLY.
    END.
    ELSE avail-gl-acct = YES.
END.
