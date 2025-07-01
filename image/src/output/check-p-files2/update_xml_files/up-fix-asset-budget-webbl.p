DEFINE INPUT PARAMETER nr-budget        AS INTEGER.
DEFINE INPUT PARAMETER desc-budget      AS CHAR.
DEFINE INPUT PARAMETER date-budget      AS DATE.
DEFINE INPUT PARAMETER amount-budget    AS DECIMAL.
DEFINE INPUT PARAMETER is-active-budget AS LOGICAL.
DEFINE INPUT PARAMETER user-init        AS CHARACTER.
DEFINE OUTPUT PARAMETER err-mark        AS CHAR INITIAL "".

DEFINE VARIABLE rec-id AS INTEGER.

/* #################### START OF DEFINE FUNCTION ################### */

FUNCTION convert-status RETURNS CHARACTER (INPUT statusInp AS LOGICAL):
    IF statusInp THEN
        RETURN "Active".
    ELSE
        RETURN "Deactive".
END FUNCTION.

/* ##################### END OF DEFINE FUNCTION ##################### */

FIND FIRST queasy WHERE queasy.key EQ 324 AND queasy.number1 EQ nr-budget NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    rec-id = RECID(queasy).
    RUN update-it.
END.
ELSE
    err-mark = "budget-fix-asset-is-not-found".

PROCEDURE update-it:

    DEFINE VARIABLE oldStatus AS CHARACTER INITIAL "".

    oldStatus = queasy.char1 + ", date: " + STRING(queasy.date1) + 
                ", amount: " + STRING(queasy.deci1) + 
                ", status: " + convert-status(queasy.logi1).

    FIND FIRST queasy WHERE RECID(queasy) EQ rec-id NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN
            queasy.char1   = desc-budget
            queasy.date1   = date-budget
            queasy.deci1   = amount-budget
            queasy.logi1   = is-active-budget
        .
        
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.

    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    CREATE res-history. 
    ASSIGN 
        res-history.nr        = bediener.nr 
        res-history.datum     = TODAY 
        res-history.zeit      = TIME 
        res-history.action    = "Fix Asset Budget"
        res-history.aenderung = "Modify Fix Asset Budget with number " + STRING(nr-budget) + 
                                " from " + oldStatus + " to " + desc-budget + ", date: " + STRING(date-budget) + 
                                ", amount: " + STRING(amount-budget) + ", status: " + convert-status(is-active-budget)
    .
END.
