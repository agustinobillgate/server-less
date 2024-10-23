DEFINE TEMP-TABLE l-art LIKE l-artikel. 

DEFINE TEMP-TABLE tt-artnr
    FIELD curr-i   AS INTEGER
    FIELD ss-artnr AS INTEGER
.
DEFINE TEMP-TABLE tt-content
    FIELD curr-i     AS INTEGER
    FIELD ss-content AS INTEGER
.

DEFINE INPUT PARAMETER pvILanguage  AS INT      NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR tt-artnr.
DEFINE INPUT PARAMETER TABLE FOR tt-content.
DEFINE INPUT PARAMETER s-unit       AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER artnr        AS INT      NO-UNDO.
DEFINE INPUT PARAMETER t-recid      AS INT      NO-UNDO.
DEFINE INPUT PARAMETER fibukonto    AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER dml-art      AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER bez-aend     AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER picture-file AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER original-art AS INT      NO-UNDO.
DEFINE INPUT PARAMETER user-init    AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR l-art.
DEFINE OUTPUT PARAMETER sss-artnr   AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER sss-cont    AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER str-msg     AS CHAR     NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER changed     AS LOGICAL  NO-UNDO INIT NO.

DEFINE VARIABLE ss-artnr     AS INT      NO-UNDO EXTENT 3.
DEFINE VARIABLE ss-content   AS INT      NO-UNDO EXTENT 3.

DEFINE VARIABLE old-lastpc-price AS DECIMAL NO-UNDO.

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "chg-sarticle". 

DEF BUFFER l-art1 FOR l-artikel. 
DEF BUFFER l-art2 FOR l-artikel. 
FIND FIRST l-art NO-LOCK NO-ERROR.

FOR EACH tt-artnr:
    ss-artnr[tt-artnr.curr-i] = tt-artnr.ss-artnr.
END.
FOR EACH tt-content:
    ss-content[tt-content.curr-i] = tt-content.ss-content.
END.

IF ss-artnr[1] NE 0 THEN 
DO: 
    FIND FIRST l-art1 WHERE l-art1.artnr = ss-artnr[1] NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-art1 OR l-art1.betriebsnr GT 0 THEN 
    DO: 
        sss-artnr = YES.
        RETURN. 
    END. 
    IF ss-content[1] = 0 THEN 
    DO: 
        sss-cont = YES.
        RETURN. 
    END. 
END. 
IF ss-artnr[2] NE 0 THEN 
DO: 
    FIND FIRST l-art1 WHERE l-art1.artnr = ss-artnr[2] NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-art1 OR l-art1.betriebsnr GT 0 THEN 
    DO: 
        sss-artnr = YES.
        RETURN.
    END. 
    IF ss-content[2] = 0 THEN 
    DO: 
        sss-cont = YES.
        RETURN.
    END. 
END. 
IF ss-artnr[3] NE 0 THEN 
DO: 
    FIND FIRST l-art1 WHERE l-art1.artnr = ss-artnr[3] NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-art1 OR l-art1.betriebsnr GT 0 THEN 
    DO: 
        sss-artnr = YES.
        RETURN.
    END. 
    IF ss-content[3] = 0 THEN 
    DO: 
        sss-cont = YES.
        RETURN.
    END. 
END. 

IF artnr = 0 THEN 
    str-msg = translateExtended ("Article Number not yet defined",lvCAREA,""). 
ELSE 
DO:     
    FIND FIRST l-artikel WHERE l-artikel.artnr = artnr 
        AND RECID(l-artikel) NE t-recid NO-LOCK NO-ERROR. 
    IF AVAILABLE l-artikel THEN 
        str-msg = translateExtended ("Article Number ",lvCAREA,"") 
                  + STRING(artnr) + " - " + l-artikel.bezeich + CHR(2) 
                  + "already exists". 
    ELSE 
    DO: 
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibukonto 
            NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-art.zwkum NO-LOCK. 
            FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto 
                NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE gl-acct THEN 
                str-msg = "&W" + translateExtended ("Chart of Account not correctly defined.",lvCAREA,""). 
        END. 

        RUN update-l-artikel. 
        RUN update-artnr.
        changed = YES.      
    END. 
