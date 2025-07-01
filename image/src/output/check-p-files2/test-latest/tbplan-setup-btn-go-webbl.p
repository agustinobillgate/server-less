DEF TEMP-TABLE t-queasy LIKE queasy
    FIELD rec-id AS INT.

DEF INPUT PARAMETER curr-mode  AS CHAR.
DEF INPUT PARAMETER location   AS INT.
DEF INPUT PARAMETER from-table AS INT.
DEF INPUT PARAMETER location2  AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

IF curr-mode = "add" THEN
DO:
    CREATE queasy. 
    ASSIGN 
        queasy.key = 31 
        queasy.number1 = location 
        queasy.number2 = from-table
        queasy.deci3   = location2
      . 
    FIND CURRENT queasy NO-LOCK. 
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
    ASSIGN t-queasy.rec-id = RECID(queasy).
END.
ELSE IF curr-mode = "move" THEN
DO:
    FIND FIRST queasy WHERE queasy.key = 31 AND queasy.number1 = location 
        AND queasy.number2 = from-table AND queasy.betriebsnr = 0 AND queasy.deci3 EQ location2 NO-LOCK. 
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
    ASSIGN t-queasy.rec-id = RECID(queasy).
END.
