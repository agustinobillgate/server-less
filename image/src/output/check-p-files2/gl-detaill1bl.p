
DEFINE TEMP-TABLE b1-list
    FIELD jnr       LIKE gl-jouhdr.jnr
    FIELD datum     LIKE gl-jouhdr.datum
    FIELD refno     LIKE gl-jouhdr.refno
    FIELD bezeich   LIKE gl-jouhdr.bezeich
    FIELD debit     LIKE gl-journal.debit
    FIELD credit    LIKE gl-journal.credit
    FIELD userinit  LIKE gl-journal.userinit
    FIELD bemerk    LIKE gl-journal.bemerk
    FIELD jtype     LIKE gl-jouhdr.jtype
    FIELD fibukonto LIKE gl-journal.fibukonto.

DEF TEMP-TABLE t-gl-acct LIKE gl-acct.

DEF INPUT  PARAMETER fibu      AS CHAR. 
DEF INPUT  PARAMETER from-date AS DATE. 
DEF INPUT  PARAMETER to-date   AS DATE.
DEF OUTPUT PARAMETER TABLE FOR b1-list.
DEF OUTPUT PARAMETER TABLE FOR t-gl-acct.
/*Eko 030615*/
DEFINE VARIABLE t-from-date     AS DATE NO-UNDO.
DEFINE VARIABLE t-to-date       AS DATE NO-UNDO.
DEFINE VARIABLE from-datehis    AS DATE NO-UNDO.
DEFINE VARIABLE to-datehis      AS DATE NO-UNDO.
DEFINE VARIABLE t-date          AS DATE NO-UNDO.

FUNCTION lastDay RETURNS DATE ( INPUT d AS DATE ):
    RETURN ADD-INTERVAL( DATE( MONTH( d ), 1, YEAR( d )), 1, "month" ) - 1.
END FUNCTION.
/*End Eko*/
FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibu NO-LOCK.
CREATE t-gl-acct.
BUFFER-COPY gl-acct TO t-gl-acct.

ASSIGN
    t-from-date = from-date
    t-to-date = to-date
    from-date = ?
    t-date = ?. 

FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum LE lastDay(t-from-date) NO-LOCK NO-ERROR.
IF AVAILABLE gl-jouhdr THEN DO: /*Data only available on present datastore*/
    ASSIGN
        from-date = t-from-date
        to-date = t-to-date.
    RUN disp-it.
END.
ELSE DO:
    FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum LE t-to-date NO-LOCK NO-ERROR.
    IF AVAILABLE gl-jouhdr THEN DO: /*Data available in archive and present datastore*/
        DO t-date = t-from-date TO t-to-date:
            FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum LE t-date NO-LOCK NO-ERROR.
            IF AVAILABLE gl-jouhdr THEN DO:
                ASSIGN
                    from-datehis = t-from-date
                    to-datehis   = t-date - 1.
                RUN disp-it-his.
                ASSIGN
                    from-date = t-date
                    to-date   = t-to-date.
                    RUN disp-it.
                LEAVE.
             END.
        END.
    END.
    ELSE DO: /*Data only available on archive datastore*/
        ASSIGN
            from-datehis = t-from-date
            to-datehis = t-to-date.
        RUN disp-it-his.
    END.
END.

PROCEDURE disp-it: 
  FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE from-date 
      AND gl-jouhdr.datum LE to-date NO-LOCK, 
      EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr 
      AND gl-journal.fibukonto = fibu NO-LOCK 
      BY gl-jouhdr.datum:
      CREATE b1-list.
      ASSIGN
        b1-list.jnr       = gl-jouhdr.jnr
        b1-list.datum     = gl-jouhdr.datum
        b1-list.refno     = gl-jouhdr.refno
        b1-list.bezeich   = gl-jouhdr.bezeich
        b1-list.debit     = gl-journal.debit
        b1-list.credit    = gl-journal.credit
        b1-list.userinit  = gl-journal.userinit
        b1-list.bemerk    = gl-journal.bemerk
        b1-list.jtype     = gl-jouhdr.jtype
        b1-list.fibukonto = gl-journal.fibukonto.
  END.
END. 

PROCEDURE disp-it-his: 
  FOR EACH gl-jhdrhis WHERE gl-jhdrhis.datum GE from-datehis 
      AND gl-jhdrhis.datum LE to-datehis NO-LOCK, 
      EACH gl-jourhis WHERE gl-jourhis.jnr = gl-jhdrhis.jnr 
      AND gl-jourhis.fibukonto = fibu NO-LOCK 
      BY gl-jhdrhis.datum:
      CREATE b1-list.
      ASSIGN
        b1-list.jnr       = gl-jhdrhis.jnr
        b1-list.datum     = gl-jhdrhis.datum
        b1-list.refno     = gl-jhdrhis.refno
        b1-list.bezeich   = gl-jhdrhis.bezeich
        b1-list.debit     = gl-jourhis.debit
        b1-list.credit    = gl-jourhis.credit
        b1-list.userinit  = gl-jourhis.userinit
        b1-list.bemerk    = gl-jourhis.bemerk
        b1-list.jtype     = gl-jhdrhis.jtype
        b1-list.fibukonto = gl-jourhis.fibukonto.
  END.
END. 
