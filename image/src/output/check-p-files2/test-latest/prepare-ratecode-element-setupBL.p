DEFINE TEMP-TABLE t-queasy LIKE queasy.

DEFINE OUTPUT PARAMETER TABLE FOR t-queasy.

FOR EACH queasy WHERE queasy.KEY = 287 NO-LOCK:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.
