
DEF INPUT PARAMETER chequeNo   AS CHAR.
DEF INPUT PARAMETER dueDate    AS DATE.
DEF INPUT PARAMETER postDate   AS DATE.
DEF INPUT PARAMETER pay-amount LIKE gc-pi.betrag.
DEF INPUT PARAMETER docu-nr    AS CHAR.

FIND FIRST gc-giro WHERE gc-giro.gironum = chequeNo EXCLUSIVE-LOCK
    NO-ERROR.
IF AVAILABLE gc-giro THEN
DO:
    ASSIGN 
        gc-giro.giro-status = 1
        gc-giro.dueDate     = dueDate
        gc-giro.postedDate  = postDate
        gc-giro.betrag      = pay-amount
        gc-giro.docu-nr     = docu-nr
    .
    FIND CURRENT gc-giro NO-LOCK.
    RELEASE gc-giro.
END.

