DEFINE TEMP-TABLE inv-list
    FIELD s-recid       AS INTEGER
    FIELD reihenfolge   AS INTEGER FORMAT ">9" LABEL "No"
    FIELD amount        AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Amount"
    FIELD remark        AS CHAR FORMAT "x(28)" LABEL "Remark"
    FIELD inv-AcctNo    LIKE gl-acct.fibukonto
    FIELD inv-bezeich   AS CHAR FORMAT "x(28)" LABEL "Description" 
    FIELD supplier      AS CHAR FORMAT "x(28)" LABEL "Supplier"
    FIELD invNo         AS CHAR FORMAT "x(12)" LABEL "Invoice"
    FIELD created       AS DATE
    FIELD zeit          AS INTEGER
.

DEF INPUT  PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER journaltype     AS INTEGER.
DEF INPUT  PARAMETER pbuff-betrag    LIKE gc-pi.betrag.
DEF INPUT  PARAMETER pbuff-returnAmt LIKE gc-pi.returnAmt.
DEF INPUT  PARAMETER ret-Acctno      AS CHAR.
DEF INPUT  PARAMETER user-init       AS CHAR.
DEF INPUT  PARAMETER docu-nr         AS CHAR.
DEF INPUT  PARAMETER TABLE FOR inv-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-gcPI".

FIND FIRST gc-pi WHERE gc-pi.docu-nr = docu-nr NO-LOCK.

DO TRANSACTION:
    FIND CURRENT gc-PI EXCLUSIVE-LOCK.
    
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
      gl-jouhdr.refno   = gc-pi.docu-nr2 
      gl-jouhdr.datum   = gc-pi.datum2 
      gl-jouhdr.bezeich = gc-pi.docu-nr
    .
    IF pbuff-returnAmt LT 0 THEN
    ASSIGN
      gl-jouhdr.debit   = pbuff-betrag - pbuff-returnAmt
      gl-jouhdr.credit  = pbuff-betrag - pbuff-returnAmt
    . 
    ELSE
    ASSIGN
      gl-jouhdr.debit   = pbuff-betrag
      gl-jouhdr.credit  = pbuff-betrag
    . 
    
    IF pbuff-returnAmt NE 0 THEN
    DO:
      CREATE gl-journal.
      ASSIGN
        gl-journal.jnr       = counters.counter
        gl-journal.fibukonto = ret-Acctno
        gl-journal.userinit  = user-init
        gl-journal.sysdate   = TODAY
        gl-journal.zeit      = TIME
        gl-journal.bemerk    = gc-pi.docu-nr
      .
      IF pbuff-returnAmt GT 0 THEN gl-journal.debit = pbuff-returnAmt.
      ELSE gl-journal.credit = - pbuff-returnAmt.
      FIND CURRENT gl-journal NO-LOCK.
    END.

    CREATE gl-journal.
    ASSIGN
        gl-journal.jnr       = counters.counter 
        gl-journal.fibukonto = gc-PI.debit-fibu
        gl-journal.credit    = gc-pi.betrag
        gl-journal.userinit  = user-init
        gl-journal.sysdate   = TODAY
        gl-journal.zeit      = TIME
        gl-journal.bemerk    = gc-pi.docu-nr
    .
    FIND CURRENT gl-journal NO-LOCK.

    FOR EACH inv-list:
      CREATE gl-journal.
      ASSIGN
        gl-journal.jnr       = counters.counter 
        gl-journal.fibukonto = inv-list.inv-acctNo
        gl-journal.debit     = inv-list.amount
        gl-journal.userinit  = user-init
        gl-journal.sysdate   = TODAY
        gl-journal.zeit      = TIME
        gl-journal.bemerk    = inv-list.remark
      .
      IF inv-list.supplier NE "" OR inv-list.invNo NE "" 
      THEN gl-journal.bemerk = gl-journal.bemerk 
        + " [" + inv-list.supplier + "-" + inv-list.invNo + "]".
      FIND CURRENT gl-journal NO-LOCK.
    END.
    FIND CURRENT gl-jouhdr NO-LOCK.

    ASSIGN gc-pi.pi-status = 2.
    FIND CURRENT gc-pi NO-LOCK.
END.
