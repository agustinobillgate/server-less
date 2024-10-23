DEFINE INPUT PARAMETER usersession AS CHAR.
DEFINE INPUT PARAMETER command-string AS CHAR.
DEFINE INPUT PARAMETER gastnr AS INT.
DEFINE INPUT PARAMETER scanner-number AS INT.


FIND FIRST queasy WHERE queasy.KEY EQ 284 
    AND queasy.char1 EQ usersession 
    AND queasy.number2 EQ scanner-number NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY     = 284
        queasy.char1   = usersession
        queasy.char2   = command-string
        queasy.logi1   = NO
        queasy.number1 = gastnr
        queasy.number2 = scanner-number
        .
    RELEASE queasy.
END.
ELSE
DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    ASSIGN 
        queasy.char2 = command-string
        queasy.logi1 = NO.
    FIND CURRENT queasy NO-LOCK.
    RELEASE queasy.
END.
