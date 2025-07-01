
DEF INPUT  PARAMETER case-type  AS INTEGER.
DEF INPUT  PARAMETER int1       AS INTEGER.
DEF OUTPUT PARAMETER succesFlag AS LOGICAL INIT NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST fixleist WHERE RECID(fixleist) = int1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE fixleist THEN
        DO:
            DELETE fixleist.
            RELEASE fixleist.
            succesFlag = YES.
        END.
    END.
END CASE.
