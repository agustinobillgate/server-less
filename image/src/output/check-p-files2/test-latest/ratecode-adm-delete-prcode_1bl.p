
DEF INPUT PARAMETER icase           AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER prcode          AS CHAR     NO-UNDO.
DEF INPUT PARAMETER user-init       AS CHAR     NO-UNDO.

DEF OUTPUT PARAMETER msg-str    AS CHAR INIT ""     NO-UNDO.
DEF OUTPUT PARAMETER error-flag AS LOGICAL INIT NO  NO-UNDO.

DEFINE BUFFER bqueasy FOR queasy.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "ratecode-admin". 

FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = prcode
  NO-LOCK.

IF icase = 1 THEN
DO:
  FIND FIRST ratecode WHERE ratecode.code = prcode NO-LOCK NO-ERROR. 
  IF AVAILABLE ratecode THEN 
  DO: 
    msg-str = translateExtended ("Contract Rates exists, deleting not possible",lvCAREA,"").
    error-flag = YES.
    RETURN.
  END. 
  msg-str = "&Q" + translateExtended ("Do you really want to REMOVE the Rate Code",lvCAREA,"") 
    + CHR(10) + STRING(prcode) + " - " + queasy.char2 + " ?". 
  RETURN.
END.
ELSE IF icase = 2 THEN
DO: 
    FIND FIRST guest-pr WHERE guest-pr.code = queasy.char1 NO-ERROR. 
    IF AVAILABLE guest-pr THEN 
    DO:    
        FIND FIRST guest WHERE guest.gastnr = guest-pr.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE guest AND guest.karteityp = 9 THEN
        DO:
            FIND CURRENT guest EXCLUSIVE-LOCK.
            DELETE guest.
        END.
        DELETE guest-pr. 
    END.
    
    IF queasy.char1 NE "" THEN
    FOR EACH prtable WHERE prtable.prcode = queasy.char1 EXCLUSIVE-LOCK: 
        DELETE prtable. 
    END. 

    /*Alder Start*/
    FIND FIRST bqueasy WHERE bqueasy.KEY = 289 AND bqueasy.char1 EQ queasy.char1 NO-LOCK NO-ERROR.
    IF AVAILABLE bqueasy THEN
    DO: 
        FIND CURRENT bqueasy EXCLUSIVE-LOCK.
        DELETE bqueasy.
    END.
    /*Alder End*/

    FIND CURRENT queasy EXCLUSIVE-LOCK. 
    DELETE queasy. 

    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN 
    DO:                          
        CREATE res-history.
        ASSIGN 
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.aenderung   = "Delete RateCode, Code: " + prcode.
            res-history.action      = "RateCode".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.
    END.

END.


