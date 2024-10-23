DEF TEMP-TABLE t-queasy LIKE queasy.

DEFINE INPUT  PARAMETER case-type   AS INTEGER NO-UNDO. 
DEFINE INPUT  PARAMETER qNo         AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE  FOR t-queasy.

CASE case-type :
    WHEN 1 THEN
    DO:
        FOR EACH queasy WHERE queasy.KEY = qNo NO-LOCK:
            CREATE t-queasy.
            BUFFER-COPY queasy TO t-queasy.
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH queasy WHERE queasy.KEY = qNo AND queasy.logi2 NO-LOCK 
            BY queasy.char1:
            CREATE t-queasy.
            BUFFER-COPY queasy TO t-queasy.
        END.
    END.
    WHEN 3 THEN
    DO:
        FOR EACH queasy WHERE queasy.KEY = qNo AND NOT queasy.logi2 NO-LOCK 
            BY queasy.char1:
            CREATE t-queasy.
            BUFFER-COPY queasy TO t-queasy.
        END.
    END.
    WHEN 4 THEN
    DO:
        FOR EACH queasy WHERE queasy.KEY = qNo NO-LOCK,
            FIRST gl-acct WHERE gl-acct.fibukonto = queasy.char3 :
            CREATE t-queasy.
            BUFFER-COPY queasy TO t-queasy.
        END.
    END.
    WHEN 11 THEN      /* special for HK preference !!!! */
    DO:
        FOR EACH queasy WHERE queasy.KEY = qNo NO-LOCK:
            CREATE t-queasy.
            BUFFER-COPY queasy TO t-queasy.
            ASSIGN t-queasy.number3 = INTEGER(RECID(queasy)).
        END.
    END.

END CASE.

