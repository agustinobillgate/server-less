DEFINE TEMP-TABLE t-l-artikel  LIKE l-artikel
    FIELD is-delete     AS LOGICAL
    FIELD is-select     AS LOGICAL
.


DEFINE INPUT PARAMETER pvILanguage                  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR t-l-artikel. 
DEFINE OUTPUT PARAMETER str-msg     AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER delete-it   AS LOGICAL INITIAL YES. 

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "sarticle-list". 

FIND FIRST t-l-artikel WHERE t-l-artikel.is-select EQ YES AND t-l-artikel.is-delete EQ YES NO-LOCK NO-ERROR.
IF NOT AVAILABLE t-l-artikel THEN
DO:
    str-msg = translateExtended ("Select at least 1 article to delete",lvCAREA,"").
    delete-it = NO.
    RETURN.
END.

FOR EACH t-l-artikel WHERE t-l-artikel.is-select EQ YES AND t-l-artikel.is-delete EQ YES NO-LOCK:

    FIND FIRST l-bestand WHERE l-bestand.artnr = t-l-artikel.artnr 
        AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN 
    DO: 
        str-msg = "Unable to delete " + STRING(t-l-artikel.artnr) + CHR(10) 
                + translateExtended ("Stock Onhand exists, deleting not possible.",lvCAREA,"").
        delete-it = NO. 
        RETURN. 
    END. 

    FIND FIRST l-order WHERE l-order.artnr = t-l-artikel.artnr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-order THEN 
    DO: 
        str-msg = "Unable to delete " + STRING(t-l-artikel.artnr) + CHR(10) 
                + translateExtended ("Article in used by order file",lvCAREA,"") 
                + CHR(10) + "Document No: " + l-order.docu-nr.
        delete-it = NO. 
        RETURN. 
    END. 

    IF delete-it THEN 
    DO: 
        FIND FIRST l-op WHERE l-op.artnr = t-l-artikel.artnr NO-LOCK NO-ERROR. 
        IF AVAILABLE l-op THEN 
        DO: 
            str-msg = "Unable to delete " + STRING(t-l-artikel.artnr) + CHR(10) 
                    + translateExtended ("Article in used by stock in-/out operation file",lvCAREA,"") 
                    + CHR(10) + "Document No: " + l-op.docu-nr + CHR(10) + 
                    "Delivery Note: " + l-op.lscheinnr.
            delete-it = NO. 
            RETURN. 
        END. 
    END. 

    IF delete-it THEN 
    DO: 
        FIND FIRST h-rezlin WHERE h-rezlin.artnrlager = t-l-artikel.artnr NO-LOCK NO-ERROR. 
        IF AVAILABLE h-rezlin THEN 
        DO: 
            FIND FIRST h-rezept WHERE h-rezept.artnrrezept = h-rezlin.artnrrezept NO-LOCK. 
            str-msg = "Unable to delete " + STRING(t-l-artikel.artnr) + CHR(10) 
                    + translateExtended ("Article in used by recipe file",lvCAREA,"") 
                    + CHR(10) + 
                    STRING(h-rezept.artnrrezept) + " - " + h-rezept.bezeich.
            delete-it = NO. 
            RETURN. 
        END. 
    END. 

    IF delete-it THEN 
    DO: 
        FIND FIRST h-artikel WHERE h-artikel.artnrlager = t-l-artikel.artnr NO-LOCK NO-ERROR. 
        IF AVAILABLE h-artikel THEN 
        DO: 
            str-msg = "Unable to delete " + STRING(t-l-artikel.artnr) + CHR(10) 
                    + translateExtended ("Article in used by outlet artikel stock item",lvCAREA,"") 
                    + CHR(10) + 
                    STRING(h-artikel.artnr) + " - " + h-artikel.bezeich.
            delete-it = NO. 
            RETURN. 
        END. 
    END. 
    
    IF delete-it THEN 
    DO: 
        FIND FIRST dml-art WHERE  dml-art.artnr EQ t-l-artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE dml-art THEN 
        DO: 
            str-msg = "Unable to delete " + STRING(t-l-artikel.artnr) + CHR(10) 
                    + translateExtended ("Article in used by DML",lvCAREA,"").
            delete-it = NO. 
            RETURN. 
        END. 
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
                AND INT(ENTRY(1,reslin-queasy.char1,";")) EQ t-l-artikel.artnr NO-LOCK NO-ERROR.      
        IF AVAILABLE reslin-queasy THEN 
        DO: 
            str-msg = "Unable to delete " + STRING(t-l-artikel.artnr) + CHR(10) 
                    + translateExtended ("Article in used by DML",lvCAREA,"").
            delete-it = NO. 
            RETURN. 
        END. 
        FIND FIRST dml-artdep WHERE dml-artdep.artnr EQ t-l-artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE dml-artdep THEN 
        DO: 
            str-msg = "Unable to delete " + STRING(t-l-artikel.artnr) + CHR(10) 
                    + translateExtended ("Article in used by DML",lvCAREA,"").
            delete-it = NO. 
            RETURN. 
        END. 
    END. 
END.

FOR EACH t-l-artikel WHERE t-l-artikel.is-select EQ YES AND t-l-artikel.is-delete EQ YES:
    FOR EACH l-lager NO-LOCK: 
        FOR EACH l-bestand WHERE l-bestand.artnr = t-l-artikel.artnr 
            AND l-bestand.lager-nr = l-lager.lager-nr EXCLUSIVE-LOCK: 
            DELETE l-bestand. 
        END. 
    END. 
    FOR EACH l-verbrauch WHERE l-verbrauch.artnr = t-l-artikel.artnr EXCLUSIVE-LOCK: 
        DELETE l-verbrauch. 
    END. 
    FIND FIRST l-artikel WHERE l-artikel.artnr = t-l-artikel.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE l-artikel THEN
    DO:
        FIND CURRENT l-artikel EXCLUSIVE-LOCK.
        DELETE l-artikel. 
    END.
END.

str-msg = translateExtended ("Article deleted",lvCAREA,"").

