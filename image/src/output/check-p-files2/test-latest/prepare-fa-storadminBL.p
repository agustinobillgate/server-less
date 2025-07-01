DEFINE TEMP-TABLE t-fa-lager LIKE fa-lager
    FIELD rec-id AS INT.

DEF OUTPUT PARAMETER TABLE FOR t-fa-lager.

FOR EACH fa-lager NO-LOCK:
    CREATE t-fa-lager.
    BUFFER-COPY fa-lager TO t-fa-lager.
    ASSIGN t-fa-lager.rec-id = RECID(fa-lager).
END.
