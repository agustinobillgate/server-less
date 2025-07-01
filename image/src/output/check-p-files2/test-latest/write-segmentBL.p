DEF TEMP-TABLE t-segment LIKE segment.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER TABLE FOR t-segment.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-segment NO-ERROR.
IF NOT AVAILABLE t-segment THEN RETURN.

CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE segment.
        BUFFER-COPY t-segment TO segment.
        RELEASE segment.
        success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST segment WHERE segment.segmentcode = t-segment.segmentcode
            EXCLUSIVE-LOCK.
        IF AVAILABLE segment THEN
        DO:
            BUFFER-COPY t-segment TO segment.
            RELEASE segment.
            success-flag = YES.
        END.
    END.
END CASE.
