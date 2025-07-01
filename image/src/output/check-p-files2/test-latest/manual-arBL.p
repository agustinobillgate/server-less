
DEF TEMP-TABLE s-list 
    FIELD fibukonto LIKE gl-acct.fibukonto INITIAL "000000000000" 
    FIELD debit     LIKE gl-journal.debit 
    FIELD credit    LIKE gl-journal.credit. 


DEFINE INPUT  PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER TABLE FOR s-list.
DEFINE INPUT  PARAMETER rgdatum         AS DATE.
DEFINE INPUT  PARAMETER firma           AS CHAR.
DEFINE INPUT  PARAMETER art-fibukonto   AS CHAR.
DEFINE INPUT  PARAMETER user-init       AS CHAR.
DEFINE INPUT  PARAMETER invoice         AS INT.
DEFINE INPUT  PARAMETER saldo           AS DECIMAL.
DEFINE INPUT  PARAMETER refno           LIKE gl-jouhdr.refno.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "manual-ar". 

DEFINE BUFFER sbuff FOR s-list.

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
    gl-jouhdr.refno = refno 
    gl-jouhdr.datum = rgdatum 
    gl-jouhdr.bezeich = firma 
    gl-jouhdr.batch = YES 
    gl-jouhdr.jtype = 2 
    . 
CREATE gl-journal. 
ASSIGN 
    gl-journal.jnr = gl-jouhdr.jnr 
    gl-journal.fibukonto = art-fibukonto 
    gl-journal.userinit = user-init 
    gl-journal.zeit = TIME 
    gl-journal.bemerk = STRING(invoice)
    . 
IF saldo GT 0 THEN gl-journal.debit = saldo.
ELSE gl-journal.credit = - saldo.

gl-jouhdr.credit = gl-jouhdr.credit + gl-journal.credit.
gl-jouhdr.debit = gl-jouhdr.debit + gl-journal.debit.
FOR EACH sbuff WHERE DECIMAL(sbuff.fibukonto) NE 0:
    CREATE gl-journal. 
    ASSIGN 
         gl-journal.jnr = gl-jouhdr.jnr 
         gl-journal.fibukonto = sbuff.fibukonto 
         gl-journal.userinit = user-init 
         gl-journal.zeit = TIME 
         gl-journal.bemerk = STRING(invoice )
         gl-journal.debit = sbuff.debit 
         gl-journal.credit = sbuff.credit 
       . 
    gl-jouhdr.credit = gl-jouhdr.credit + gl-journal.credit. 
    gl-jouhdr.debit = gl-jouhdr.debit + gl-journal.debit. 
    FIND CURRENT gl-journal NO-LOCK. 
END.
FIND CURRENT gl-jouhdr NO-LOCK.
