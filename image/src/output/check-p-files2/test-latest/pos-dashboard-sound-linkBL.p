DEFINE INPUT PARAMETER sound-link AS CHARACTER.
DEFINE OUTPUT PARAMETER v-success AS LOGICAL INITIAL NO.

FIND FIRST queasy WHERE queasy.KEY EQ 299 
    AND queasy.number1 EQ 1
    AND queasy.char1 EQ "SelfOrder-Sound" EXCLUSIVE-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN
        queasy.KEY = 299
        queasy.number1 = 1
        queasy.char1 = "SelfOrder-Sound"
        queasy.char2 = sound-link
        .
END.
ELSE
DO:
    queasy.char2 = sound-link.    
END.
FIND CURRENT queasy NO-LOCK.
RELEASE queasy.
v-success = YES.
