
DEF INPUT  PARAMETER s-rezlin-h-recid AS INT.
DEF INPUT  PARAMETER h-rezept-recid AS INT.
DEF INPUT  PARAMETER qty AS DECIMAL.
DEF INPUT  PARAMETER lostfact LIKE h-rezlin.lostfact.
DEF INPUT  PARAMETER user-init AS CHAR. /*FDL Sept 25, 2023 => Ticket 1E0427*/
DEF OUTPUT PARAMETER artnrlager LIKE h-rezlin.artnrlager.

DEFINE VARIABLE vLog AS LOGICAL.

FIND FIRST h-rezept WHERE RECID(h-rezept) = h-rezept-recid NO-LOCK.
FIND FIRST h-rezlin WHERE RECID(h-rezlin) = s-rezlin-h-recid NO-LOCK.
DO TRANSACTION:
    /*FDL Sept 25, 2023 => Ticket 1E0427*/
    IF h-rezlin.menge NE qty 
        OR h-rezlin.lostfact NE lostfact THEN
    DO:
        vLog = YES.
    END.

    IF vLog THEN
    DO:
        FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
        CREATE res-history.
        ASSIGN
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.action      = "Change Recipe"
            res-history.aenderung   = "Modify Recipe Item " + STRING(h-rezept.artnrrezept) 
                                    + "(" + SUBSTR(h-rezept.bezeich, 1, 24) + ")" + " => "
            .

        IF h-rezlin.menge NE qty THEN
        DO:
            res-history.aenderung = res-history.aenderung + "Qty " + STRING(h-rezlin.menge)
                + " to " + STRING(qty) + ";".
        END.
        ELSE IF h-rezlin.lostfact NE lostfact THEN
        DO:
            res-history.aenderung = res-history.aenderung + "Loss Factor " + STRING(h-rezlin.lostfact)
                + " to " + STRING(lostfact) + ";".
        END.
    END.
    
    FIND CURRENT h-rezlin EXCLUSIVE-LOCK.
    ASSIGN
        h-rezlin.menge = qty
        h-rezlin.lostfact = lostfact.
    FIND CURRENT h-rezlin NO-LOCK. 

    FIND CURRENT h-rezept EXCLUSIVE-LOCK.
    h-rezept.datummod = today.
    FIND CURRENT h-rezept NO-LOCK.
END.

artnrlager = h-rezlin.artnrlager.
