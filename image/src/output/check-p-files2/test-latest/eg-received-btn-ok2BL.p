DEFINE TEMP-TABLE tbudget 
    FIELD res-nr AS INTEGER
    FIELD YEAR   AS INTEGER
    FIELD MONTH  AS INTEGER
    FIELD strMONTH  AS CHAR FORMAT "x(12)"
    FIELD amount    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99".

DEFINE TEMP-TABLE sbudget LIKE tbudget.

DEFINE TEMP-TABLE recBudget
    FIELD res-nr    AS INTEGER
    FIELD YEAR      AS INTEGER
    FIELD MONTH     AS INTEGER
    FIELD score     AS INTEGER.

DEF INPUT PARAMETER TABLE FOR sbudget.
DEF INPUT PARAMETER intres AS INT.
DEF INPUT PARAMETER fyear AS INT.
DEF INPUT PARAMETER user-init AS CHAR.

DEF BUFFER usr   FOR bediener.
DEF VAR usrnr    AS INTEGER INITIAL 0  NO-UNDO.
DEF VAR res-nm   AS CHAR        FORMAT "x(30)".
define variable month-list as char extent 12 initial
          ["January", "February", "March", 
           "April", "May", "June",
           "July", "August", "September", 
           "October", "November", "December"].

FOR EACH recbudget :
    DELETE recbudget.
END.

FOR EACH eg-budget WHERE eg-budget.nr = intres AND eg-budget.YEAR = fyear :
    
    CREATE recbudget.
    ASSIGN recbudget.res-nr  = eg-budget.nr
            recbudget.YEAR   = eg-budget.YEAR
            recbudget.MONTH  = eg-budget.MONTH 
            recbudget.score  = eg-budget.score.

    DELETE eg-budget.
END.


FIND FIRST usr WHERE usr.userinit = user-init NO-LOCK NO-ERROR.
IF AVAILABLE usr THEN usrnr = usr.nr.

FOR EACH sbudget:

    FIND FIRST recbudget WHERE recbudget.MONTH = sbudget.MONTH AND 
        recbudget.res-nr = sbudget.res-nr AND recbudget.YEAR = sbudget.YEAR NO-LOCK NO-ERROR.

    IF AVAILABLE recbudget THEN
    DO:
        
        IF recbudget.score NE sbudget.amount THEN
        DO:
            FIND FIRST eg-resources WHERE eg-resources.nr = sbudget.res-nr NO-LOCK NO-ERROR.
            IF AVAILABLE eg-resources THEN
            DO:
                res-nm  = eg-resources.bezeich.
            END.
            ELSE
            DO:
                res-nm = "undefine".
            END.
            
            CREATE res-history.
            ASSIGN
                res-history.nr          = usrnr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.Action      = "Engineering Budget"
                res-history.aenderung   = "Change amount resource " + res-nm +  " " +
                    STRING(recbudget.YEAR) + ", " + month-list[recbudget.MONTH] + STRING(recbudget.score , "->>,>>>,>>>,>>9.99") + 
                    " to " + STRING(sbudget.amount,"->>,>>>,>>>,>>9.99").
        END.
    END.
    ELSE
    DO:

    END.
    


    CREATE eg-budget.
    ASSIGN eg-budget.nr       = sbudget.res-nr
           eg-budget.YEAR     = sbudget.YEAR
           eg-budget.MONTH    = sbudget.MONTH
           eg-budget.score    = sbudget.amount.
END.

    FOR EACH recbudget :
        DELETE recbudget.
    END.
/*MT
HIDE MESSAGE NO-PAUSE.  
MESSAGE translateExtended ("Budget has been successfully Modified.",lvCAREA,"")
    VIEW-AS ALERT-BOX INFORMATION.
*/
