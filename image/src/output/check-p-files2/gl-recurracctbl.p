DEF TEMP-TABLE b1-list LIKE queasy
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD bezeich   LIKE gl-acct.bezeich
    FIELD rec-id    AS INT.

DEF OUTPUT PARAMETER TABLE FOR b1-list.

FOR EACH queasy WHERE key = 106 NO-LOCK,
    FIRST gl-acct WHERE gl-acct.fibukonto = queasy.char3 
    BY queasy.char1 BY gl-acct.fibukonto:
    CREATE b1-list.
    BUFFER-COPY queasy TO b1-list.
    b1-list.rec-id = RECID(queasy).
    ASSIGN
      b1-list.fibukonto = gl-acct.fibukonto
      b1-list.bezeich   = gl-acct.bezeich.
END.
