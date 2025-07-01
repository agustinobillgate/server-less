
DEF INPUT PARAMETER maintask-number1 AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER egReq FOR eg-Request.
DEF BUFFER egSub FOR eg-subtask.
DEF BUFFER egprop FOR eg-property.

FIND FIRST egReq WHERE egReq.maintask = maintask-number1 NO-LOCK NO-ERROR.
FIND FIRST egSub WHERE egSub.main-nr  = maintask-number1 NO-LOCK NO-ERROR.
FIND FIRST egprop WHERE egprop.maintask = maintask-number1 NO-LOCK NO-ERROR.

IF AVAILABLE egprop OR AVAILABLE egReq OR AVAILABLE egSub THEN
    fl-code = 1.
