
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER int1      AS INT.
DEF INPUT PARAMETER char1     AS CHAR.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST ekum WHERE ekum.eknr = int1 AND ekum.bezeich EQ char1
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE ekum THEN
        DO:
            DELETE ekum.
            RELEASE ekum.
            success-flag = YES.
        END.
    END.
END CASE.
