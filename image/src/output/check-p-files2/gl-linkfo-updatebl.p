
DEFINE TEMP-TABLE g-list 
  FIELD  flag       AS INTEGER 
  FIELD  datum      AS DATE 
  FIELD  artnr      AS INTEGER 
  FIELD  dept       AS INTEGER 
  FIELD  jnr        LIKE gl-journal.jnr 
  FIELD  fibukonto  LIKE gl-journal.fibukonto 
  FIELD  debit      LIKE gl-journal.debit   FORMAT ">,>>>,>>>,>>9.99"
  FIELD  credit     LIKE gl-journal.credit FORMAT ">,>>>,>>>,>>9.99"
  FIELD  bemerk     AS CHAR FORMAT "x(32)" 
  FIELD  userinit   LIKE gl-journal.userinit 
  FIELD  sysdate    LIKE gl-journal.sysdate INITIAL today 
  FIELD  zeit       LIKE gl-journal.zeit 
  FIELD  chginit    LIKE gl-journal.chginit 
  FIELD  chgdate    LIKE gl-journal.chgdate INITIAL ? 
  FIELD  duplicate  AS LOGICAL INITIAL YES
  FIELD  acct-fibukonto LIKE gl-acct.fibukonto
  FIELD  bezeich    LIKE gl-acct.bezeich. 

DEFINE INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER remains     AS DECIMAL NO-UNDO.
DEFINE INPUT  PARAMETER credits     LIKE gl-acct.actual[1].
DEFINE INPUT  PARAMETER debits      LIKE gl-acct.actual[1].
DEFINE INPUT  PARAMETER to-date     AS DATE NO-UNDO.
DEFINE INPUT  PARAMETER c-refno     AS CHAR NO-UNDO.
DEFINE INPUT  PARAMETER c-bezeich   AS CHAR NO-UNDO.

DEFINE INPUT  PARAMETER TABLE FOR g-list.

DEFINE VARIABLE new-hdr AS LOGICAL INITIAL YES. 

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-linkfo". 


RUN create-header.
RUN create-journals.

PROCEDURE create-header: 
  create gl-jouhdr. 
  FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE counters THEN 
  DO: 
    create counters. 
    counters.counter-no = 25. 
    counters.counter-bez = translateExtended ("G/L Transaction Journal",lvCAREA,""). 
  END. 
  ASSIGN
    counters.counter  = counters.counter + 1
    gl-jouhdr.jnr     = counters.counter 
    gl-jouhdr.datum   = to-date
    gl-jouhdr.refno   = c-refno 
    gl-jouhdr.bezeich = c-bezeich 
    gl-jouhdr.batch   = YES 
    gl-jouhdr.jtype   = 1 
    new-hdr           = YES
  . 
END. 
 
PROCEDURE create-journals: 
  FOR EACH g-list NO-LOCK: 
    CREATE gl-journal. 
    ASSIGN
      gl-journal.jnr        = gl-jouhdr.jnr
      gl-journal.fibukonto  = g-list.fibukonto 
      gl-journal.debit      = g-list.debit
      gl-journal.credit     = g-list.credit 
      gl-journal.bemerk     = g-list.bemerk 
      gl-journal.userinit   = g-list.userinit 
      gl-journal.zeit       = g-list.zeit
    . 
  END. 
  DO transaction: 
    IF remains = 0.01 OR remains = - 0.01 THEN remains = 0. 
    FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK. 
    ASSIGN
      gl-jouhdr.credit = credits
      gl-jouhdr.debit  = debits 
      gl-jouhdr.remain = remains
    . 
    FIND CURRENT gl-jouhdr NO-LOCK. 
  END. 
  RELEASE gl-jouhdr. 
  DO TRANSACTION: 
    FIND FIRST htparam WHERE paramnr = 1003 EXCLUSIVE-LOCK. 
    /* LAST FO Transfer DATE */ 
    htparam.fdate = to-date. 
    FIND CURRENT htparam NO-LOCK. 
  END. 
END. 
