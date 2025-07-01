
DEF INPUT PARAMETER pvILanguage     AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER docu-nr         AS CHAR.
DEF INPUT PARAMETER pbuff-postDate  AS DATE.
DEF INPUT PARAMETER journaltype     AS INT.
DEF INPUT PARAMETER giro-tempAcct   AS CHAR.
DEF INPUT PARAMETER user-init       AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-gcPI".
 
RUN go3.

PROCEDURE go3:
    
    FIND FIRST gc-pi WHERE gc-pi.docu-nr = docu-nr EXCLUSIVE-LOCK.
    ASSIGN gc-pi.postDate = pbuff-postDate.

    FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE counters THEN 
    DO: 
      CREATE counters. 
      counters.counter-no = 25. 
      counters.counter-bez = translateExtended ("G/L Transaction Journal",lvCAREA,""). 
    END. 
    counters.counter = counters.counter + 1. 
    FIND CURRENT counter NO-LOCK. 
    CREATE gl-jouhdr. 
    ASSIGN 
      gl-jouhdr.jnr     = counters.counter 
      gl-jouhdr.jtype   = journaltype
      gl-jouhdr.BATCH   = YES
      gl-jouhdr.refno   = gc-pi.docu-nr2 + "A" 
      gl-jouhdr.datum   = gc-pi.postDate 
      gl-jouhdr.bezeich = gc-pi.bemerk
      gl-jouhdr.debit   = gc-pi.betrag
      gl-jouhdr.credit  = gc-pi.betrag
    . 

    CREATE gl-journal.
    ASSIGN
        gl-journal.jnr       = counters.counter 
        gl-journal.fibukonto = giro-tempAcct
        gl-journal.debit     = gc-pi.betrag
        gl-journal.userinit  = user-init
        gl-journal.sysdate   = TODAY
        gl-journal.zeit      = TIME
        gl-journal.bemerk    = gc-pi.bemerk
    .
    FIND CURRENT gl-journal NO-LOCK.
    
    CREATE gl-journal.
    ASSIGN
        gl-journal.jnr       = counters.counter 
        gl-journal.fibukonto = gc-PI.credit-fibu
        gl-journal.credit    = gc-pi.betrag
        gl-journal.userinit  = user-init
        gl-journal.zeit      = TIME
        gl-journal.bemerk    = gc-pi.bemerk
    .
    FIND CURRENT gl-journal NO-LOCK.
    FIND CURRENT gl-jouhdr NO-LOCK.
END.