END. 


PROCEDURE update-l-artikel: 
    DO transaction: 
        FIND FIRST l-artikel WHERE RECID(l-artikel) EQ t-recid EXCLUSIVE-LOCK. 
        old-lastpc-price = l-artikel.ek-letzter.
        ASSIGN l-artikel.artnr = artnr
               l-artikel.fibukonto = fibukonto
               l-artikel.bestellt = dml-art
               l-artikel.jahrgang = INTEGER(bez-aend)
               l-artikel.bezeich = l-art.bezeich
               l-artikel.zwkum = l-art.zwkum
               l-artikel.endkum = l-art.endkum 
               l-artikel.herkunft = l-art.herkunft + ";" + s-unit + ";"
               l-artikel.masseinheit = l-art.masseinheit
               l-artikel.inhalt = l-art.inhalt
               l-artikel.traubensort = l-art.traubensort
               l-artikel.lief-einheit = l-art.lief-einheit 
               l-artikel.min-bestand = l-art.min-bestand
               l-artikel.anzverbrauch = l-art.anzverbrauch 
               l-artikel.alkoholgrad = l-art.alkoholgrad
               l-artikel.lief-nr1 = l-art.lief-nr1
               l-artikel.lief-artnr[1] = l-art.lief-artnr[1]
               l-artikel.lief-nr2 = l-art.lief-nr2
               l-artikel.lief-artnr[2] = l-art.lief-artnr[2]
               l-artikel.lief-nr3 = l-art.lief-nr3
               l-artikel.lief-artnr[3] = l-art.lief-artnr[3]
               l-artikel.betriebsnr = l-art.betriebsnr
               l-artikel.ek-aktuell = l-art.ek-aktuell 
               l-artikel.ek-letzter = l-art.ek-letzter 
               l-artikel.vk-preis = l-art.vk-preis
            . 
        FIND CURRENT l-artikel NO-LOCK. 

        FIND FIRST queasy WHERE queasy.KEY = 20 AND queasy.number1 = artnr 
            EXCLUSIVE-LOCK NO-ERROR. 
        IF ss-artnr[1] NE 0 OR ss-artnr[2] NE 0 OR ss-artnr[3] NE 0 
            OR picture-file NE "" THEN
        DO: 
            IF NOT AVAILABLE queasy THEN 
            DO: 
                CREATE queasy. 
                ASSIGN 
                    queasy.KEY = 20 
                    queasy.number1 = artnr. 
            END. 
            ASSIGN 
                queasy.deci1 = ss-artnr[1] 
                queasy.deci2 = ss-artnr[2] 
                queasy.deci3 = ss-artnr[3] 
                queasy.char2 = STRING(ss-content[1],"999") + ";" 
                             + STRING(ss-content[2],"999") + ";" 
                             + STRING(ss-content[3],"999") + ";"        
                queasy.char3 = picture-file
                queasy.date3 = TODAY. 
            RELEASE queasy. 
        END. 
        ELSE 
        DO: 
            IF AVAILABLE queasy THEN DELETE queasy. 
        END. 

        IF original-art NE l-artikel.artnr THEN 
        DO: 
            FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.     
            CREATE res-history. 
            ASSIGN 
                res-history.nr = bediener.nr 
                res-history.datum = TODAY 
                res-history.zeit = TIME 
                res-history.action = "Inventory"
                res-history.aenderung = "Change Inventory ArtNo: "
                                        + STRING(original-art, "9999999") + " -> " 
                                        + STRING(l-artikel.artnr,"9999999"). 
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history. 
        END. 
        
        IF old-lastpc-price NE l-art.ek-letzter THEN
        DO:
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK.     
            CREATE res-history. 
            ASSIGN 
                res-history.nr = bediener.nr 
                res-history.datum = TODAY 
                res-history.zeit = TIME 
                res-history.action = "Inventory"
                res-history.aenderung = "Change Last Purchase Price " + l-artikel.bezeich + " : "
                                        + STRING(old-lastpc-price) + " --> " + STRING(l-art.ek-letzter). 
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history. 
        END.
    END. /* transaction */ 
