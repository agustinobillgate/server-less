
DEF INPUT PARAMETER case-type   AS INT.
DEF INPUT PARAMETER int1        AS INT.
DEF INPUT PARAMETER int2        AS INT.
DEF INPUT PARAMETER char1       AS CHAR.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST bediener WHERE bediener.nr = int1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            DELETE bediener.
            RELEASE bediener.
            ASSIGN success-flag = YES.
        END.
    END.
END CASE.
