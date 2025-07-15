
DEF INPUT PARAMETER maintask-number1 AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER eg-prop FOR eg-property. /* Malik Serverless 802 change name for tools conversion egProp -> eg-prop */
DEF BUFFER eg-req FOR eg-Request. /* Malik Serverless 802 change name for tools conversion egReq -> eg-req */
DEF BUFFER eg-sub FOR eg-subtask. /* Malik Serverless 802 change name for tools conversion egSub -> eg-sub */

FIND FIRST eg-sub WHERE eg-sub.main-nr  = maintask-number1 /*ANDeg-sub.reserve-int = "" */ NO-LOCK NO-ERROR.
IF AVAILABLE eg-sub THEN
DO:
    FIND FIRST eg-prop WHERE eg-prop.maintask = maintask-number1 NO-LOCK NO-ERROR.
    IF AVAILABLE eg-prop THEN
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


