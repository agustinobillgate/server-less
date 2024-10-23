
DEF INPUT PARAMETER maintask-number1 AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER egProp FOR eg-property.
DEF BUFFER egReq FOR eg-Request.
DEF BUFFER egSub FOR eg-subtask.

FIND FIRST egSub WHERE egSub.main-nr  = maintask-number1 /*ANDegSub.reserve-int = "" */ NO-LOCK NO-ERROR.
FIND FIRST egProp WHERE egProp.maintask = maintask-number1 NO-LOCK NO-ERROR.

IF AVAILABLE egProp /*egReq*/ OR AVAILABLE egSub THEN
DO:
    fl-code = 1.
    RETURN NO-APPLY.  
END.
FIND FIRST queasy WHERE RECID(queasy) = rec-id.
FIND CURRENT queasy EXCLUSIVE-LOCK.  
DELETE queasy.
