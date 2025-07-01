
DEF TEMP-TABLE t-zimkateg LIKE zimkateg.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER TABLE FOR t-zimkateg.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-zimkateg NO-ERROR.
IF NOT AVAILABLE t-zimkateg THEN RETURN.

CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE zimkateg.
        BUFFER-COPY t-zimkateg TO zimkateg.
        RELEASE zimkateg.
        ASSIGN success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = t-zimkateg.zikatnr
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN
        DO:
            BUFFER-COPY t-zimkateg TO zimkateg.
            RELEASE zimkateg.
            ASSIGN success-flag = YES.
        END.
    END.
END CASE.
