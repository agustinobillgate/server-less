DEFINE INPUT PARAMETER curr-nr AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER rec-id  AS INTEGER NO-UNDO.

DEFINE BUFFER hbuff FOR hoteldpt.

FIND FIRST mc-disc WHERE mc-disc.nr = curr-nr 
    AND RECID(mc-disc) = rec-id NO-LOCK NO-ERROR.
IF AVAILABLE mc-disc THEN DO:
    FIND CURRENT mc-disc EXCLUSIVE-LOCK.
    DELETE mc-disc.
    RELEASE mc-disc.    
END.
