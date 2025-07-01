
DEF INPUT PARAMETER actionnr AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER egreq FOR eg-mdetail. /*Alder - Serverless - Issue 805*/

FIND FIRST egreq WHERE egreq.KEY EQ 1 AND egreq.nr EQ actionnr NO-LOCK NO-ERROR.
IF AVAILABLE egreq THEN
DO:
    fl-code = 1.
    RETURN NO-APPLY.  
END.

/*Alder - Serverless - Issue 805*/
FIND FIRST eg-action WHERE RECID(eg-action) EQ rec-id NO-LOCK NO-ERROR.
IF AVAILABLE eg-action THEN
DO:
    FIND CURRENT eg-action EXCLUSIVE-LOCK.  
    DELETE eg-action.  
    RELEASE eg-action. 
END.
/*Alder - Serverless - Issue 805*/
