
DEF INPUT PARAMETER a-gastnr AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER err AS INT INIT 0.

FIND FIRST akt-cust WHERE RECID(akt-cust) = rec-id.
FIND FIRST akthdr WHERE akthdr.gastnr = a-gastnr 
  NO-LOCK NO-ERROR. 
IF AVAILABLE akthdr THEN err = 1.
FIND CURRENT akt-cust EXCLUSIVE-LOCK. 
DELETE akt-cust. 
