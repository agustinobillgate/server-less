
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER err AS INT INIT 0.

FIND FIRST akt-code WHERE RECID(akt-code) = rec-id.
FIND FIRST akthdr WHERE akthdr.referred = akt-code.aktionscode 
     NO-LOCK NO-ERROR. 
IF AVAILABLE akthdr THEN err = 1.
ELSE 
DO: 
    FIND CURRENT akt-code EXCLUSIVE-LOCK. 
    delete akt-code.
END.
