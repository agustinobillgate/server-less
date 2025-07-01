
DEF TEMP-TABLE t-gc-giro LIKE gc-giro
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER case-type AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-gc-giro.

CASE case-type :
    WHEN 1 THEN
    DO:
        FOR EACH gc-giro NO-LOCK:
            RUN assign-it.
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH gc-giro WHERE gc-giro.giro-status = 0 NO-LOCK:
            RUN assign-it.
        END.
    END.
END CASE.

PROCEDURE assign-it:
    CREATE t-gc-giro.
    BUFFER-COPY gc-giro TO t-gc-giro.
    ASSIGN t-gc-giro.rec-id = RECID(gc-giro).
END.
