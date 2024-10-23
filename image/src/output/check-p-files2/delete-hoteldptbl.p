

DEF INPUT  PARAMETER case-type AS INTEGER.
DEF INPUT  PARAMETER int1  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER int2  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER char1 AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER success-flag AS LOGICAL.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST hoteldpt WHERE hoteldpt.num = int1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE hoteldpt THEN
        DO:
            DELETE hoteldpt.
            RELEASE hoteldpt.
            ASSIGN success-flag = YES.
        END.
    END.
END CASE.
