
DEFINE INPUT  PARAMETER case-type   AS INTEGER.
DEFINE OUTPUT PARAMETER i           AS INTEGER INIT 0 NO-UNDO.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

IF case-type = 1 THEN RUN del-old-hcompli.
ELSE IF case-type = 2 THEN RUN del-old-workorder.
ELSE IF case-type = 3 THEN RUN del-old-global-allotment.
ELSE IF case-type = 4 THEN RUN del-old-quote-attach.

PROCEDURE del-old-hcompli: 
DEFINE VARIABLE anz AS INTEGER. 
DEFINE VARIABLE curr-date AS DATE. 
  FIND FIRST htparam WHERE paramnr = 1083 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz LE 60 THEN anz = 180. 
  curr-date = ci-date - anz. 
  FIND FIRST h-compli WHERE h-compli.datum LE curr-date NO-LOCK 
    USE-INDEX dat_ix NO-ERROR. 
  DO WHILE AVAILABLE h-compli: 
    DO TRANSACTION: 
      i = i + 1.
      FIND CURRENT h-compli EXCLUSIVE-LOCK. 
      delete h-compli. 
    END. 
    FIND NEXT h-compli WHERE h-compli.datum LE curr-date NO-LOCK 
      USE-INDEX dat_ix NO-ERROR. 
  END. 
END. 

PROCEDURE del-old-workorder:
DEF BUFFER qbuff FOR queasy.
  FIND FIRST queasy WHERE queasy.KEY = 28 AND queasy.number1 = 2
    AND queasy.date1 LT (ci-date - 60) NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE queasy:
    DO TRANSACTION:
      FIND FIRST qbuff WHERE RECID(qbuff) = RECID(queasy) EXCLUSIVE-LOCK.
      DELETE qbuff.
      RELEASE qbuff.
    END.
    FIND NEXT queasy WHERE queasy.KEY = 28 AND queasy.number1 = 2
      AND queasy.date1 LT (ci-date - 60) NO-LOCK NO-ERROR.
  END.
END.

PROCEDURE del-old-global-allotment:
DEF BUFFER kline FOR kontline.
  FIND FIRST kontline WHERE kontline.abreise LT (ci-date - 1) NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE kontline:
    FIND FIRST queasy WHERE queasy.KEY = 147
      AND queasy.number1 = kontline.gastnr
      AND queasy.char1   = kontline.kontcode NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
      FIND FIRST res-line WHERE res-line.active-flag = 1
          AND res-line.kontignr = kontline.kontignr NO-LOCK NO-ERROR.
      IF NOT AVAILABLE res-line THEN
      DO TRANSACTION:
        FIND FIRST kline WHERE RECID(kline) = RECID(kontline) 
            EXCLUSIVE-LOCK.
        DELETE kline.
        RELEASE kline.
      END.
    END.
    FIND NEXT kontline WHERE kontline.abreise LT (ci-date - 1) NO-LOCK NO-ERROR.
  END.
END.

PROCEDURE del-old-quote-attach:
DEFINE VARIABLE anz         AS INTEGER. 
DEFINE VARIABLE curr-date   AS DATE. 
DEFINE VARIABLE attach-num  AS INT.

    FIND FIRST htparam WHERE htparam.paramnr EQ 1083 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam AND htparam.finteger NE 0 THEN anz = htparam.finteger.

    IF anz EQ 0 THEN anz = 365.
    curr-date = ci-date - anz.

    FIND FIRST l-quote WHERE l-quote.to-date LT curr-date NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-quote:

        attach-num = INTEGER("-18" + STRING(RECID(l-quote))).
        FIND FIRST guestbook WHERE guestbook.gastnr EQ attach-num 
            AND guestbook.reserve-int[1] EQ INT(RECID(l-quote)) NO-LOCK NO-ERROR.
        IF AVAILABLE guestbook THEN
        DO:
            FIND CURRENT guestbook EXCLUSIVE-LOCK.
            DELETE guestbook.
            RELEASE guestbook.
        END.

        FIND NEXT l-quote WHERE l-quote.to-date LT curr-date NO-LOCK NO-ERROR.
    END.
END PROCEDURE.
