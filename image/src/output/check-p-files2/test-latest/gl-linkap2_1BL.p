
DEFINE TEMP-TABLE g-list 
  FIELD  nr         AS INTEGER 
  FIELD  remark     AS CHAR 
  FIELD  docu-nr    AS CHAR 
  FIELD  lscheinnr  AS CHAR 
  FIELD  jnr        LIKE gl-journal.jnr 
  FIELD  fibukonto  LIKE gl-journal.fibukonto 
  FIELD  debit      LIKE gl-journal.debit 
  FIELD  credit     LIKE gl-journal.credit 
  FIELD  bemerk     AS CHAR FORMAT "x(32)" 
  FIELD  userinit   LIKE gl-journal.userinit 
  FIELD  sysdate    LIKE gl-journal.sysdate INITIAL today 
  FIELD  zeit       LIKE gl-journal.zeit 
  FIELD  chginit    LIKE gl-journal.chginit 
  FIELD  chgdate    LIKE gl-journal.chgdate INITIAL ? 
  FIELD  duplicate  AS LOGICAL INITIAL YES
  FIELD  acct-fibukonto  LIKE gl-acct.fibukonto
  FIELD  bezeich    LIKE gl-acct.bezeich.

DEF INPUT PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER remains         AS DECIMAL.
DEF INPUT PARAMETER credits         AS DECIMAL.
DEF INPUT PARAMETER debits          AS DECIMAL.
DEF INPUT PARAMETER to-date         AS DATE.
DEF INPUT PARAMETER c-refno         AS CHAR.
DEF INPUT PARAMETER c-bezeich       AS CHAR.
DEF INPUT PARAMETER TABLE FOR g-list.
DEF OUTPUT PARAMETER msg-str        AS CHAR.

DEFINE VARIABLE new-hdr AS LOGICAL INITIAL YES. 
DEFINE VARIABLE hdr-found AS LOGICAL INITIAL NO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-linkap2_1".

RUN verify-refno.       /* CHIRAG 26AUG2019 (PENAMBAHAN VALIDASI UNTUK KEBUTUHAN VHPWEB) */
IF hdr-found = YES THEN
    RETURN.
RUN create-header. 
RUN create-journals.

PROCEDURE verify-refno:

    msg-str = "".
    FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno = c-refno NO-LOCK NO-ERROR.
    IF AVAILABLE gl-jouhdr THEN
    DO:
        msg-str = "Refno " + c-refno + " Already Exists: " + STRING(gl-jouhdr.datum) + " " + gl-jouhdr.bezeich.
        hdr-found = YES.
    END.

END PROCEDURE.

PROCEDURE create-header: 
  CREATE gl-jouhdr. 
  FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE counters THEN 
  DO: 
    CREATE counters. 
    counters.counter-no = 25. 
    counters.counter-bez = translateExtended ("G/L Transaction Journal",lvCAREA,""). 
  END. 
  counters.counter    = counters.counter + 1.
  FIND CURRENT counter NO-LOCK.

  ASSIGN
    gl-jouhdr.jnr       = counters.counter
    gl-jouhdr.refno     = c-refno
    gl-jouhdr.datum     = to-date
    gl-jouhdr.bezeich   = c-bezeich 
    gl-jouhdr.batch     = YES 
    gl-jouhdr.jtype     = 4 
    new-hdr             = YES
  . 
END. 
 
PROCEDURE create-journals: 
  FOR EACH g-list NO-LOCK:
      CREATE gl-journal.
      ASSIGN
        gl-journal.jnr          = counters.counter
        gl-journal.fibukonto    = g-list.fibukonto 
        gl-journal.debit        = g-list.debit
        gl-journal.credit       = g-list.credit
        gl-journal.bemerk       = g-list.bemerk 
        gl-journal.userinit     = g-list.userinit 
        gl-journal.zeit         = g-list.zeit
      . 
  END. 
  DO TRANSACTION: 
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
    FIND FIRST htparam WHERE paramnr = 1118 EXCLUSIVE-LOCK. 
    /* LAST A/P Transfer DATE */ 
    htparam.fdate = to-date. 
    FIND CURRENT htparam NO-LOCK. 
  END. 
END. 
