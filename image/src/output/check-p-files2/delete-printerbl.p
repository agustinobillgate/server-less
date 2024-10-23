
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER int1      AS INT.
DEF OUTPUT PARAMETER success-flag AS LOGICAL.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST printer WHERE printer.nr = int1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE printer THEN
        DO:
            DELETE printer.
            RELEASE printer.
            success-flag = YES.
        END.
    END.
END CASE.
