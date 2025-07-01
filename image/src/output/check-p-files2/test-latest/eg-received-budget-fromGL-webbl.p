
DEFINE TEMP-TABLE tbudget 
    FIELD res-nr    AS INTEGER
    FIELD YEAR      AS INTEGER
    FIELD MONTH     AS INTEGER
    FIELD strMONTH  AS CHAR FORMAT "x(12)"
    FIELD amount    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
.

DEFINE TEMP-TABLE sbudget 
    FIELD res-nr    AS INTEGER
    FIELD YEAR      AS INTEGER
    FIELD MONTH     AS INTEGER
    FIELD strMONTH  AS CHAR FORMAT "x(12)"
    FIELD amount    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
.

DEFINE INPUT PARAMETER resources-char1 AS CHARACTER.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR tbudget.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR sbudget.
DEFINE OUTPUT PARAMETER msg-str AS CHARACTER.

DEF BUFFER buf-gl-acct FOR gl-acct.
DEF VAR i AS INT.

IF resources-char1 NE "" THEN
DO:
    FIND FIRST buf-gl-acct WHERE buf-gl-acct.fibukonto = resources-char1
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE buf-gl-acct THEN
    DO:
        msg-str = "Wrong COA Definition".  
    END.
    ELSE
    DO: 
        DO i = 1 TO 12:
            FIND FIRST tbudget WHERE tbudget.MONTH = i EXCLUSIVE-LOCK.
            tbudget.amount = buf-gl-acct.budget[i].
            FIND CURRENT tbudget NO-LOCK.
            FIND FIRST sbudget WHERE sbudget.MONTH = i EXCLUSIVE-LOCK.
            sbudget.amount = buf-gl-acct.budget[i].
            FIND CURRENT sbudget NO-LOCK.
        END.
    END.
END.
ELSE
DO:
    msg-str = "COA Not Yet Defined.". 
END.
