DEF TEMP-TABLE t-fa-grup LIKE fa-grup
    FIELD rec-id AS INT.

DEF OUTPUT PARAMETER TABLE FOR t-fa-grup.

FOR EACH fa-grup NO-LOCK:
    CREATE t-fa-grup.
    BUFFER-COPY fa-grup TO t-fa-grup.
    ASSIGN t-fa-grup.rec-id = RECID(fa-grup).
END.
