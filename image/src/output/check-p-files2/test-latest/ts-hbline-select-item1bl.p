
DEF INPUT  PARAMETER billdate    AS DATE.
DEF INPUT  PARAMETER dept        AS INT.
DEF INPUT  PARAMETER curr-rechnr AS INT.
DEF OUTPUT PARAMETER voucher     AS CHAR.

FIND LAST vhp.h-journal WHERE vhp.h-journal.bill-datum = billdate
  AND vhp.h-journal.departement = dept
  AND vhp.h-journal.rechnr = curr-rechnr 
  AND vhp.h-journal.wabkurz NE "" USE-INDEX kellner_ix NO-LOCK NO-ERROR.
IF AVAILABLE vhp.h-journal THEN voucher = vhp.h-journal.wabkurz.
