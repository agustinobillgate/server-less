DEFINE TEMP-TABLE g-list 
  FIELD docu-nr     AS CHAR 
  FIELD lscheinnr   AS CHAR 
  FIELD jnr         LIKE gl-journal.jnr 
  FIELD fibukonto   LIKE gl-journal.fibukonto 
  FIELD debit       LIKE gl-journal.debit 
  FIELD credit      LIKE gl-journal.credit 
  FIELD bemerk      AS CHAR FORMAT "x(32)" 
  FIELD userinit    LIKE gl-journal.userinit 
  FIELD sysdate     LIKE gl-journal.sysdate INITIAL today 
  FIELD zeit        LIKE gl-journal.zeit 
  FIELD chginit     LIKE gl-journal.chginit 
  FIELD chgdate     LIKE gl-journal.chgdate INITIAL ? 
  FIELD add-note    AS CHAR 
  FIELD duplicate   AS LOGICAL INITIAL YES
  FIELD acct-fibukonto  LIKE gl-acct.fibukonto
  FIELD bezeich    LIKE gl-acct.bezeich.

DEF INPUT PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT PARAMETER remains     AS DECIMAL.
DEF INPUT PARAMETER credits     AS DECIMAL.
DEF INPUT PARAMETER debits      AS DECIMAL.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER refno       AS CHAR.
DEF INPUT PARAMETER datum       AS DATE.
DEF INPUT PARAMETER bezeich     AS CHAR.
DEF INPUT PARAMETER TABLE FOR g-list.

DEFINE VARIABLE new-hdr AS LOGICAL INITIAL YES. 
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-linkcompli".

RUN create-header. 
RUN create-journals. 
FIND FIRST htparam WHERE paramnr = 1123 EXCLUSIVE-LOCK. 
fdate = to-date. 
FIND CURRENT htparam NO-LOCK. 

PROCEDURE create-header: 
  create gl-jouhdr. 
  FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE counters THEN 
  DO: 
    create counters. 
    counters.counter-no = 25. 
    counters.counter-bez = translateExtended ("G/L Transaction Journal",lvCAREA,""). 
  END. 
  counters.counter = counters.counter + 1.
  FIND CURRENT counter NO-LOCK.

  gl-jouhdr.jnr = counters.counter. 
  gl-jouhdr.refno = refno. 
  gl-jouhdr.datum = datum. 
  gl-jouhdr.bezeich = bezeich. 
  gl-jouhdr.batch = YES. 
  gl-jouhdr.jtype = 3. 
  new-hdr = YES. 

  /*ragung add for validasi closing*/
  FIND FIRST queasy WHERE queasy.KEY = 333
   AND queasy.char1   = refno
   AND queasy.char3   = "Compliment Journal"
  NO-LOCK NO-ERROR.
  IF NOT AVAILABLE queasy THEN DO:
      CREATE queasy.
      ASSIGN 
          queasy.KEY       = 333
          queasy.char1     = refno
          queasy.char2     = bezeich
          queasy.char3     = "Compliment Journal"
          queasy.date1     = datum
          queasy.number1   = jtype.           
  END.

END. 

PROCEDURE create-journals: 
  FOR EACH g-list  NO-LOCK: 
      create gl-journal. 
      gl-journal.jnr = counters.counter.
      gl-journal.fibukonto = g-list.fibukonto. 
      gl-journal.debit = ROUND(g-list.debit,2). 
      gl-journal.credit = ROUND(g-list.credit,2). 
      gl-journal.bemerk = g-list.bemerk + g-list.add-note. 
      gl-journal.userinit = g-list.userinit. 
      gl-journal.zeit = g-list.zeit. 
  END. 
  DO transaction: 
    IF remains = 0.01 OR remains = - 0.01 THEN remains = 0. 
    FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK. 
    gl-jouhdr.credit = credits. 
    gl-jouhdr.debit = debits. 
    gl-jouhdr.remain = remains. 
    FIND CURRENT gl-jouhdr NO-LOCK. 
  END. 
  release gl-jouhdr. 
/* WRONG !!! 
  DO transaction: 
    FIND FIRST htparam WHERE paramnr = 269 EXCLUSIVE-LOCK. 
    /* LAST FB Compliment - GL Transfer DATE */ 
    htparam.fdate = datum. 
    FIND CURRENT htparam NO-LOCK. 
  END. 
*/ 
END. 
