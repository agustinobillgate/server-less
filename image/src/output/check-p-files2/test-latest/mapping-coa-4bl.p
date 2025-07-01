DEF TEMP-TABLE coa-list
    FIELD old-fibu AS CHAR FORMAT "x(12)"
    FIELD new-fibu AS CHAR FORMAT "x(12)"
    FIELD bezeich AS CHAR FORMAT "x(48)"  /**/
    FIELD coaStat  AS INTEGER INITIAL -1
    FIELD old-main AS INTEGER
    FIELD new-main AS INTEGER
    FIELD bezeichM AS CHAR
    FIELD old-dept AS INTEGER
    FIELD new-dept AS INTEGER
    FIELD bezeichD AS CHAR
    FIELD catno    AS INTEGER
    FIELD acct     AS INTEGER
    FIELD old-acct AS INTEGER
    INDEX coa-ix old-fibu
.

DEF TEMP-TABLE acct-list LIKE gl-acct
    INDEX acct_ix fibukonto.

DEFINE INPUT PARAMETER TABLE FOR coa-list.

MESSAGE "start mapping COA 4" VIEW-AS ALERT-BOX.

DEFINE VARIABLE i AS INTEGER NO-UNDO.

RUN update-gl3.
RUN delete-gl.

PROCEDURE update-gl3:
    FOR EACH acct-list.
        DELETE acct-list.
    END.

    DO TRANSACTION:
        FIND FIRST gl-acct NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE gl-acct:
          FIND FIRST coa-list WHERE coa-list.old-fibu = gl-acct.fibukonto NO-LOCK NO-ERROR.
          IF AVAILABLE coa-list THEN
          DO:
            CREATE acct-list.
            BUFFER-COPY gl-acct TO acct-list.
            FIND CURRENT gl-acct EXCLUSIVE-LOCK.
            DELETE gl-acct.
            RELEASE gl-acct.
          END.
          FIND NEXT gl-acct NO-LOCK NO-ERROR.
        END.
    END.

    MESSAGE "done delete gl-acct" VIEW-AS ALERT-BOX.

    FIND FIRST coa-list WHERE coa-list.old-fibu NE ? NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE coa-list:
        FIND FIRST acct-list WHERE acct-list.fibukonto = coa-list.old-fibu NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE acct-list:
            FIND FIRST gl-acct WHERE gl-acct.fibukonto = coa-list.new-fibu NO-ERROR.
              IF AVAILABLE gl-acct THEN
              DO TRANSACTION:
                  DO i = 1 TO 12:
                    ASSIGN
                      gl-acct.actual[i]    = gl-acct.actual[i]    + acct-list.actual[i]
                      gl-acct.last-yr[i]   = gl-acct.last-yr[i]   + acct-list.last-yr[i]
                      gl-acct.budget[i]    = gl-acct.budget[i]    + acct-list.budget[i]
                      gl-acct.ly-budget[i] = gl-acct.ly-budget[i] + acct-list.ly-budget[i]
                      gl-acct.debit[i]     = gl-acct.debit[i]     + acct-list.debit[i]
                      gl-acct.credit[i]    = gl-acct.credit[i]    + acct-list.credit[i].
                  END.
              END.
              ELSE
              DO TRANSACTION:
                  CREATE gl-acct.
                  BUFFER-COPY acct-list EXCEPT fibukonto TO gl-acct.
                  ASSIGN 
                    gl-acct.fibukonto = coa-list.new-fibu
                    gl-acct.bezeich   = coa-list.bezeich
                    gl-acct.main-nr   = coa-list.new-main
                    gl-acct.deptnr    = coa-list.new-dept
                    gl-acct.fs-type   = coa-list.catno
                    gl-acct.acc-type  = coa-list.acct.
              END.
            FIND NEXT acct-list WHERE acct-list.fibukonto = coa-list.old-fibu NO-LOCK NO-ERROR.
        END.
        FIND NEXT coa-list WHERE coa-list.old-fibu NE ? NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update gl-acct" VIEW-AS ALERT-BOX.

    FOR EACH coa-list WHERE coa-list.old-fibu = ? AND coa-list.new-fibu NE "":
      CREATE gl-acct.
      ASSIGN 
        gl-acct.fibukonto = coa-list.new-fibu
        gl-acct.bezeich   = coa-list.bezeich
        gl-acct.main-nr   = coa-list.new-main
        gl-acct.deptnr    = coa-list.new-dept
        gl-acct.fs-type   = coa-list.catno
        gl-acct.acc-type  = coa-list.acct.
    END.
    MESSAGE "done create new gl-acct" VIEW-AS ALERT-BOX.
END.

PROCEDURE delete-gl:
    FOR EACH coa-list WHERE coa-list.coaStat = -1:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = coa-list.old-fibu
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        DO:
            DELETE gl-acct.
            RELEASE gl-acct.
        END.

        FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = coa-list.old-fibu
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE gl-accthis THEN
        DO:
            DELETE gl-accthis.
            RELEASE gl-accthis.
        END.

        FIND FIRST gl-jourhis WHERE gl-jourhis.fibukonto = coa-list.old-fibu
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE gl-jourhis THEN
        DO:
            DELETE gl-jourhis.
            RELEASE gl-jourhis.
        END.

        FIND FIRST gl-journal WHERE gl-journal.fibukonto = coa-list.old-fibu
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE gl-journal THEN
        DO:
            DELETE gl-journal.
            RELEASE gl-journal.
        END.
    END.
END.

