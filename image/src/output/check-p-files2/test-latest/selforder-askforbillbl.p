DEFINE INPUT PARAMETER session-parameter AS CHAR.
DEFINE INPUT PARAMETER outlet-number AS INT.
DEFINE OUTPUT PARAMETER mess-result AS CHAR.

IF session-parameter EQ "" OR session-parameter EQ ? THEN
DO:
    mess-result = "1-Session Param can't be null".
    RETURN.
END.
IF outlet-number EQ 0 OR outlet-number EQ ? THEN
DO:
    mess-result = "1-Outlet can't be null".
    RETURN.
END.

DO TRANSACTION:
    FIND FIRST queasy WHERE queasy.KEY EQ 225 
        AND queasy.char1 EQ "orderbill"
        AND queasy.number1 EQ outlet-number 
        AND queasy.char3 EQ session-parameter 
        AND queasy.logi1 EQ YES /*EXCLUSIVE-LOCK*/ NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN queasy.logi2 = YES.
        mess-result = "0-Ask For Bill Success".
        FIND CURRENT queasy NO-LOCK.
    END.
    ELSE
    DO:
        mess-result = "1-No Record Found!Ask for Bill Failed".
    END.    
    RELEASE queasy.
END.

