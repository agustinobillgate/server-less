
DEF TEMP-TABLE t-queasy LIKE queasy
    FIELD rec-id AS INT
    FIELD char4 AS CHARACTER.

DEF OUTPUT PARAMETER compli-dept AS INTEGER INITIAL 1 NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

DEFINE VARIABLE str AS CHAR.

RUN get-compli-dept.

FOR EACH queasy WHERE queasy.key = 105 NO-LOCK BY queasy.char1:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
    ASSIGN 
        t-queasy.rec-id = RECID(queasy)
        str = ENTRY(NUM-ENTRIES(queasy.char3,"&") - 1,queasy.char3, "&")
        t-queasy.char3 = SUBSTR (queasy.char3, 1, LENGTH(queasy.char3) - LENGTH(str) - 2).
        t-queasy.char4 = TRIM(str).
END.


PROCEDURE get-compli-dept:
  FOR EACH vhp.h-artikel WHERE vhp.h-artikel.artart = 11 NO-LOCK
    BY vhp.h-artikel.departement:
    compli-dept = vhp.h-artikel.departement.
    RETURN.
  END.
END.

