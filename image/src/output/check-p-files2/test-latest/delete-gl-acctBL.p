
DEF INPUT PARAMETER case-type AS INTEGER.
DEF INPUT PARAMETER int1 AS INT.
DEF INPUT PARAMETER char1 AS CHAR.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = char1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        DO:
            DELETE gl-acct.
            RELEASE gl-acct.
            ASSIGN success-flag = YES.
        END.
    END.
END CASE.
