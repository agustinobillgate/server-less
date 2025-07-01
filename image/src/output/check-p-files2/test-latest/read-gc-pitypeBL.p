
DEF TEMP-TABLE t-gc-pitype LIKE gc-pitype.

DEF INPUT  PARAMETER case-type AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-gc-pitype.

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH gc-pitype NO-LOCK
            BY gc-pitype.activeflag BY gc-pitype.nr:
            RUN assign-it.
        END.
    END.
END CASE.

PROCEDURE assign-it:
    CREATE t-gc-pitype.
    BUFFER-COPY gc-pitype TO t-gc-pitype.
END.
