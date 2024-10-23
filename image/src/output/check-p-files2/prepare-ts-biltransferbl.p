
DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER h-recid    AS INTEGER.

DEF OUTPUT PARAMETER multi-vat  AS LOGICAL.
DEF OUTPUT PARAMETER dept       AS INT.
DEF OUTPUT PARAMETER splitted   AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 271 NO-LOCK. 
IF vhp.htparam.feldtyp = 4 THEN multi-vat = vhp.htparam.flogical.

FIND FIRST vhp.h-bill WHERE RECID(vhp.h-bill) = h-recid NO-LOCK. 
dept = vhp.h-bill.departement. 
 
FIND FIRST vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr 
  AND vhp.h-bill-line.departement = dept AND vhp.h-bill-line.waehrungsnr GT 0 
  NO-LOCK NO-ERROR. 
IF AVAILABLE vhp.h-bill-line THEN splitted = YES.

CREATE t-h-bill.
BUFFER-COPY h-bill TO t-h-bill.
ASSIGN t-h-bill.rec-id = RECID(h-bill).
