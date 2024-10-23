
DEF INPUT  PARAMETER rechnr  AS INT.
DEF OUTPUT PARAMETER bilflag AS INT.
DEF OUTPUT PARAMETER rec-id  AS INT.
DEF OUTPUT PARAMETER zinr    AS CHAR.

FIND FIRST vhp.bill WHERE vhp.bill.rechnr = rechnr NO-LOCK. 
bilflag = vhp.bill.flag.
rec-id = RECID(bill).
zinr = bill.zinr.
