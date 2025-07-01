/*
DEF TEMP-TABLE t-mapping-nation
    FIELD nationVHP AS CHAR
    FIELD nationBE  AS CHAR
    FIELD descr     AS CHAR
    FIELD nr        AS INT
    .
*/

/*Alder - Serverless - Issue 779 - Start*/
DEFINE TEMP-TABLE t-mapping-nation
    FIELD nationvhp AS CHARACTER    /*nationVHP -> nationvhp*/
    FIELD nationbe  AS CHARACTER    /*nationBE -> nationbe*/
    FIELD descr     AS CHARACTER
    FIELD nr        AS INTEGER.
/*Alder - Serverless - Issue 779 - End*/

DEF BUFFER nameqsy FOR queasy.
DEF BUFFER buffqsy FOR queasy.
DEFINE VARIABLE be-name AS CHARACTER.
DEFINE VARIABLE changedstr AS LONGCHAR.

DEF INPUT  PARAMETER TABLE FOR t-mapping-nation.
DEF INPUT  PARAMETER bookengID AS INT.
DEF INPUT  PARAMETER user-init AS CHAR.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.

/*Alder - Serverless - Issue 779 - Start*/
FIND FIRST nameqsy WHERE nameqsy.KEY = 159 AND nameqsy.number1 = bookengID NO-LOCK NO-ERROR.
IF AVAILABLE nameqsy THEN 
DO:
    ASSIGN be-name = nameqsy.char1 + "|Country".
END. 
/*Alder - Serverless - Issue 779 - End*/

FIND FIRST buffqsy WHERE buffqsy.KEY = 165 NO-LOCK NO-ERROR.
FIND FIRST t-mapping-nation NO-LOCK NO-ERROR.
IF NOT AVAILABLE buffqsy AND AVAILABLE t-mapping-nation THEN
DO:
    IF AVAILABLE bediener THEN
    DO:
        CREATE res-history. 
        ASSIGN 
            res-history.nr     = bediener.nr 
            res-history.datum  = TODAY 
            res-history.zeit   = TIME 
            res-history.action = "Booking Engine Interface".

        res-history.aenderung = CHR(40) + be-name + CHR(41) + " New Country Mapping Has Been Created".

        RELEASE res-history.
    END.
END.

changedstr = "".
FOR EACH t-mapping-nation NO-LOCK:
    FIND FIRST queasy WHERE queasy.KEY = 165
        AND queasy.number1 = bookengID
        AND queasy.number2 = t-mapping-nation.nr
        NO-ERROR.
    IF AVAILABLE queasy THEN 
    DO:
        IF queasy.char2 NE t-mapping-nation.nationbe THEN
            changedstr = changedstr + queasy.char1 + "=" + queasy.char2 + ">>" + t-mapping-nation.nationbe + " ".

        queasy.char2 = t-mapping-nation.nationbe.
    END.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY = 165
            queasy.number1 = bookengID
            queasy.number2 = t-mapping-nation.nr
            queasy.char1   = t-mapping-nation.nationvhp.
    END.
END.

IF changedstr NE "" THEN
DO:
    CREATE res-history.
    ASSIGN
        res-history.nr      = bediener.nr
        res-history.datum   = TODAY
        res-history.zeit    = TIME
        res-history.action  = "Booking Engine Interface".

    res-history.aenderung = CHR(40) + be-name + CHR(41) + " " + changedstr.
END.
