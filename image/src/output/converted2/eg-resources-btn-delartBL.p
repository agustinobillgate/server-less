
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER resources-nr AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER eg-req FOR eg-cost.

FIND FIRST eg-req WHERE eg-req.resource-nr = resources-nr NO-LOCK NO-ERROR.
IF AVAILABLE eg-req THEN
DO:
    fl-code = 1.
    RETURN NO-APPLY.  
END.
/* Malik Serverless 801 add if available */
FIND FIRST eg-resources WHERE RECID(eg-resources) = rec-id NO-LOCK NO-ERROR.
IF AVAILABLE eg-resources THEN
DO:
    FIND CURRENT eg-resources EXCLUSIVE-LOCK.
    DELETE eg-resources.  
    RELEASE eg-resources.
END.
