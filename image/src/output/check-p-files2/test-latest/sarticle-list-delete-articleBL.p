DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER artnr        AS INTEGER  NO-UNDO. 
DEFINE OUTPUT PARAMETER str-msg     AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER delete-it   AS LOGICAL INITIAL YES. 

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "sarticle-list". 

FIND FIRST l-bestand WHERE l-bestand.artnr = artnr 
    AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE l-bestand THEN 
DO: 
    str-msg = translateExtended ("Stock Onhand exists, deleting not possible.",lvCAREA,"").
    delete-it = NO. 
    RETURN. 
END. 

FIND FIRST l-order WHERE l-order.artnr = artnr NO-LOCK NO-ERROR. 
IF AVAILABLE l-order THEN 
DO: 
    str-msg = translateExtended ("Article in used by order file",lvCAREA,"") 
              + CHR(10) + "Document No: " + l-order.docu-nr.
    delete-it = NO. 
    RETURN. 
END. 

IF delete-it THEN 
DO: 
    FIND FIRST l-op WHERE l-op.artnr = artnr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-op THEN 
    DO: 
        str-msg = translateExtended ("Article in used by stock in-/out operation file",lvCAREA,"") 
                  + CHR(10) + "Document No: " + l-op.docu-nr + CHR(10) + 
                  "Delivery Note: " + l-op.lscheinnr.
        delete-it = NO. 
        RETURN. 
    END. 
END. 

IF delete-it THEN 
DO: 
    FIND FIRST h-rezlin WHERE h-rezlin.artnrlager = artnr NO-LOCK NO-ERROR. 
    IF AVAILABLE h-rezlin THEN 
    DO: 
        FIND FIRST h-rezept WHERE h-rezept.artnrrezept = h-rezlin.artnrrezept NO-LOCK. 
        str-msg = translateExtended ("Article in used by recipe file",lvCAREA,"") 
                  + CHR(10) + 
                  STRING(h-rezept.artnrrezept) + " - " + h-rezept.bezeich.
        delete-it = NO. 
        RETURN. 
    END. 
END. 

IF delete-it THEN 
DO: 
    FOR EACH l-lager NO-LOCK: 
        FOR EACH l-bestand WHERE l-bestand.artnr = artnr 
            AND l-bestand.lager-nr = l-lager.lager-nr EXCLUSIVE-LOCK: 
            DELETE l-bestand. 
            RELEASE l-bestand.
        END. 
    END. 
    FOR EACH l-verbrauch WHERE l-verbrauch.artnr = artnr EXCLUSIVE-LOCK: 
        DELETE l-verbrauch. 
        RELEASE l-verbrauch.
    END. 
    FIND FIRST l-artikel WHERE l-artikel.artnr = artnr EXCLUSIVE-LOCK. 
    IF AVAILABLE l-artikel THEN /*FT serverless*/
    DO:
        DELETE l-artikel. 
        RELEASE l-artikel.
        str-msg = translateExtended ("Article deleted",lvCAREA,"").
    END.                                                           
END. 

