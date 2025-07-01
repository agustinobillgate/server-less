
DEF INPUT PARAMETER duration-nr AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER egsub FOR eg-subtask. /*Alder - Serverless - Issue 804*/

FIND FIRST egsub WHERE egsub.dur-nr = duration-nr NO-LOCK NO-ERROR.
IF AVAILABLE egsub THEN
DO:
    fl-code = 1.
    RETURN NO-APPLY.  
END.

/*Alder - Serverless - Issue 804 - Start*/
FIND FIRST eg-duration WHERE RECID(eg-duration) EQ rec-id NO-LOCK NO-ERROR.
IF AVAILABLE eg-duration THEN
DO:
    FIND CURRENT eg-duration EXCLUSIVE-LOCK.  
    DELETE eg-duration.  
    RELEASE eg-duration.
END.
/*Alder - Serverless - Issue 804 - End*/
