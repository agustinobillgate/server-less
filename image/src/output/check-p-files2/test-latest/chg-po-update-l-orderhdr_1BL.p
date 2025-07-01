DEF INPUT PARAMETER rec-id    AS INT.
DEF INPUT PARAMETER user-init AS CHAR.

DEF VAR gedruckt AS DATE.
DEF VAR docu-nr  AS CHAR.

FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = rec-id.
FIND CURRENT l-orderhdr EXCLUSIVE-LOCK.
ASSIGN 
    l-orderhdr.gedruckt = today
    gedruckt            = l-orderhdr.gedruckt
    docu-nr             = l-orderhdr.docu-nr.
FIND CURRENT l-orderhdr NO-LOCK.
FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(rec-id) NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY   = 214
            queasy.char1 = STRING(rec-id)
            queasy.char2 = user-init
            queasy.char3 = bediener.username.
        CREATE res-history.
        ASSIGN
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            /*ONGOING*/
            res-history.aenderung   = "Release PO, Date: " + STRING(gedruckt) + "Docu no: " + STRING(docu-nr)
            res-history.action      = "Release PO".
    END.
END.
/*ELSE
DO:
    DISP 
        queasy.char1 FORMAT "x(20)"
        queasy.char2 FORMAT "x(20)"
        queasy.char3 FORMAT "x(20)".

    MESSAGE "available"
        VIEW-AS ALERT-BOX INFO BUTTONS OK.
END.*/
