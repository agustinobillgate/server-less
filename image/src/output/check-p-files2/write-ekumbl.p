DEF TEMP-TABLE t-ekum LIKE ekum.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER TABLE FOR t-ekum.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-ekum NO-ERROR.
IF NOT AVAILABLE t-ekum THEN RETURN.

CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE ekum.
        BUFFER-COPY t-ekum TO ekum.
        RELEASE ekum.
        success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST ekum WHERE ekum.eknr = t-ekum.eknr 
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE ekum THEN
        DO:
            BUFFER-COPY t-ekum TO ekum.
            RELEASE ekum.
            success-flag = YES.
        END.
    END.
END CASE.
