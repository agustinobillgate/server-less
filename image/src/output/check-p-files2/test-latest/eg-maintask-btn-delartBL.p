
DEF INPUT PARAMETER maintask-number1 AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER egprop FOR eg-property.
DEF BUFFER egreq FOR eg-Request.
DEF BUFFER egsub FOR eg-subtask.

FIND FIRST egsub WHERE egsub.main-nr  = maintask-number1 /*ANDegsub.reserve-int = "" */ NO-LOCK NO-ERROR.
IF AVAILABLE egsub THEN
DO:
    FIND FIRST egprop WHERE egprop.maintask = maintask-number1 NO-LOCK NO-ERROR.
    IF AVAILABLE egprop THEN
    DO:
        fl-code = 1.
        RETURN.  
    END.
    FIND FIRST queasy WHERE RECID(queasy) = rec-id NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.  
        DELETE queasy.
    END.
END.