END. 
 


PROCEDURE update-artnr: 
DEFINE buffer l-op1 FOR l-op. 
DEFINE buffer l-ophis1 FOR l-ophis. 
DEFINE buffer l-od1 FOR l-order. 
DEFINE buffer l-art1 FOR l-artikel. 
  
    FIND FIRST l-bestand WHERE l-bestand.artnr = original-art 
        AND l-bestand.lager-nr = 0 EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN l-bestand.artnr = artnr. 

    FOR EACH l-lager NO-LOCK: 
        FIND FIRST l-bestand WHERE l-bestand.artnr = original-art 
            AND l-bestand.lager-nr = l-lager.lager-nr EXCLUSIVE-LOCK NO-ERROR. 
        IF AVAILABLE l-bestand THEN l-bestand.artnr = artnr. 
        FOR EACH l-op WHERE l-op.artnr = original-art 
            AND l-op.lager-nr = l-lager.lager-nr NO-LOCK USE-INDEX artnrlag_ix: 
            FIND FIRST l-op1 WHERE RECID(l-op1) = RECID(l-op) EXCLUSIVE-LOCK. 
            l-op1.artnr = artnr. 
            FIND CURRENT l-op1 NO-LOCK. 
        END. 
    END. 
    
    FIND FIRST l-besthis WHERE l-besthis.artnr = original-art NO-ERROR.
    DO WHILE AVAILABLE l-besthis:
        ASSIGN l-besthis.artnr = artnr.
        FIND CURRENT l-besthis NO-LOCK.
        FIND NEXT l-besthis WHERE l-besthis.artnr = original-art NO-ERROR.
    END.

    FOR EACH l-ophis WHERE l-ophis.artnr = original-art NO-LOCK 
        USE-INDEX art-dat-op_ix: 
        FIND FIRST l-ophis1 WHERE RECID(l-ophis1) = RECID(l-ophis) EXCLUSIVE-LOCK. 
        l-ophis1.artnr = artnr. 
        FIND CURRENT l-ophis1 NO-LOCK. 
    END. 
    FOR EACH l-verbrauch WHERE l-verbrauch.artnr = original-art: 
        l-verbrauch.artnr = artnr. 
    END. 
    FOR EACH l-order WHERE l-order.artnr = original-art NO-LOCK: 
        FIND FIRST l-od1 WHERE RECID(l-od1) = RECID(l-order) EXCLUSIVE-LOCK. 
        l-od1.artnr = artnr. 
        FIND CURRENT l-od1 NO-LOCK. 
    END. 
    FOR EACH l-pprice WHERE l-pprice.artnr = original-art EXCLUSIVE-LOCK: 
        l-pprice.artnr = artnr. 
    END. 
    FOR EACH h-rezlin WHERE h-rezlin.artnrlager = original-art EXCLUSIVE-LOCK: 
        h-rezlin.artnrlager = artnr. 
    END. 
 
    FIND FIRST queasy WHERE queasy.KEY = 20 AND queasy.number1 = original-art 
        EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE queasy THEN 
    DO: 
        queasy.number1 = artnr. 
        FIND CURRENT queasy NO-LOCK. 
        RELEASE queasy. 
    END. 
 
    FIND FIRST dml-art WHERE dml-art.artnr = original-art NO-ERROR.
    DO WHILE AVAILABLE dml-art:
        ASSIGN dml-art.artnr = artnr.
        FIND CURRENT dml-art NO-LOCK.
        FIND NEXT dml-art WHERE dml-art.artnr = original-art NO-ERROR.
    END.

    FIND FIRST dml-artdep WHERE dml-artdep.artnr = original-art NO-ERROR.
    DO WHILE AVAILABLE dml-artdep:
        ASSIGN dml-artdep.artnr = artnr.
        FIND CURRENT dml-artdep NO-LOCK.
        FIND NEXT dml-artdep WHERE dml-artdep.artnr = original-art NO-ERROR.
    END.
END. 
