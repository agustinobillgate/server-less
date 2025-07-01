DEFINE TEMP-TABLE param-list LIKE parameters 
    FIELD recid-param AS INTEGER.
.


DEFINE INPUT PARAMETER recid-param AS INTEGER NO-UNDO.

FIND FIRST parameters WHERE RECID(parameters) = recid-param NO-LOCK NO-ERROR. /* Malik Serverless : gak ada -> NO-LOCK NO-ERROR */
/* Malik Serverless */
IF AVAILABLE parameters THEN
DO:
    FIND CURRENT parameters EXCLUSIVE-LOCK.
    DELETE parameters.    
    RELEASE parameters.
END.
/* END Malik */
/* DELETE parameters. */

