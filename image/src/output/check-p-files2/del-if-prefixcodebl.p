DEFINE TEMP-TABLE param-list LIKE parameters 
    FIELD recid-param AS INTEGER.
.


DEFINE INPUT PARAMETER recid-param AS INTEGER NO-UNDO.

FIND FIRST parameters WHERE RECID(parameters) = recid-param .
DELETE parameters.
