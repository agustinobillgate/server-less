
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER int1      AS INT.
DEF INPUT PARAMETER int2      AS INT.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH argt-line WHERE argt-line.argtnr = int1: 
            delete argt-line. 
        END. 
        FIND FIRST arrangement WHERE arrangement.argtnr = int1 
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN
        DO:
            DELETE arrangement.
            success-flag = YES.
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH argt-line WHERE argt-line.argtnr = int1: 
            delete argt-line. 
        END. 
        FIND FIRST arrangement WHERE RECID(arrangement) = int2
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN
        DO:
            DELETE arrangement.
            success-flag = YES.
        END.
    END.
END CASE.
