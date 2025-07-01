DEFINE INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER number1        AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str        AS CHARACTER NO-UNDO.
DEFINE OUTPUT PARAMETER success-flag   AS LOGICAL NO-UNDO INIT NO.

{SupertransBL.i}
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "room-category-admin".

FIND FIRST zimkateg WHERE zimkateg.typ = number1 NO-LOCK NO-ERROR. 
IF AVAILABLE zimkateg  THEN 
DO: 
   msg-str = msg-str + CHR(2)
           + translateExtended ("Room Type exists, deleting not possible:",lvCAREA,"")
           + " " + zimkateg.kurzbez.
END. 
ELSE 
DO: 
    /*FIND FIRST queasy WHERE queasy.KEY = 152 AND queasy.number1 = number1 
    EXCLUSIVE-LOCK. 
    DELETE queasy. 
    success-flag = YES.*/
    
    /*Alder - Serverless - Issue 722 - Start*/
    FIND FIRST queasy WHERE queasy.KEY EQ 152 AND queasy.number1 EQ number1 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        DELETE queasy.
        RELEASE queasy.
        ASSIGN success-flag = YES.
    END.
    /*Alder - Serverless - Issue 722 - End*/
END. 
