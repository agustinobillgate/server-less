DEFINE TEMP-TABLE min-onhand-list
    FIELD artnr      AS INTEGER FORMAT "9999999"
    FIELD name       AS CHAR FORMAT "x(36)"
    FIELD min-oh     AS DECIMAL FORMAT "->>>,>>9.99"
    FIELD curr-oh    AS DECIMAL FORMAT "->>>,>>9.99"
    /*FIELD avrgprice  AS CHAR FORMAT "x(16)"
    FIELD ek-aktuell AS CHAR FORMAT "x(16)"*/
    FIELD avrgprice  AS DECIMAL
    FIELD ek-aktuell AS DECIMAL
    FIELD datum      AS DATE
    . 

DEF INPUT PARAMETER sorttype AS INT.
DEF INPUT PARAMETER main-grp AS INT.
DEF INPUT PARAMETER from-store3 AS INT.
DEF INPUT PARAMETER to-store3 AS INT.
DEF INPUT PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR min-onhand-list.

/*DEF VAR sorttype AS INT INITIAL 1.
DEF VAR main-grp AS INT INITIAL 1.
DEF VAR from-store3 AS INT INITIAL 0.
DEF VAR to-store3 AS INT INITIAL 1.
DEF VAR show-price AS LOGICAL INITIAL YES.*/

DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

IF sorttype = 1 THEN RUN create-list.
ELSE RUN create-list2.

/*FOR EACH min-onhand-list:
    DISP min-onhand-list.
END.*/

PROCEDURE create-list: 
    DEFINE VARIABLE n1 AS INTEGER. 
    DEFINE VARIABLE n2 AS INTEGER. 
    DEFINE VARIABLE i  AS INTEGER.
    DEFINE VARIABLE curr-best AS DECIMAL FORMAT "->,>>9.999". 
    n1 = main-grp * 1000000. 
    n2 = (main-grp + 1) * 1000000 - 1. 

    FOR EACH min-onhand-list: 
        DELETE min-onhand-list. 
    END.

    FOR EACH l-lager WHERE l-lager.lager-nr GE from-store3 AND l-lager.lager-nr LE to-store3 NO-LOCK:
        i = 0.
        FOR EACH l-artikel WHERE l-artikel.artnr GE n1 AND l-artikel.artnr LE n2 AND l-artikel.min-best GT 0 NO-LOCK BY l-artikel.artnr: 
            curr-best = 0. 
            FIND FIRST l-bestand WHERE l-bestand.artnr = l-artikel.artnr AND l-bestand.lager-nr = l-lager.lager-nr NO-LOCK NO-ERROR. 
            IF AVAILABLE l-bestand THEN 
            DO:
                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-best THEN 
                DO: 
                    i = i + 1.
                    IF i = 1 THEN
                    DO:
                        CREATE min-onhand-list.
                        ASSIGN min-onhand-list.NAME = STRING(l-lager.lager-nr, "99") + " " + STRING(l-lager.bezeich, "x(13)").
                       
                    END.
                    CREATE min-onhand-list.
                        ASSIGN 
                           min-onhand-list.artnr      = l-artikel.artnr
                           min-onhand-list.name       = l-artikel.bezeich
                           min-onhand-list.min-oh     = l-artikel.min-best
                           min-onhand-list.curr-oh    = curr-best.
                    
                           min-onhand-list.avrgprice  = l-artikel.vk-preis.
                           min-onhand-list.ek-aktuell = l-artikel.ek-aktuell.
                    /*IF show-price THEN 
                    DO: 
                        IF long-digit THEN 
                        DO:
                            ASSIGN 
                               min-onhand-list.avrgprice  = STRING(l-artikel.vk-preis, ">,>>>,>>>,>>9")
                               min-onhand-list.ek-aktuell = STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9").
                        END.
                        ELSE
                        DO:
                            ASSIGN 
                               min-onhand-list.avrgprice  = STRING(l-artikel.vk-preis, ">,>>>,>>>,>>9.99")
                               min-onhand-list.ek-aktuell = STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9.99").
                        END.
                    END.*/
                    IF l-artikel.lieferfrist GT 0 THEN 
                    DO: 
                        FIND FIRST l-pprice WHERE l-pprice.artnr = l-artikel.artnr AND l-pprice.counter = l-artikel.lieferfrist USE-INDEX counter_ix NO-LOCK NO-ERROR. 
                        IF AVAILABLE l-pprice THEN 
                        DO:
                            ASSIGN min-onhand-list.datum      = l-pprice.bestelldatum.
                        END.
                    END. 
                END. 
            END.
        END.
    END.
