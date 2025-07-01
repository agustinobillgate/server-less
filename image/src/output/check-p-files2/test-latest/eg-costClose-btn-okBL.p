
DEF INPUT PARAMETER styear AS INT.
DEF INPUT PARAMETER stmonth AS INT.
DEF INPUT PARAMETER intRes AS INT.
DEF INPUT PARAMETER user-init AS CHAR.

FIND FIRST eg-budget WHERE eg-budget.YEAR = styear AND eg-budget.MONTH = stmonth
    AND eg-budget.nr = intRes NO-ERROR.
IF AVAILABLE eg-budget THEN
DO:
    ASSIGN eg-budget.closeflag = YES
            eg-budget.close-date = TODAY
            eg-budget.close-time = TIME
            eg-budget.close-by   = user-init.

END.
ELSE
DO:

END.


FIND FIRST eg-cost WHERE eg-cost.YEAR = styear AND eg-cost.MONTH = stmonth
    AND eg-cost.resource-nr = intRes NO-ERROR.
IF AVAILABLE eg-cost THEN
DO:
    ASSIGN eg-cost.closeflag = YES
            eg-cost.close-date = TODAY /* apakah pake ci-date */
            eg-cost.close-time = TIME
            eg-cost.close-by   = user-init.
END.
ELSE
DO:

END.
