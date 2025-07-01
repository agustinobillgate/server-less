DEF TEMP-TABLE t-queasy LIKE queasy
    FIELD rec-id AS INT.

DEF INPUT PARAMETER location     AS INT.
DEF INPUT PARAMETER floor    AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FOR EACH queasy WHERE queasy.key EQ 31 AND queasy.number1 EQ location 
    AND queasy.betriebsnr EQ 0 AND queasy.deci3 EQ floor NO-LOCK BY queasy.number2: 
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
    ASSIGN t-queasy.rec-id = RECID(queasy).
END. 
