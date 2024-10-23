
DEF INPUT  PARAMETER bil-recid AS INT.

FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK.

FIND CURRENT bill EXCLUSIVE-LOCK NO-ERROR. 
bill.rgdruck = 1. 
bill.printnr = bill.printnr + 1. 
FIND CURRENT bill NO-LOCK NO-ERROR. 
