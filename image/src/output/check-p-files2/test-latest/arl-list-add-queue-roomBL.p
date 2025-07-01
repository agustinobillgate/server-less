DEF INPUT PARAMETER roomno      AS CHAR NO-UNDO.
DEF INPUT PARAMETER user-init   AS CHAR NO-UNDO.

FIND FIRST queasy WHERE queasy.KEY = 162
    AND queasy.char1 = roomno NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN
        queasy.KEY      = 162
        queasy.char1    = roomno
    .
END.
ASSIGN        
    queasy.char2    = user-init
    queasy.number1  = 0
    queasy.number2  = TIME
    queasy.date2    = TODAY
    .
FIND CURRENT queasy NO-LOCK.
