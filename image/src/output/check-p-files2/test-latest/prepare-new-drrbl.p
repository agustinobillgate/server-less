DEFINE TEMP-TABLE menu-drr
    FIELD nr    AS INT
    FIELD descr AS CHAR FORMAT "x(50)".

DEFINE OUTPUT PARAMETER TABLE FOR menu-drr.

FIND FIRST menu-drr NO-LOCK NO-ERROR.
IF NOT AVAILABLE menu-drr THEN DO:
    CREATE menu-drr.
    ASSIGN menu-drr.nr    = 1
           menu-drr.descr = "STATISTIC".
    CREATE menu-drr.
    ASSIGN menu-drr.nr    = 2
           menu-drr.descr = "REVENUE BY SEGMENT".
    CREATE menu-drr.
    ASSIGN menu-drr.nr    = 3
           menu-drr.descr = "REVENUE".
    CREATE menu-drr.
    ASSIGN menu-drr.nr    = 4
           menu-drr.descr = "PAYABLE".
    CREATE menu-drr.
    ASSIGN menu-drr.nr    = 5
           menu-drr.descr = "PAYMENT".
    CREATE menu-drr.
    ASSIGN menu-drr.nr    = 6
           menu-drr.descr = "GUEST LEDGER".
    CREATE menu-drr.
    ASSIGN menu-drr.nr    = 7
           menu-drr.descr = "FB SALES BY SHIFT".
END.



