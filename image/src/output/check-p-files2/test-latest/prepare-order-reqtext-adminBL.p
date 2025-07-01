
DEFINE TEMP-TABLE t-queasy
    FIELD char1     LIKE queasy.char1
    FIELD number1   LIKE queasy.number1
    FIELD rec-id    AS INT.

DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FOR EACH queasy WHERE key = 12 
    NO-LOCK BY queasy.number1:
    CREATE t-queasy.
    ASSIGN
        t-queasy.char1     = queasy.char1
        t-queasy.number1   = queasy.number1
        t-queasy.rec-id    = RECID(queasy).
END.