END. 

PROCEDURE create-list2: 
    DEFINE VARIABLE n1 AS INTEGER. 
    DEFINE VARIABLE n2 AS INTEGER. 
    DEFINE VARIABLE i  AS INTEGER.
    DEFINE VARIABLE curr-best AS DECIMAL FORMAT "->,>>9.999". 
    n1 = main-grp * 1000000. 
    n2 = (main-grp + 1) * 1000000 - 1. 
    FOR EACH min-onhand-list: 
        DELETE min-onhand-list. 
    END.

    FOR EACH l-lager WHERE l-lager.lager-nr GE from-store3 AND l-lager.lager-nr LE to-store3 NO-LOCK:
        i = 0.
        FOR EACH l-artikel WHERE l-artikel.artnr GE n1 AND l-artikel.artnr LE n2 AND l-artikel.min-best GT 0 NO-LOCK BY l-artikel.bezeich: 
            curr-best = 0. 
            FIND FIRST l-bestand WHERE l-bestand.artnr = l-artikel.artnr AND l-bestand.lager-nr = l-lager.lager-nr NO-LOCK NO-ERROR. 
            IF AVAILABLE l-bestand THEN 
            DO:
                curr-best = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
                IF curr-best LT l-artikel.min-best THEN 
                DO: 
                    i = i + 1.
                    IF i = 1 THEN
                    DO:
                        CREATE min-onhand-list.
                        ASSIGN min-onhand-list.NAME = STRING(l-lager.lager-nr, "99") + " " + STRING(l-lager.bezeich, "x(13)").
                    END.
                    CREATE min-onhand-list.
                        ASSIGN 
                           min-onhand-list.artnr      = l-artikel.artnr
                           min-onhand-list.name       = l-artikel.bezeich
                           min-onhand-list.min-oh     = l-artikel.min-best
                           min-onhand-list.curr-oh    = curr-best.

                           min-onhand-list.avrgprice  = l-artikel.vk-preis.
                           min-onhand-list.ek-aktuell = l-artikel.ek-aktuell.
                    /*IF show-price THEN 
                    DO: 
                        IF long-digit THEN 
                        DO:
                             ASSIGN 
                                min-onhand-list.avrgprice  = STRING(l-artikel.vk-preis, ">,>>>,>>>,>>9")
                                min-onhand-list.ek-aktuell = STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9").
                        END.
                        ELSE
                        DO:
                            ASSIGN 
                               min-onhand-list.avrgprice  = STRING(l-artikel.vk-preis, ">,>>>,>>>,>>9.99")
                               min-onhand-list.ek-aktuell = STRING(l-artikel.ek-aktuell, ">,>>>,>>>,>>9.99").
                        END.
                    END.*/
                    IF l-artikel.lieferfrist GT 0 THEN 
                    DO: 
                        FIND FIRST l-pprice WHERE l-pprice.artnr = l-artikel.artnr AND l-pprice.counter = l-artikel.lieferfrist USE-INDEX counter_ix NO-LOCK NO-ERROR. 
                        IF AVAILABLE l-pprice THEN 
                        DO:
                            ASSIGN min-onhand-list.datum = l-pprice.bestelldatum.
                        END.
                    END. 
                END. 
            END.
        END.
    END.
END. 
