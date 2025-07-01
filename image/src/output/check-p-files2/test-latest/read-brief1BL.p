
DEF TEMP-TABLE t-brief          LIKE brief.

DEF INPUT  PARAMETER case-type  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER int1       AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER int2       AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER int3       AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER char1      AS CHAR NO-UNDO.
DEF INPUT  PARAMETER char2      AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-brief.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST brief WHERE brief.briefbezeich = char1
            AND brief.briefnr NE int1 NO-LOCK NO-ERROR.
        IF AVAILABLE brief THEN RUN assign-it.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH brief WHERE brief.briefkateg = int1 NO-LOCK:
            RUN assign-it.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST brief WHERE (brief.briefkateg + 600) = int1
            NO-LOCK NO-ERROR.
        IF AVAILABLE brief THEN RUN assign-it.
    END.
    WHEN 4 THEN
    DO:
        FIND FIRST brief WHERE brief.briefbezeich = char1
            AND brief.briefnr NE int1 AND brief.briefkateg = int2 
            NO-LOCK NO-ERROR.
        IF AVAILABLE brief THEN RUN assign-it.
    END.
    WHEN 5 THEN
    DO:
        FOR EACH brief NO-LOCK:
            RUN assign-it.
        END.
    END.
    WHEN 6 THEN
    DO:
        FIND FIRST brief WHERE brief.briefnr = int1 NO-LOCK NO-ERROR.
        IF AVAILABLE brief THEN RUN assign-it.
    END.
END CASE.

PROCEDURE assign-it:
    CREATE t-brief.
    BUFFER-COPY brief TO t-brief.
END.
