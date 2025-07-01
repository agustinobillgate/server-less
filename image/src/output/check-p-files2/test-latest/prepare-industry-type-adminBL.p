DEF TEMP-TABLE t-queasy LIKE queasy.

DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FOR EACH queasy WHERE queasy.KEY = 281 NO-LOCK:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.
