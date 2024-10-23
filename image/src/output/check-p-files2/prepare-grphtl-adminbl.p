
DEFINE TEMP-TABLE t-queasy LIKE queasy
    FIELD rec-id AS INT.

DEFINE OUTPUT PARAMETER TABLE FOR t-queasy.

DEFINE BUFFER queasy1 FOR queasy.  

RUN check-queasy136.
FOR EACH queasy WHERE queasy.KEY = 136 NO-LOCK BY queasy.number1:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
    ASSIGN t-queasy.rec-id = RECID(queasy).
END.


PROCEDURE check-queasy136:
    FIND FIRST queasy WHERE queasy.KEY = 136 
        AND NOT queasy.char1 MATCHES ("*:*") NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
      DO TRANSACTION:
        FIND FIRST queasy1 WHERE RECID(queasy1) = RECID(queasy).
        ASSIGN
            queasy.char1 = queasy.char2 + ":" + queasy.char1
            queasy.char2 = ""
        .
        FIND CURRENT queasy1 NO-LOCK.
        RELEASE queasy1.
        FIND NEXT queasy WHERE queasy.KEY = 136 
            AND NOT queasy.char1 MATCHES ("*:*") NO-LOCK NO-ERROR.
      END.
    END.
END.
