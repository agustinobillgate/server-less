
DEFINE TEMP-TABLE t-h-bill  LIKE h-bill
    FIELD rec-id AS INT.

DEF INPUT PARAMETER bilrecid        AS INT.
DEF INPUT PARAMETER recid-h-bill    AS INT.
DEF INPUT PARAMETER balance-foreign AS DECIMAL.
DEF INPUT PARAMETER balance         AS DECIMAL.
DEF INPUT PARAMETER pay-type        AS INT.

DEF OUTPUT PARAMETER billart        AS INT.
DEF OUTPUT PARAMETER qty            AS INT.
DEF OUTPUT PARAMETER price          AS DECIMAL.
DEF OUTPUT PARAMETER amount-foreign LIKE vhp.bill-line.betrag.
DEF OUTPUT PARAMETER amount         LIKE vhp.bill-line.betrag.
DEF OUTPUT PARAMETER description    AS CHAR.
DEF OUTPUT PARAMETER transfer-zinr  AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.  

  FIND FIRST vhp.bill WHERE RECID(bill) = bilrecid NO-LOCK. 
  billart = 0. 
  qty = 1. 
  price = 0. 
  amount-foreign = - balance-foreign. 
  amount = - balance. 

  /*FD November 04, 2021*/
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
  END. 
  ELSE IF pay-type = 3 OR pay-type = 4 THEN 
    description = "Transfer" + " *" + STRING(bill.rechnr).


FIND FIRST vhp.h-bill WHERE RECID(h-bill) = recid-h-bill EXCLUSIVE-LOCK.
ASSIGN vhp.h-bill.bilname = vhp.bill.NAME.
FIND CURRENT vhp.h-bill NO-LOCK.
CREATE t-h-bill.
BUFFER-COPY h-bill TO t-h-bill.
ASSIGN t-h-bill.rec-id = RECID(h-bill).
