DEF BUFFER rline FOR res-line.

DEF INPUT PARAMETER recid-rline AS INT.

FIND FIRST rline WHERE RECID(rline) = recid-rline NO-LOCK NO-ERROR.

IF AVAILABLE rline THEN
    DO TRANSACTION: 
        FIND CURRENT rline EXCLUSIVE-LOCK. 
        rline.betrieb-gast = rline.betrieb-gast + 1. 
        FIND CURRENT rline NO-LOCK. 
        RELEASE rline.
    END.
