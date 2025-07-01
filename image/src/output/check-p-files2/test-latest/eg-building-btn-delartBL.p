
DEF INPUT PARAMETER build-number1 AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER egbuilding FOR eg-Location.

FIND FIRST egbuilding WHERE egbuilding.building = build-number1 NO-LOCK NO-ERROR.
IF AVAILABLE egbuilding THEN
DO:
    fl-code = 1.
    RETURN NO-APPLY.  
END.

FIND FIRST queasy WHERE RECID(queasy) = rec-id.
FIND CURRENT queasy EXCLUSIVE-LOCK.  
DELETE queasy.
