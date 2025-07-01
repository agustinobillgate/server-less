

DEFINE TEMP-TABLE t-eg-budget    LIKE eg-budget.
DEFINE TEMP-TABLE res
    FIELD res-nr        AS INTEGER
    FIELD res-nm        AS CHAR     FORMAT "x(16)"
    FIELD res-selected  AS LOGICAL INITIAL NO
.

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

DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER curr-year    AS INTEGER.
DEFINE INPUT PARAMETER intres       AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR res.
DEFINE INPUT PARAMETER TABLE FOR t-eg-budget.
DEFINE OUTPUT PARAMETER TABLE FOR tbudget.
DEFINE OUTPUT PARAMETER TABLE FOR sbudget.

DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE month-list AS CHAR EXTENT 12 INITIAL
          ["January", "February", "March", 
           "April", "May", "June",
           "July", "August", "September", 
           "October", "November", "December"].

IF case-type = 1 THEN RUN create-budget.
ELSE IF case-type = 2 THEN RUN create-get-budget.

/*********************************************************************************************/
PROCEDURE create-budget:
    DEFINE VARIABLE s AS INTEGER.
    DEFINE VARIABLE tAmount AS INTEGER.

    s = curr-year.

    FOR EACH tbudget:
        DELETE tbudget.
    END.

    IF s = ?  THEN
    DO:
        
    END.
    ELSE
    DO:
        FOR EACH res NO-LOCK:
            i = 1.
            do while i LE 12:
   
                FIND FIRST t-eg-budget WHERE t-eg-budget.nr =  res.res-nr  
                    AND t-eg-budget.YEAR = s 
                    AND t-eg-budget.MONTH = i NO-LOCK NO-ERROR.
                IF AVAILABLE t-eg-budget THEN
                    tAmount = t-eg-budget.score.
                ELSE
                    tAmount = 0.
        
                CREATE tbudget.
                ASSIGN tbudget.res-nr   = res.res-nr 
                       tbudget.YEAR     = s 
                       tbudget.MONTH    = i 
                       tbudget.strMONTH = month-list[i]
                       tbudget.amount   = tAmount.
        
                i = i + 1 .
            end. 
        END.
    END.   
END PROCEDURE.

PROCEDURE create-get-budget:
    DEFINE VARIABLE sAmount AS INTEGER.

    FOR EACH sbudget:
        DELETE sbudget.
    END.

    i = 1.
    DO WHILE i LE 12:
        FIND FIRST t-eg-budget WHERE t-eg-budget.nr = intres 
            AND t-eg-budget.YEAR = curr-year 
            AND t-eg-budget.MONTH = i NO-LOCK NO-ERROR.
        IF AVAILABLE t-eg-budget THEN
            sAmount = t-eg-budget.score.
        ELSE
            sAmount = 0.
   
        CREATE sbudget.
        ASSIGN sbudget.res-nr   = intres
               sbudget.YEAR     = curr-year
               sbudget.MONTH    = i
               sbudget.strMONTH = month-list[i]
               sbudget.amount   = sAmount.
        
        i = i + 1 .
    END. 
END PROCEDURE.
