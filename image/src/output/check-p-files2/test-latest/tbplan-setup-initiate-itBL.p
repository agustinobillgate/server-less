DEF TEMP-TABLE t-queasy LIKE queasy
    FIELD rec-id AS INT.

DEF INPUT PARAMETER location AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FOR EACH queasy WHERE queasy.key = 31 AND queasy.number1 = location 
    AND queasy.betriebsnr = 0 NO-LOCK BY queasy.number2: 
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
    ASSIGN t-queasy.rec-id = RECID(queasy).
END. 
