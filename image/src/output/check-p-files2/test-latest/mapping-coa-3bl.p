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

DEF TEMP-TABLE temp-gl-accthis LIKE gl-accthis.

DEF TEMP-TABLE acct-list LIKE gl-acct
    INDEX acct_ix fibukonto.

DEFINE INPUT PARAMETER TABLE FOR coa-list.

MESSAGE "start mapping COA 3" VIEW-AS ALERT-BOX.

DEFINE VARIABLE i AS INTEGER NO-UNDO.

RUN update-gl2.

PROCEDURE update-gl2:
    FOR EACH temp-gl-accthis:
        DELETE temp-gl-accthis.
    END.

    DO TRANSACTION:
        FIND FIRST gl-accthis NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE gl-accthis:
          FIND FIRST coa-list WHERE coa-list.old-fibu = gl-accthis.fibukonto NO-LOCK NO-ERROR.
          IF AVAILABLE coa-list THEN
          DO:
            CREATE temp-gl-accthis.
            BUFFER-COPY gl-accthis TO temp-gl-accthis.
            FIND CURRENT gl-accthis EXCLUSIVE-LOCK.
            DELETE gl-accthis.
            RELEASE gl-accthis.
          END.
          FIND NEXT gl-accthis NO-LOCK NO-ERROR.
        END.
    END.

    MESSAGE "done delete gl-accthis" VIEW-AS ALERT-BOX.

    FIND FIRST coa-list NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE coa-list:
        FIND FIRST temp-gl-accthis WHERE temp-gl-accthis.fibukonto = coa-list.old-fibu NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE temp-gl-accthis:
          FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = coa-list.new-fibu 
            AND gl-accthis.YEAR = temp-gl-accthis.YEAR NO-ERROR.
          IF AVAILABLE gl-accthis THEN
          DO TRANSACTION:
              DO i = 1 TO 12:
                ASSIGN
                    gl-accthis.actual[i]    = gl-accthis.actual[i]    + temp-gl-accthis.actual[i]
                    gl-accthis.last-yr[i]   = gl-accthis.last-yr[i]   + temp-gl-accthis.last-yr[i]
                    gl-accthis.budget[i]    = gl-accthis.budget[i]    + temp-gl-accthis.budget[i]
                    gl-accthis.ly-budget[i] = gl-accthis.ly-budget[i] + temp-gl-accthis.ly-budget[i]
                    gl-accthis.debit[i]     = gl-accthis.debit[i]     + temp-gl-accthis.debit[i]
                    gl-accthis.credit[i]    = gl-accthis.credit[i]    + temp-gl-accthis.credit[i].
              END.
          END.
          ELSE
          DO TRANSACTION:
              CREATE gl-accthis.
              BUFFER-COPY temp-gl-accthis EXCEPT fibukonto TO gl-accthis.
              ASSIGN 
                gl-accthis.fibukonto = coa-list.new-fibu
                gl-accthis.bezeich   = coa-list.bezeich
                gl-accthis.main-nr   = coa-list.new-main
                gl-accthis.deptnr    = coa-list.new-dept
                gl-accthis.fs-type   = coa-list.catno
                gl-accthis.acc-type  = coa-list.acct.
          END.
          FIND NEXT temp-gl-accthis WHERE temp-gl-accthis.fibukonto = coa-list.old-fibu NO-LOCK NO-ERROR.
        END.
        FIND NEXT coa-list NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update gl-accthis" VIEW-AS ALERT-BOX.
END.
