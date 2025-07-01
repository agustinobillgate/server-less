DEFINE INPUT PARAMETER nr-budget        AS INTEGER.
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
    RUN delete-it.
END.
ELSE
    err-mark = "budget-fix-asset-is-not-found".

PROCEDURE delete-it:

    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.

    CREATE res-history. 
    ASSIGN 
        res-history.nr        = bediener.nr 
        res-history.datum     = TODAY 
        res-history.zeit      = TIME 
        res-history.action    = "Fix Asset Budget"
        res-history.aenderung = "Delete Fix Asset Budget with number " + STRING(nr-budget) + 
                                " as " + queasy.char1 + ", date: " + STRING(queasy.date1) + 
                                ", amount: " + STRING(queasy.logi1) + ", status: " + convert-status(queasy.logi1)
    .
    
    FIND FIRST queasy WHERE RECID(queasy) EQ rec-id EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        DELETE queasy.
    END.
END.
