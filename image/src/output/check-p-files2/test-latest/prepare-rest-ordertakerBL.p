
DEF TEMP-TABLE t-queasy LIKE queasy
    FIELD rec-id AS INT.


DEF OUTPUT PARAMETER TABLE FOR t-queasy.
FOR EACH queasy WHERE key = 10 
    NO-LOCK BY queasy.number1:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
    ASSIGN t-queasy.rec-id = RECID(queasy).
END.
