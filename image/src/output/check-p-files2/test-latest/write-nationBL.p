DEF TEMP-TABLE t-nation LIKE nation.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER TABLE FOR t-nation.
DEF OUTPUT PARAMETER success-flag AS LOGICAL.

FIND FIRST t-nation NO-LOCK NO-ERROR.
IF NOT AVAILABLE t-nation THEN RETURN.

CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE nation.
        BUFFER-COPY t-nation TO nation.
        success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST nation WHERE nation.kurzbez = t-nation.kurzbez
            AND nation.untergruppe = t-nation.untergruppe 
            AND nation.natcode = t-nation.natcode
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE nation THEN
        DO:
            BUFFER-COPY t-nation TO nation.
            success-flag = YES.
        END.
    END.
END CASE.
