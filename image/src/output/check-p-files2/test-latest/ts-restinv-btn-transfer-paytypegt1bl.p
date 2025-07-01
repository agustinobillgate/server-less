DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF INPUT PARAMETER bilrecid AS INT.
DEF INPUT PARAMETER h-bill-recid AS INT.
DEF INPUT PARAMETER balance-foreign AS DECIMAL.
DEF INPUT PARAMETER balance AS DECIMAL.
DEF INPUT PARAMETER pay-type AS INT.

DEF OUTPUT PARAMETER billart AS INT.
DEF OUTPUT PARAMETER qty AS INT.
DEF OUTPUT PARAMETER price AS DECIMAL.
DEF OUTPUT PARAMETER amount-foreign LIKE vhp.bill-line.betrag.
DEF OUTPUT PARAMETER amount LIKE vhp.bill-line.betrag.
DEF OUTPUT PARAMETER gname AS CHAR.
DEF OUTPUT PARAMETER description AS CHAR.
DEF OUTPUT PARAMETER transfer-zinr AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

  FIND FIRST vhp.bill WHERE RECID(bill) = bilrecid NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE bill THEN RETURN. /*FT serverless*/
  FIND FIRST h-bill WHERE RECID(h-bill) = h-bill-recid NO-LOCK NO-ERROR.
  IF NOT AVAILABLE h-bill THEN RETURN. /*FT serverless*/
  billart = 0. 
  qty = 1. 
  price = 0. 
  amount-foreign = - balance-foreign. 
  amount = - balance. 
  gname = "". 

  IF vhp.bill.rechnr = 0 THEN 
  DO: 
    FIND FIRST vhp.counters WHERE vhp.counters.counter-no = 3 
      EXCLUSIVE-LOCK. 
    vhp.counters.counter = vhp.counters.counter + 1. 
    FIND CURRENT counter NO-LOCK. 
    FIND CURRENT vhp.bill EXCLUSIVE-LOCK. 
    vhp.bill.rechnr = vhp.counters.counter. 
    FIND CURRENT vhp.bill NO-LOCK. 
  END. 

  IF pay-type = 2 THEN     /* room transfer */ 
  DO: 
    description = "RmNo " + vhp.bill.zinr + " *" + STRING(bill.rechnr). 
    transfer-zinr = vhp.bill.zinr. 
    FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = vhp.bill.resnr 
      AND vhp.res-line.reslinnr = vhp.bill.reslinnr NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.res-line AND AVAILABLE vhp.h-bill THEN 
    DO: 
      gname = vhp.res-line.name. 
      FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
      vhp.h-bill.bilname = gname. 
      FIND CURRENT vhp.h-bill NO-LOCK. 
    END. 
    CREATE t-h-bill.
    BUFFER-COPY h-bill TO t-h-bill.
    ASSIGN t-h-bill.rec-id = RECID(h-bill).
  END. 
  ELSE IF pay-type = 3 OR pay-type = 4 THEN 
  DO: 
    description = "Transfer" + " *" + STRING(bill.rechnr). 
    gname = vhp.bill.name. 
    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
    vhp.h-bill.bilname = gname. 
    FIND CURRENT vhp.h-bill NO-LOCK. 
    CREATE t-h-bill.
    BUFFER-COPY h-bill TO t-h-bill.
    ASSIGN t-h-bill.rec-id = RECID(h-bill).
  END.


