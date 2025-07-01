DEFINE INPUT PARAMETER nr-budget        AS INTEGER.
DEFINE INPUT PARAMETER desc-budget      AS CHAR.
DEFINE INPUT PARAMETER date-budget      AS DATE.
DEFINE INPUT PARAMETER amount-budget    AS DECIMAL.
DEFINE INPUT PARAMETER is-active-budget AS LOGICAL.
DEFINE INPUT PARAMETER user-init        AS CHARACTER.
DEFINE OUTPUT PARAMETER err-mark        AS CHAR INITIAL "".

/* #################### START OF DEFINE FUNCTION ################### */

FUNCTION convert-status RETURNS CHARACTER (INPUT statusInp AS LOGICAL):
    IF statusInp THEN
        RETURN "Active".
    ELSE
        RETURN "Deactive".
END FUNCTION.

/* ##################### END OF DEFINE FUNCTION ##################### */

FIND FIRST queasy WHERE queasy.key EQ 324 AND queasy.number1 EQ nr-budget NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    RUN create-it.
END.
ELSE
    err-mark = "number-is-used".

PROCEDURE create-it:
    CREATE queasy.
    ASSIGN
        queasy.key     = 324
        queasy.number1 = nr-budget
        queasy.char1   = desc-budget
        queasy.date1   = date-budget
        queasy.deci1   = amount-budget
        queasy.logi1   = is-active-budget
    .

    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    CREATE res-history. 
    ASSIGN 
        res-history.nr        = bediener.nr 
        res-history.datum     = TODAY 
        res-history.zeit      = TIME 
        res-history.action    = "Fix Asset Budget"
        res-history.aenderung = "Add Fix Asset Budget with number " + STRING(nr-budget) + 
                                " as " + desc-budget + ", date: " + STRING(date-budget) + 
                                ", amount: " + STRING(amount-budget) + ", status: " + convert-status(is-active-budget)
    .
END.
