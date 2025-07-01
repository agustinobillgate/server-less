DEFINE INPUT  PARAMETER number1        AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str        AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER success-flag   AS LOGICAL NO-UNDO INIT NO.

/*FIND FIRST queasy WHERE queasy.KEY = 189 AND queasy.number1 = number1 
    EXCLUSIVE-LOCK. 
DELETE queasy. 
success-flag = YES.*/

/*Alder - Serverless - Issue 720 - Start*/
FIND FIRST queasy WHERE queasy.KEY EQ 189 AND queasy.number1 EQ number1 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    DELETE queasy.
    RELEASE queasy.
    ASSIGN success-flag = YES.
END.
/*Alder - Serverless - Issue 720 - End*/
 
