DEF TEMP-TABLE t-nitehist LIKE nitehist.


DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER int1 AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER int2 AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER date1 AS DATE NO-UNDO.
DEF INPUT  PARAMETER char1 AS CHAR NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR t-nitehist.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST nitehist WHERE nitehist.datum = date1 NO-LOCK NO-ERROR.
        IF AVAILABLE nitehist THEN
        DO:
            CREATE t-nitehist.
            BUFFER-COPY nitehist TO t-nitehist.
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH vhp.nitehist WHERE vhp.nitehist.datum = date1
            AND vhp.nitehist.reihenfolge = int1 NO-LOCK:
            CREATE t-nitehist.
            BUFFER-COPY nitehist TO t-nitehist.
        END.
    END.
END CASE.
