DEF TEMP-TABLE t-brief LIKE brief.

DEF INPUT PARAMETER case-type AS INT NO-UNDO.
DEF INPUT PARAMETER TABLE FOR t-brief.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-brief NO-ERROR.
IF NOT AVAILABLE t-brief THEN RETURN.

CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE brief.
        BUFFER-COPY t-brief TO brief.
        RELEASE brief.
        success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST brief WHERE brief.briefnr = t-brief.briefnr
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE brief THEN
        DO:
            BUFFER-COPY t-brief TO brief.
            RELEASE brief.
            success-flag = YES.
        END.
    END.
END CASE.
