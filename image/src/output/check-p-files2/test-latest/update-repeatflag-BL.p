
FIND FIRST queasy WHERE queasy.KEY = 167 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    queasy.date1 = TODAY.
    queasy.logi1 = YES.
    RELEASE queasy.
END.
ELSE
DO :
    CREATE queasy.
    ASSIGN
        queasy.KEY = 167
        queasy.date1 = TODAY
        queasy.logi1 = YES.
END.
