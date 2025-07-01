DEF TEMP-TABLE t-artikel LIKE artikel.

DEF OUTPUT PARAMETER TABLE FOR t-artikel.

FOR EACH artikel WHERE artikel.artart = 0 OR artikel.artart = 8 NO-LOCK:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
END.
