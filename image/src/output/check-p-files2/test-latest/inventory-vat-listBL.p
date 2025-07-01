
DEFINE INPUT PARAMETER caseType     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER nr           AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER bezeich      AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER vatValue     AS DECIMAL NO-UNDO.
DEFINE INPUT PARAMETER fibukonto    AS CHAR    NO-UNDO.

DEFINE OUTPUT PARAMETER successFlag AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR    NO-UNDO.


IF caseType = 1 THEN /*add*/
DO:
    FIND FIRST queasy WHERE queasy.KEY = 303 
        AND queasy.number1 = nr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN DO:
        ASSIGN successFlag = NO
               msg-str     = "Tax value with No . " + STRING(nr) + " is already exist."
            .
    END.
    ELSE IF NOT AVAILABLE queasy THEN DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY     = 303 
            queasy.number1 = nr        
            queasy.char1   = bezeich   
            queasy.deci1   = vatValue 
            queasy.char2   = fibukonto 
            successFlag    = YES
         .
    END.
END.
ELSE IF caseType = 2 THEN /*modify*/
DO:
    FIND FIRST queasy WHERE queasy.KEY = 303
        AND queasy.number1 = nr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN 
            queasy.char1   = bezeich   
            queasy.deci1   = vatValue 
            queasy.char2   = fibukonto 
            successFlag    = YES
        .
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.         
END.
ELSE IF caseType = 3 THEN /*delete*/
DO:
    FIND FIRST queasy WHERE queasy.KEY = 303
        AND queasy.number1 = nr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        DELETE queasy.
        RELEASE queasy.
    END.
END.

