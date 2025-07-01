DEF TEMP-TABLE t-printcod LIKE printcod.

DEF INPUT  PARAMETER case-type AS INT.
DEF INPUT  PARAMETER char1 AS CHAR NO-UNDO.
DEF INPUT  PARAMETER char2 AS CHAR NO-UNDO.
DEF INPUT  PARAMETER char3 AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-printcod.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST printcod WHERE printcod.emu = char1  NO-LOCK NO-ERROR.
        IF AVAILABLE printcod THEN
        DO:
          RUN assign-it.
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH printcod NO-LOCK BY printcod.emu:
            RUN assign-it.
        END.
    END.
END CASE.

PROCEDURE assign-it:
    CREATE t-printcod.
    BUFFER-COPY printcod TO t-printcod.
END.
