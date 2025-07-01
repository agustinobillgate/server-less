DEF INPUT PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER docu-nr         AS CHAR.
DEF INPUT PARAMETER billdate        AS DATE.
DEF INPUT PARAMETER journaltype     AS INT.
DEF INPUT PARAMETER pi-acctNo       AS CHAR.
DEF INPUT PARAMETER user-init       AS CHAR.
DEF INPUT PARAMETER pbuff-postDate  AS DATE.
DEF INPUT PARAMETER giro-tempAcct   AS CHAR.


{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-gcPI".
DEF BUFFER gc-pibuff FOR gc-pi.

FIND FIRST gc-pi WHERE gc-pi.docu-nr = docu-nr NO-LOCK NO-ERROR. /* Malik Serverless 583 add NO-LOCK NO-ERROR */
IF NOT AVAILABLE gc-pi THEN RETURN. /* Malik Serverless 583 */

DO TRANSACTION:
    ASSIGN
        gc-pi.debit-fibu = pi-acctNo
        gc-pi.pi-status  = 1.
    FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE counters THEN 
    DO: 
      CREATE counters. 
      counters.counter-no = 25. 
      counters.counter-bez = translateExtended ("G/L Transaction Journal",lvCAREA,""). 
    END. 
    /*FIND FIRST gc-pibuff WHERE SUBSTR(gc-pibuff.docu-nr, 1, 9) 
        = ("PI" + STRING(MONTH(billdate),"99") + STRING(YEAR(billdate),"9999") 
        + "-") NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gc-pibuff THEN ASSIGN counters.counter = 0.*/

    counters.counter = counters.counter + 1.
    FIND CURRENT counter NO-LOCK. 

    CREATE gl-jouhdr. 
    ASSIGN 
      gl-jouhdr.jnr     = counters.counter 
      gl-jouhdr.jtype   = journaltype
      gl-jouhdr.BATCH   = YES
      gl-jouhdr.refno   = gc-pi.docu-nr 
      gl-jouhdr.datum   = gc-pi.pay-datum 
      gl-jouhdr.bezeich = gc-pi.bemerk
      gl-jouhdr.debit   = gc-pi.betrag
      gl-jouhdr.credit  = gc-pi.betrag
    . 
    IF gc-pi.postDate NE ? THEN gl-jouhdr.datum = gc-pi.postDate.

    CREATE gl-journal.
    ASSIGN
        gl-journal.jnr       = counters.counter 
        gl-journal.fibukonto = gc-PI.debit-fibu
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
        gl-journal.credit    = gc-pi.betrag
        gl-journal.userinit  = user-init
        gl-journal.zeit      = TIME
        gl-journal.bemerk    = gc-pi.bemerk
    .
    IF gc-pi.pay-type NE 2 OR giro-tempAcct = "" OR pbuff-postDate NE ? THEN
        ASSIGN gl-journal.fibukonto = gc-PI.credit-fibu.
    ELSE gl-journal.fibukonto = giro-tempAcct.

    FIND CURRENT gl-journal NO-LOCK.
    FIND CURRENT gl-jouhdr NO-LOCK.
END.
