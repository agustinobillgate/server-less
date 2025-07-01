DEFINE TEMP-TABLE h-list LIKE h-artikel.

DEF INPUT PARAMETER TABLE FOR h-list.
DEF INPUT PARAMETER case-type   AS INT.
DEF INPUT PARAMETER fract-flag  AS LOGICAL.
DEF INPUT PARAMETER ask-voucher AS LOGICAL.
DEF INPUT PARAMETER bezeich2    AS CHAR.
DEF INPUT PARAMETER barcode     AS CHAR.
DEF INPUT PARAMETER user-init   AS CHAR.

DEFINE VARIABLE v-log AS LOGICAL.
DEFINE BUFFER buff-hart FOR h-artikel.

FIND FIRST h-list.
IF case-type = 1 THEN   /*MT add */
DO:
    create h-artikel. 
    RUN fill-artikel. 
END.
ELSE IF case-type = 2 THEN   /*MT chg */
DO:
    FIND FIRST h-artikel WHERE h-artikel.artnr = h-list.artnr
        AND h-artikel.departement = h-list.departement EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE h-artikel THEN
    DO:
      RUN fill-artikel. 
      FIND CURRENT h-artikel NO-LOCK. 
      RELEASE h-artikel.
    END.
END.

PROCEDURE fill-artikel:
    IF case-type EQ 2 THEN
    DO:        
        IF TRIM(h-artikel.bezeich) NE TRIM(h-list.bezeich)
            OR h-artikel.zwkum NE h-list.zwkum
            OR h-artikel.endkum NE h-list.endkum 
            OR h-artikel.epreis1 NE h-list.epreis1 
            OR h-artikel.artart NE h-list.artart
            OR h-artikel.mwst-code NE h-list.mwst-code
            OR h-artikel.service-code NE h-list.service-code 
            OR h-artikel.artnrfront NE h-list.artnrfront
            OR h-artikel.bondruckernr[1] NE h-list.bondruckernr[1]
            OR h-artikel.activeflag NE h-list.activeflag THEN
        DO:
            v-log = YES.
        END.

        IF v-log THEN
        DO:
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.

            CREATE res-history.
            ASSIGN
                res-history.nr          = bediener.nr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.action      = "Outlet Article Setup"
                res-history.aenderung   = "Modify ArtNo " + STRING(h-artikel.artnr) + " => "
                .

            IF TRIM(h-artikel.bezeich) NE TRIM(h-list.bezeich) THEN
            DO:
                res-history.aenderung = res-history.aenderung + h-artikel.bezeich 
                    + " to " + h-list.bezeich + ";".
            END.
            IF h-artikel.zwkum NE h-list.zwkum THEN
            DO:
                res-history.aenderung = res-history.aenderung + "SubGroup " + STRING(h-artikel.zwkum)
                    + " to " + STRING(h-list.zwkum) + ";".
            END.
            IF h-artikel.endkum NE h-list.endkum THEN
            DO:
                res-history.aenderung = res-history.aenderung + "MainGroup " + STRING(h-artikel.endkum)
                    + " to " + STRING(h-list.endkum) + ";".
            END.
            IF h-artikel.epreis1 NE h-list.epreis1 THEN
            DO:
                res-history.aenderung = res-history.aenderung + "UnitPrice " + STRING(h-artikel.epreis1)
                    + " to " + STRING(h-list.epreis1) + ";".
            END.
            IF h-artikel.artart NE h-list.artart THEN
            DO:
                res-history.aenderung = res-history.aenderung + "ArtType " + STRING(h-artikel.artart)
                    + " to " + STRING(h-list.artart) + ";".
            END.
            IF h-artikel.mwst-code NE h-list.mwst-code THEN
            DO:
                res-history.aenderung = res-history.aenderung + "VAT " + STRING(h-artikel.mwst-code)
                    + " to " + STRING(h-list.mwst-code) + ";".
            END.
            IF h-artikel.service-code NE h-list.service-code THEN
            DO:
                res-history.aenderung = res-history.aenderung + "Service " + STRING(h-artikel.service-code)
                    + " to " + STRING(h-list.service-code) + ";".
            END.
            IF h-artikel.artnrfront NE h-list.artnrfront THEN
            DO:
                res-history.aenderung = res-history.aenderung + "FO ArtNo " + STRING(h-artikel.artnrfront)
                    + " to " + STRING(h-list.artnrfront) + ";".
            END.
            IF h-artikel.bondruckernr[1] NE h-list.bondruckernr[1] THEN
            DO:
                res-history.aenderung = res-history.aenderung + "KP No " + STRING(h-artikel.bondruckernr[1])
                    + " to " + STRING(h-list.bondruckernr[1]) + ";".
            END.
            IF h-artikel.activeflag NE h-list.activeflag THEN
            DO:
                res-history.aenderung = res-history.aenderung + "ActiveArt " + STRING(h-artikel.activeflag)
                    + " to " + STRING(h-list.activeflag) + ";".
            END.
        END.
    END.

    ASSIGN 
    h-artikel.artnr  = h-list.artnr 
    h-artikel.departement = h-list.departement 
    h-artikel.bezaendern = h-list.bezaendern 
    h-artikel.bezeich = h-list.bezeich 
    h-artikel.zwkum   = h-list.zwkum 
    h-artikel.endkum  = h-list.endkum 
    h-artikel.epreis1  = h-list.epreis1 
    h-artikel.abbuchung  = h-list.abbuchung
    h-artikel.autosaldo = h-list.autosaldo 
    h-artikel.artart  = h-list.artart 
    h-artikel.epreis2  = h-list.epreis2 
    h-artikel.gang = INTEGER(fract-flag)
    h-artikel.bondruckernr[1]   = h-list.bondruckernr[1] 
    h-artikel.aenderwunsch = h-list.aenderwunsch 
    h-artikel.artnrfront = h-list.artnrfront 
    h-artikel.mwst-code  = h-list.mwst-code 
    h-artikel.service-code = h-list.service-code 
    h-artikel.activeflag = h-list.activeflag 
    h-artikel.s-gueltig  = h-list.s-gueltig 
    h-artikel.e-gueltig = h-list.e-gueltig 
    h-artikel.artnrlager = h-list.artnrlager 
    h-artikel.artnrrezept = h-list.artnrrezept 
    h-artikel.prozent = h-list.prozent 
    h-artikel.lagernr = h-list.lagernr 
    h-artikel.betriebsnr = h-list.betriebsnr 
    h-artikel.bondruckernr[4] = INTEGER(ask-voucher) 
    . 
    IF bezeich2 = "" THEN
    DO:
        FIND FIRST queasy WHERE queasy.key = 38 AND queasy.number1 = h-list.departement
            AND queasy.number2 = h-list.artnr EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN DELETE queasy.
    END.
    ELSE
    DO:
        FIND FIRST queasy WHERE queasy.key = 38 AND queasy.number1 = h-list.departement
            AND queasy.number2 = h-list.artnr EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            CREATE queasy.
            ASSIGN
                queasy.key = 38
                queasy.number1 = h-list.departement
                queasy.number2 = h-list.artnr
            .
        END.
        ASSIGN queasy.char3 = bezeich2.
        FIND CURRENT queasy NO-LOCK.
    END.

    FIND FIRST queasy WHERE queasy.key = 200 AND queasy.number1 = h-list.departement
         AND queasy.number2 = h-list.artnr EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN
            queasy.key = 200
            queasy.number1 = h-list.departement
            queasy.number2 = h-list.artnr
            queasy.char1   = barcode
            queasy.char2   = h-list.bezeich.
    END.
    ELSE 
    DO:
        ASSIGN queasy.char1 = barcode.  
    END.
    FIND CURRENT queasy NO-LOCK.

    RELEASE queasy.
END. 

