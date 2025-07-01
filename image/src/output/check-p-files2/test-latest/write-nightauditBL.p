DEF TEMP-TABLE t-nightaudit LIKE nightaudit
    FIELD n-recid AS INT.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER TABLE FOR t-nightaudit.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-nightaudit NO-ERROR.
IF NOT AVAILABLE t-nightaudit THEN RETURN.
CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE nightaudit.
        BUFFER-COPY t-nightaudit TO nightaudit.
        RELEASE nightaudit.
        success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST nightaudit WHERE RECID(nightaudit) = t-nightaudit.n-recid
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE nightaudit THEN
        DO:
            BUFFER-COPY t-nightaudit TO nightaudit.
            RELEASE nightaudit.
            success-flag = YES.
        END.
    END.
END CASE.
