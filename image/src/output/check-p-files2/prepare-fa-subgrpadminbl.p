DEF TEMP-TABLE t-fa-grup LIKE fa-grup
    FIELD rec-id AS INT.
DEF TEMP-TABLE t-fa-artikel LIKE fa-artikel.

DEF OUTPUT PARAMETER TABLE FOR t-fa-grup.
DEF OUTPUT PARAMETER TABLE FOR t-fa-artikel.

FOR EACH fa-grup NO-LOCK:
    CREATE t-fa-grup.
    BUFFER-COPY fa-grup TO t-fa-grup.
    ASSIGN t-fa-grup.rec-id = RECID(fa-grup).
END.


FOR EACH fa-artikel NO-LOCK:
    CREATE t-fa-artikel.
    BUFFER-COPY fa-artikel TO t-fa-artikel.
END.
