
DEF INPUT PARAMETER desc-cj     AS CHAR.
DEF INPUT PARAMETER credit      AS DECIMAL.
DEF INPUT PARAMETER debit       AS DECIMAL.
DEF INPUT PARAMETER remain      AS DECIMAL.
DEF INPUT PARAMETER jnr         AS INT.
DEF INPUT PARAMETER user-init   AS CHAR.
DEF INPUT PARAMETER datum       AS DATE.
DEF INPUT PARAMETER refno       AS CHAR.

DEFINE BUFFER gl-jnal FOR gl-journal. 
DEFINE BUFFER gl-jou  FOR gl-journal. 
DEFINE BUFFER gl-hdr  FOR gl-jouhdr. 

DO transaction: 
    create gl-hdr. 
    FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE counters THEN 
    DO: 
      create counters. 
      counters.counter-no = 25. 
      counters.counter-bez = "G/L Transaction Journal". 
    END. 
    counters.counter = counters.counter + 1. 
    FIND CURRENT counter NO-LOCK. 
    gl-hdr.jnr = counters.counter. 
    gl-hdr.refno = refno. 
    gl-hdr.datum = datum. 
    gl-hdr.bezeich = desc-cj.
    gl-hdr.credit = credit. 
    gl-hdr.debit = debit. 
    gl-hdr.remain = remain. 
    FIND CURRENT gl-hdr NO-LOCK. 
    FOR EACH gl-jou WHERE gl-jou.jnr = jnr NO-LOCK: 
      create gl-jnal. 
      gl-jnal.jnr = counters.counter. 
      gl-jnal.fibukonto = gl-jou.fibukonto. 
      gl-jnal.debit = gl-jou.debit. 
      gl-jnal.bemerk = gl-jou.bemerk. 
      gl-jnal.credit = gl-jou.credit. 
      gl-jnal.userinit = user-init. 
      gl-jnal.zeit = time. 
    END.
END.
