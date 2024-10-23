
DEFINE TEMP-TABLE tqueasy LIKE queasy.

DEFINE OUTPUT PARAMETER TABLE FOR tqueasy.

FOR EACH queasy WHERE queasy.key = 2 NO-LOCK BY queasy.char1:
    CREATE tqueasy.
    BUFFER-COPY queasy TO tqueasy.
END.
