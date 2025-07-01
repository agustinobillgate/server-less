
DEFINE TEMP-TABLE tbudget 
    FIELD res-nr AS INTEGER
    FIELD YEAR   AS INTEGER
    FIELD MONTH  AS INTEGER
    FIELD strMONTH  AS CHAR FORMAT "x(12)"
    FIELD amount    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99".

DEFINE TEMP-TABLE sbudget LIKE tbudget.

DEF INPUT PARAMETER TABLE FOR sbudget.

FOR EACH sbudget:
    CREATE eg-budget.
    ASSIGN eg-budget.nr       = sbudget.res-nr
           eg-budget.YEAR     = sbudget.YEAR
           eg-budget.MONTH    = sbudget.MONTH
           eg-budget.score    = sbudget.amount.
END.

