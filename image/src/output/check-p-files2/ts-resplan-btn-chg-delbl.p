DEF TEMP-TABLE t-queasy
    FIELD char1   LIKE queasy.char1
    FIELD char2   LIKE queasy.char2
    FIELD number3 LIKE queasy.number3
    FIELD rec-id  AS INT.

DEF INPUT  PARAMETER s-recid AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FIND FIRST queasy WHERE RECID(queasy) = s-recid NO-LOCK.
CREATE t-queasy.
ASSIGN
    t-queasy.char1   = queasy.char1
    t-queasy.char2   = queasy.char2
    t-queasy.number3 = queasy.number3
    t-queasy.rec-id  = RECID(queasy).
