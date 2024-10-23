DEF TEMP-TABLE s-list LIKE queasy
    FIELD char4 AS CHAR. 

DEF TEMP-TABLE t-queasy LIKE queasy
    FIELD rec-id AS INT.

DEF INPUT PARAMETER TABLE FOR s-list.
DEF INPUT PARAMETER curr-select     AS CHAR.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FIND FIRST s-list.
FIND FIRST h-artikel WHERE h-artikel.artnr = s-list.number3
    AND h-artikel.departement = 1 AND h-artikel.artart = 11 
    NO-LOCK NO-ERROR. 
IF NOT AVAILABLE h-artikel THEN 
DO: 
    err-code = 1.
    RETURN NO-APPLY. 
END.

IF curr-select = "add" THEN 
DO: 
    DO: 
      create queasy.
      create t-queasy.
      RUN fill-new-queasy. 
    END. 
    RETURN NO-APPLY. 
END. 
ELSE IF curr-select = "chg" THEN 
DO: 
    IF s-list.char1 = "" THEN . 
    ELSE 
    DO: 
      FIND FIRST queasy WHERE RECID(queasy) = rec-id EXCLUSIVE-LOCK. 
      ASSIGN
        queasy.char1 = s-list.char1
        queasy.char2 = s-list.char2 
        queasy.char3 = h-artikel.bezeich + "&" + s-list.char4 + "&"
        queasy.number3 = s-list.number3. 
        queasy.deci3 = s-list.deci3. 
      FIND CURRENT queasy NO-LOCK. 
      CREATE t-queasy.
      BUFFER-COPY queasy TO t-queasy.
      ASSIGN t-queasy.rec-id = RECID(queasy).
    END. 
    RETURN NO-APPLY. 
END. 

PROCEDURE fill-new-queasy: 
  ASSIGN
    queasy.key = 105
    queasy.number3 = s-list.number3
    queasy.deci3 = s-list.deci3
    queasy.char1 = s-list.char1 
    queasy.char2 = s-list.char2 
    queasy.char3 = h-artikel.bezeich + "&" + s-list.char4 + "&"
  .
  ASSIGN
    t-queasy.key = 105
    t-queasy.number3 = s-list.number3
    t-queasy.deci3 = s-list.deci3
    t-queasy.char1 = s-list.char1 
    t-queasy.char2 = s-list.char2 
    t-queasy.char3 = h-artikel.bezeich + "&" + s-list.char4 + "&"
    t-queasy.rec-id = RECID(queasy)
  .
END. 

