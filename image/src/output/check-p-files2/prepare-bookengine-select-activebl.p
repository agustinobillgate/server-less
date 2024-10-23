
DEF TEMP-TABLE t-queasy LIKE queasy.

DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FOR EACH queasy WHERE KEY = 159 AND queasy.number2 GT 0 NO-LOCK:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.
