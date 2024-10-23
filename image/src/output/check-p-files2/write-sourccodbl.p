DEF TEMP-TABLE t-sourccod         LIKE sourccod.


DEF INPUT  PARAMETER case-type    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER TABLE FOR t-sourccod.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-sourccod NO-ERROR.
IF NOT AVAILABLE t-sourccod THEN RETURN NO-APPLY.

CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE sourccod.
        BUFFER-COPY t-sourccod TO sourccod.
        RELEASE sourccod.
        success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST Sourccod WHERE Sourccod.source-code = t-sourccod.source-code
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE Sourccod THEN
        DO:
            BUFFER-COPY t-sourccod TO sourccod.
            RELEASE sourccod.
            success-flag = YES.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST Sourccod WHERE Sourccod.source-code = t-sourccod.source-code
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE Sourccod THEN
        DO:
            DELETE sourccod.
            RELEASE sourccod.
            success-flag = YES.
        END.
    END.
END CASE.
