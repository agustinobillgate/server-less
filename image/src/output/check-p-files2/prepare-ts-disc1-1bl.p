DEF TEMP-TABLE t-h-bill-line LIKE h-bill-line.

DEF INPUT  PARAMETER dept AS INT.
DEF INPUT  PARAMETER tischnr AS INT.

DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL.

DEF OUTPUT PARAMETER p-134 AS LOGICAL.
DEF OUTPUT PARAMETER p-135 AS LOGICAL.
DEF OUTPUT PARAMETER p-479 AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill-line.


FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 491 NO-LOCK. 
price-decimal = vhp.htparam.finteger. 
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 144 NO-LOCK. 
FIND FIRST vhp.waehrung WHERE vhp.waehrung.wabkurz = vhp.htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE vhp.waehrung THEN exchg-rate = vhp.waehrung.ankauf / vhp.waehrung.einheit. 
ELSE exchg-rate = 1. 
 
FIND FIRST vhp.h-bill WHERE vhp.h-bill.departement = dept 
  AND vhp.h-bill.tischnr = tischnr AND vhp.h-bill.flag = 0 NO-LOCK. 

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

