
DEF INPUT PARAMETER case-type     AS INT.
DEF INPUT PARAMETER int1          AS INT.
DEF INPUT PARAMETER int2          AS INT.
DEF INPUT PARAMETER date1         AS DATE.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST budget WHERE budget.artnr = int1 AND budget.departement = int2
            AND budget.datum = date1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE budget THEN
        DO:
            DELETE budget.
            RELEASE budget.
            ASSIGN success-flag = YES.
        END.
    END.
END CASE.
