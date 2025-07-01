DEF INPUT  PARAMETER bookengID AS INT.
FIND FIRST queasy WHERE queasy.KEY = 167 AND queasy.number1 = bookengID NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK NO-WAIT.
    queasy.date1 = TODAY.
    queasy.logi1 = YES.
    RELEASE queasy.
END.
