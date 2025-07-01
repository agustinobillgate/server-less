
DEF INPUT PARAMETER rec-id AS INT.

/* Malik Serverless 809 change query 
FIND FIRST parameters WHERE RECID(parameters) = rec-id EXCLUSIVE-LOCK.
delete parameters. */

FIND FIRST parameters WHERE RECID(parameters) = rec-id NO-LOCK NO-ERROR.
IF AVAILABLE parameters THEN 
DO:
    FIND CURRENT parameters EXCLUSIVE-LOCK.
    delete parameters.
    RELEASE parameters.
END.
