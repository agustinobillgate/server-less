
DEF INPUT  PARAMETER bil-recid AS INT.

FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK. /* Malik Serverless NO-LOCK -> NO-LOCK NO-ERROR */

/* Malik Serverless */
IF AVAILABLE bill THEN
DO:
    FIND CURRENT bill EXCLUSIVE-LOCK NO-ERROR. 
    bill.rgdruck = 1. 
    bill.printnr = bill.printnr + 1. 
    FIND CURRENT bill NO-LOCK NO-ERROR. 
END.
/* END Malik */

/* Uncomment for serverless 
FIND CURRENT bill EXCLUSIVE-LOCK NO-ERROR. 
bill.rgdruck = 1. 
bill.printnr = bill.printnr + 1. 
FIND CURRENT bill NO-LOCK NO-ERROR. 

*/
