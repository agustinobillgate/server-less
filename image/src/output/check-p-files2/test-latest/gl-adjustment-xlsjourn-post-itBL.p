DEFINE TEMP-TABLE g-list 
  FIELD  jnr        LIKE gl-journal.jnr 
  FIELD  fibukonto  LIKE gl-journal.fibukonto 
  FIELD  fibukonto2 LIKE gl-journal.fibukonto
  FIELD  debit      LIKE gl-journal.debit 
  FIELD  credit     LIKE gl-journal.credit 
  FIELD  userinit   LIKE gl-journal.userinit 
  FIELD  sysdate    LIKE gl-journal.sysdate INITIAL today 
  FIELD  zeit       LIKE gl-journal.zeit 
  FIELD  chginit    LIKE gl-journal.chginit 
  FIELD  chgdate    LIKE gl-journal.chgdate INITIAL ? 
  FIELD  bemerk     LIKE gl-journal.bemerk 
  FIELD  descr      LIKE gl-acct.bezeich
  FIELD  duplicate  AS LOGICAL INITIAL YES
  FIELD  correct    AS INT INITIAL 0.

DEF INPUT  PARAMETER TABLE FOR g-list.
DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER datum       AS DATE.
DEF INPUT  PARAMETER journ-no    AS CHAR.
DEF INPUT  PARAMETER jour-type   AS INT.
DEF INPUT  PARAMETER journ-name  AS CHAR.
DEF INPUT  PARAMETER debits      LIKE gl-acct.actual[1].
DEF INPUT  PARAMETER credits     LIKE gl-acct.actual[1].
DEF INPUT  PARAMETER remains     LIKE gl-acct.actual[1].
DEF OUTPUT PARAMETER t-jnr       LIKE gl-jouhdr.jnr.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-xlsjourn".

RUN post-it.

PROCEDURE post-it:
    DO TRANSACTION:
       FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE counters THEN 
        DO: 
          create counters. 
          counters.counter-no = 25. 
          counters.counter-bez = translateExtended ("G/L Transaction Journal",lvCAREA,""). 
        END. 
        counters.counter = counters.counter + 1. 
        FIND CURRENT counter NO-LOCK. 
        CREATE gl-jouhdr. 
        ASSIGN 
          gl-jouhdr.jnr = counters.counter 
          gl-jouhdr.refno = journ-no
          gl-jouhdr.datum = datum 
          gl-jouhdr.bezeich = journ-name
          gl-jouhdr.jtype  = jour-type
          gl-jouhdr.credit = credits
          gl-jouhdr.debit = debits 
          gl-jouhdr.remain = remains
          gl-jouhdr.BATCH = YES
            . 
        IF jour-type = 0 THEN
            gl-jouhdr.BATCH = NO.

        FIND CURRENT gl-jouhdr NO-LOCK. 
        ASSIGN t-jnr = gl-jouhdr.jnr.
   
        FOR EACH g-list NO-LOCK: 
            create gl-journal. 
            gl-journal.jnr = counters.counter.
            gl-journal.fibukonto = g-list.fibukonto2. 
            gl-journal.debit = g-list.debit. 
            gl-journal.credit = g-list.credit. 
            gl-journal.userinit = g-list.userinit. 
            gl-journal.zeit = g-list.zeit. 
            gl-journal.bemerk = g-list.bemerk. 
        END.          
    END. 
END.
