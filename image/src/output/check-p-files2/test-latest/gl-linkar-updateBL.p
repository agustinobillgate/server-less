
DEFINE TEMP-TABLE g-list 
  FIELD  rechnr         AS INTEGER 
  FIELD  dept           AS INTEGER 
  FIELD  jnr            LIKE gl-journal.jnr 
  FIELD  fibukonto      LIKE gl-journal.fibukonto 
  FIELD  debit          LIKE gl-journal.debit 
  FIELD  credit         LIKE gl-journal.credit 
  FIELD  bemerk         AS CHAR FORMAT "x(50)" 
  FIELD  userinit       LIKE gl-journal.userinit 
  FIELD  sysdate        LIKE gl-journal.sysdate INITIAL today 
  FIELD  zeit           LIKE gl-journal.zeit 
  FIELD  chginit        LIKE gl-journal.chginit 
  FIELD  chgdate        LIKE gl-journal.chgdate INITIAL ? 
  FIELD  duplicate      AS LOGICAL INITIAL YES 
  FIELD  add-info       AS CHAR 
  FIELD  counter        AS INTEGER
  FIELD  acct-fibukonto LIKE gl-acct.fibukonto
  FIELD  bezeich        LIKE gl-acct.bezeich.

DEFINE INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER remains     AS DECIMAL NO-UNDO.
DEFINE INPUT  PARAMETER credits     LIKE gl-acct.actual[1].
DEFINE INPUT  PARAMETER debits      LIKE gl-acct.actual[1].
DEFINE INPUT  PARAMETER to-date     AS DATE NO-UNDO.
DEFINE INPUT  PARAMETER c-refno     AS CHAR NO-UNDO.
DEFINE INPUT  PARAMETER c-bezeich   AS CHAR NO-UNDO.
DEFINE INPUT  PARAMETER datum       AS DATE.

DEFINE INPUT  PARAMETER TABLE FOR g-list.

DEFINE VARIABLE new-hdr AS LOGICAL INITIAL YES. 
DEFINE VARIABLE curr-counter AS INT INIT 0 NO-UNDO.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-linkar". 

RUN create-header.
RUN create-journals.


PROCEDURE create-header: 
  /*MT 25/09/13 */
  DO TRANSACTION:
      FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE counters THEN 
      DO:
        CREATE counters.
        ASSIGN counters.counter-no  = 25.
        counters.counter-bez = translateExtended ("G/L Transaction Journal",lvCAREA,""). 
      END. 
      ASSIGN
          counters.counter  = counters.counter + 1
          curr-counter      = counters.counter.
      FIND CURRENT counters NO-LOCK.

      CREATE gl-jouhdr. 
      ASSIGN
          gl-jouhdr.jnr     = /*MT 25/09/13 counters.counter */ curr-counter
          gl-jouhdr.refno   = c-refno
          gl-jouhdr.datum   = datum 
          gl-jouhdr.bezeich = c-bezeich 
          gl-jouhdr.batch   = YES
          gl-jouhdr.jtype   = 2
          new-hdr           = YES
      .
      FIND CURRENT gl-jouhdr NO-LOCK.
  END.
END. 
 
PROCEDURE create-journals: 
  /*MT 25/09/13 */
  DO TRANSACTION:
      FOR EACH g-list WHERE (ROUND(g-list.debit,2) NE 0 
          OR ROUND(g-list.credit,2) NE 0) NO-LOCK: 
          CREATE gl-journal.
          ASSIGN
            gl-journal.jnr       = /*MT 25/09/13 gl-jouhdr.jnr */ curr-counter
            gl-journal.fibukonto = g-list.fibukonto 
            gl-journal.debit     = g-list.debit
            gl-journal.credit    = g-list.credit 
            gl-journal.bemerk    = g-list.bemerk + g-list.add-info
            gl-journal.userinit  = g-list.userinit
            gl-journal.zeit      = g-list.zeit
          . 
      END. 

      IF remains = 0.01 OR remains = - 0.01 THEN remains = 0. 
      FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK. 
      ASSIGN
        gl-jouhdr.credit = credits 
        gl-jouhdr.debit = debits
        gl-jouhdr.remain = remains
      . 
      FIND CURRENT gl-jouhdr NO-LOCK. 
      RELEASE gl-jouhdr. 

      FIND FIRST htparam WHERE paramnr = 1014 EXCLUSIVE-LOCK. 
    /* LAST A/R Transfer DATE */ 
      ASSIGN htparam.fdate = datum. 
      FIND CURRENT htparam NO-LOCK.
  END.
END. 
