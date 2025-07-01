
DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEF INPUT  PARAMETER case-type AS INTEGER.
DEF INPUT  PARAMETER int1  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER int2  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER char1 AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

CASE case-type.
    WHEN 1 THEN
    DO:
        FIND FIRST hoteldpt WHERE hoteldpt.num = int1 NO-LOCK NO-ERROR.
        IF AVAILABLE hoteldpt THEN RUN assign-it.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST hoteldpt WHERE hoteldpt.depart = char1
            AND hoteldpt.num NE int1 NO-LOCK NO-ERROR.
        IF AVAILABLE hoteldpt THEN RUN assign-it.
    END.
END CASE.

PROCEDURE assign-it:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.
