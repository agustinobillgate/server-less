
DEF OUTPUT PARAMETER recid-l-ophdr AS INT.

DO transaction: 
    create l-ophdr.
    FIND CURRENT l-ophdr NO-LOCK.
END.
recid-l-ophdr = RECID(l-ophdr).
