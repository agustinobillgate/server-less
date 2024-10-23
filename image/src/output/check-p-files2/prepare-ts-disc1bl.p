
DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.
/*MTDEF TEMP-TABLE t-h-bill-line LIKE h-bill-line.*/

DEF INPUT  PARAMETER room AS CHAR.
DEF INPUT  PARAMETER dept AS INT.
DEF INPUT  PARAMETER tischnr AS INT.

DEF OUTPUT PARAMETER disc-alert AS LOGICAL NO-UNDO INIT YES.
DEF OUTPUT PARAMETER disc-service AS LOGICAL.
DEF OUTPUT PARAMETER disc-tax AS LOGICAL.
DEF OUTPUT PARAMETER voucher-art AS INT.
DEF OUTPUT PARAMETER disc-art1 AS INT.
DEF OUTPUT PARAMETER disc-art2 AS INT.
DEF OUTPUT PARAMETER disc-art3 AS INT.
DEF OUTPUT PARAMETER prefix-rm AS CHAR.
DEF OUTPUT PARAMETER procent AS DECIMAL.
/*MTDEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL.

DEF OUTPUT PARAMETER p-134 AS LOGICAL.
DEF OUTPUT PARAMETER p-135 AS LOGICAL.
DEF OUTPUT PARAMETER p-479 AS LOGICAL.*/

DEF OUTPUT PARAMETER TABLE FOR t-h-bill.
/*MTDEF OUTPUT PARAMETER TABLE FOR t-h-bill-line.*/

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 1203 NO-LOCK.
IF vhp.htparam.paramgr = 19 AND vhp.htparam.feldtyp = 4 THEN
ASSIGN disc-alert = vhp.htparam.flogical.


FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 468 NO-LOCK. 
  /* disc reduce service? */ 
disc-service = flogical. 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 469 NO-LOCK. 
  /* disc reduce vat? */ 
disc-tax = flogical. 


FIND FIRST vhp.htparam WHERE paramnr = 1001 NO-LOCK. 
voucher-art = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. 
disc-art1 = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 596 NO-LOCK. 
disc-art2 = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 556 NO-LOCK. 
disc-art3 = vhp.htparam.finteger. 


FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 790 no-lock. /* Sea Garden */ 
IF vhp.htparam.finteger NE 0 THEN 
DO: 
  prefix-rm = STRING(vhp.htparam.finteger). 
  IF SUBSTR(room, 1, 1) = prefix-rm THEN 
  DO: 
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 791 NO-LOCK NO-ERROR. 
    procent = vhp.htparam.fdecimal. 
  END. 
END. 


FIND FIRST vhp.h-bill WHERE vhp.h-bill.departement = dept 
  AND vhp.h-bill.tischnr = tischnr AND vhp.h-bill.flag = 0 NO-LOCK NO-ERROR.
IF AVAILABLE vhp.h-bill THEN DO: /*Fix err Log APPSERVER EKO @11Apr2016*/
    CREATE t-h-bill.
    BUFFER-COPY h-bill TO t-h-bill. 
    ASSIGN t-h-bill.rec-id = RECID(h-bill).
END.

/*MT
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 491 NO-LOCK. 
price-decimal = vhp.htparam.finteger. 
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 144 NO-LOCK. 
FIND FIRST vhp.waehrung WHERE vhp.waehrung.wabkurz = vhp.htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE vhp.waehrung THEN exchg-rate = vhp.waehrung.ankauf / vhp.waehrung.einheit. 
ELSE exchg-rate = 1.

FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr 
    AND vhp.h-bill-line.departement = dept NO-LOCK BY vhp.h-bill-line.bezeich:
    CREATE t-h-bill-line.
    BUFFER-COPY h-bill-line TO t-h-bill-line.
END.


FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK. 
p-134 = vhp.htparam.flogical. 
FIND FIRST vhp.htparam WHERE paramnr = 135 NO-LOCK. 
p-135 = vhp.htparam.flogical. 
FIND FIRST vhp.htparam WHERE paramnr = 479 NO-LOCK. 
p-479 = vhp.htparam.flogical. 
*/
