DEF TEMP-TABLE t-nebenst LIKE nebenst
    FIELD n-id AS INT.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER TABLE FOR t-nebenst.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-nebenst NO-ERROR.
IF NOT AVAILABLE t-nebenst THEN RETURN.
CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE nebenst.
        BUFFER-COPY t-nebenst TO nebenst.
        RELEASE nebenst.
        success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST nebenst WHERE RECID(nebenst) = t-nebenst.n-id
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE nebenst THEN
        DO:
            BUFFER-COPY t-nebenst TO nebenst.
            RELEASE nebenst.
            success-flag = YES.
        END.
    END.
END CASE.


