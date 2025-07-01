DEF TEMP-TABLE t-zimkateg LIKE zimkateg.
DEF TEMP-TABLE t-queasy   LIKE queasy.

DEF OUTPUT PARAMETER TABLE FOR t-zimkateg.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FOR EACH zimkateg NO-LOCK:
    CREATE t-zimkateg.
    BUFFER-COPY zimkateg TO t-zimkateg.
END.

FOR EACH queasy WHERE queasy.KEY = 152 NO-LOCK BY queasy.number1:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.
