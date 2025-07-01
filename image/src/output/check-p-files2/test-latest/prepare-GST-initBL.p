DEF TEMP-TABLE t-l-artikel LIKE l-artikel.

DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.

FOR EACH l-artikel NO-LOCK:
    CREATE t-l-artikel.
    BUFFER-COPY l-artikel TO t-l-artikel.
END.
