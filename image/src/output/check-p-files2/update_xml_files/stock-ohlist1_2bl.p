DEFINE TEMP-TABLE stockoh-list
    FIELD artnr       AS CHARACTER FORMAT "x(7)" 
    FIELD bezeich     AS CHARACTER FORMAT "x(30)" 
    FIELD prevqty     AS CHARACTER FORMAT "x(14)"
    FIELD prevval     AS CHARACTER FORMAT "x(14)" 
    FIELD incoming    AS CHARACTER FORMAT "x(14)"
    FIELD incomingval AS CHARACTER FORMAT "x(15)"
    FIELD outgoing    AS CHARACTER FORMAT "x(14)"
    FIELD outgoingval AS CHARACTER FORMAT "x(15)"
    FIELD actqty      AS CHARACTER FORMAT "x(14)" 
    FIELD actval      AS CHARACTER FORMAT "x(17)" 
    FIELD avrg-pr     AS CHARACTER FORMAT "x(19)".  /*gerald 'x(15)'*/ 


DEFINE INPUT PARAMETER from-lager   AS INTEGER.
DEFINE INPUT PARAMETER to-lager     AS INTEGER.
DEFINE INPUT PARAMETER from-art     AS INTEGER.
DEFINE INPUT PARAMETER to-art       AS INTEGER.
DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER move-art     AS LOGICAL.
DEFINE INPUT PARAMETER end-notzero  AS LOGICAL. /*FD Sept 15, 2021 => 861F7E Dwi S*/
DEFINE INPUT PARAMETER global-oh    AS LOGICAL. /*FD Sept 15, 2021 => 861F7E Dwi S*/
DEFINE OUTPUT PARAMETER TABLE FOR stockoh-list.

/*
DEFINE VARIABLE from-lager   AS INTEGER INITIAL 1.
DEFINE VARIABLE to-lager     AS INTEGER INITIAL 99.
DEFINE VARIABLE from-art     AS INTEGER.
DEFINE VARIABLE to-art       AS INTEGER INITIAL 99999999.
DEFINE VARIABLE from-date    AS DATE INITIAL 01/01/24.   
DEFINE VARIABLE to-date      AS DATE INITIAL 01/31/24.   
DEFINE VARIABLE move-art     AS LOGICAL INITIAL NO.
DEFINE VARIABLE end-notzero  AS LOGICAL INITIAL NO.
DEFINE VARIABLE global-oh    AS LOGICAL INITIAL NO.*/

DEFINE WORKFILE art-bestand 
  FIELD lager    AS INTEGER     FORMAT ">>9" 
  FIELD artnr    AS INTEGER     FORMAT ">>>>>>9" 
  FIELD zwkum    AS INTEGER 
  FIELD bezeich  AS CHARACTER   FORMAT "x(30)" 
  FIELD incoming AS DECIMAL     FORMAT "->,>>>,>>9.99" 
  FIELD in-val   AS DECIMAL     FORMAT "->>,>>>,>>9.99" 
  FIELD out-val  AS DECIMAL     FORMAT "->>,>>>,>>9.99" 
  FIELD outgoing AS DECIMAL     FORMAT "->,>>>,>>9.99" 
  FIELD prevqty  AS DECIMAL     FORMAT "->,>>>,>>9.99" 
  FIELD prevval  AS DECIMAL     FORMAT "->>,>>>,>>9.99" 
  FIELD adjust   AS DECIMAL     FORMAT "->>>,>>9.99" 
  FIELD actqty   AS DECIMAL     FORMAT "->,>>>,>>9.99" 
  FIELD actval   AS DECIMAL     FORMAT "->,>>>,>>>,>>9.99" 
  FIELD avrg-pr  AS DECIMAL     FORMAT "->>>,>>>,>>>,>>9.99". /*gerald >>>,>>>,>>9.99*/ 


DEFINE VARIABLE do-it       AS LOGICAL. 

DEFINE VARIABLE curr-art    AS INTEGER. 
DEFINE VARIABLE curr-lager  AS INTEGER. 
DEFINE VARIABLE out-bestand AS DECIMAL. 

DEFINE VARIABLE zwkum   AS INTEGER. 
DEFINE VARIABLE t-val   AS DECIMAL. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE VARIABLE j       AS INTEGER. 

DEFINE VARIABLE tot-prev    AS DECIMAL. 
DEFINE VARIABLE tot-value   AS DECIMAL. 
DEFINE VARIABLE tot-in      AS DECIMAL. 
DEFINE VARIABLE tot-out     AS DECIMAL. 
DEFINE VARIABLE total-in    AS DECIMAL. 
DEFINE VARIABLE total-out   AS DECIMAL. 
DEFINE VARIABLE total-prev  AS DECIMAL. 
DEFINE VARIABLE total-value AS DECIMAL. 
DEFINE VARIABLE tDate       AS DATE NO-UNDO.

/*naufal - bugs ending value stock article moving report NE actual value stock onhand*/
DEFINE VARIABLE qty         AS DECIMAL.
DEFINE VARIABLE wert        AS DECIMAL.
DEFINE BUFFER   l-oh        FOR l-bestand.
DEFINE BUFFER   l-ohis      FOR l-besthis.
DEFINE BUFFER   b-lager     FOR l-lager.
/***************************************************************************/
DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 
RUN htpdate.p (87, OUTPUT tDate).

STATUS DEFAULT "Processing...". 

/*ragung tambah validasi cek tahun*/

IF NOT global-oh THEN RUN create-stock1.
ELSE RUN create-stock2.

/****************************************************************************/
PROCEDURE create-stock1:
    /* Modify by Michael @ 19/07/2018 for displaying Stock On Hand history */
    IF YEAR(to-date) LT YEAR(tDate) AND YEAR(from-date) LT YEAR(tDate) THEN DO:
        IF MONTH(to-date) GT MONTH(tDate) AND MONTH(from-date) GT MONTH(tDate) THEN   
        DO:        
            FOR EACH l-lager WHERE lager-nr GE from-lager AND lager-nr LE to-lager NO-LOCK: 
                zwkum = 0. 
                t-val = 0. 
                FOR EACH l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr 
                    AND l-bestand.artnr GE from-art AND l-bestand.artnr LE to-art NO-LOCK, 
                    FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK 
                    BY l-artikel.zwkum BY l-artikel.artnr: 
                    do-it = YES. 
                    /*M
                    IF from-grp > 0 THEN 
                        IF l-artikel.zwkum LT from-grp OR l-artikel.zwkum GT to-grp THEN do-it = NO. 
                    */
            
                    IF do-it THEN 
                    DO: 
                        FIND FIRST art-bestand WHERE art-bestand.artnr EQ l-bestand.artnr 
                            AND art-bestand.lager EQ l-lager.lager-nr NO-ERROR. 
                        IF NOT AVAILABLE art-bestand THEN 
                        DO: 
                            CREATE art-bestand. 
                            art-bestand.bezeich = l-artikel.bezeich. 
                            art-bestand.zwkum = l-artikel.zwkum. 
                            art-bestand.artnr = l-bestand.artnr. 
                            art-bestand.lager = l-lager.lager-nr. 
            
                            /* INITIAL values */ 
                            art-bestand.prevqty = l-bestand.anz-anf-best. 
                            art-bestand.prevval = l-bestand.val-anf-best. 
                            art-bestand.actqty  = l-bestand.anz-anf-best. 
                            art-bestand.actval  = l-bestand.val-anf-best. 
            
                            curr-art = l-bestand.artnr. 
                            curr-lager = l-lager.lager-nr. 
                        END. 
                        out-bestand = 0. 
            
                        /*  calculate the incoming- AND outgoing stocks within the given periods */ 
                        FOR EACH l-op WHERE l-op.lager-nr = l-lager.lager-nr 
                           AND l-op.artnr = l-bestand.artnr 
                           AND (l-op.datum GE from-date AND l-op.datum LE to-date) 
                           AND loeschflag LE 1 NO-LOCK BY l-op.datum: 
                           IF l-op.op-art = 1 OR l-op.op-art = 2 THEN 
                           DO: 
                               art-bestand.incoming = art-bestand.incoming + l-op.anzahl. 
                               art-bestand.in-val   = art-bestand.in-val + l-op.anzahl * l-artikel.vk-preis.
                               /*art-bestand.in-val   = art-bestand.in-val + l-op.anzahl * l-op.einzelpreis. */
                               /*art-bestand.in-val    = art-bestand.in-val + l-bestand.wert-eingang.  */
                               art-bestand.actqty   = art-bestand.actqty + l-op.anzahl. 
                               art-bestand.actval  = art-bestand.actval 
                                                    + l-op.anzahl * l-artikel.vk-preis. 
                               /*art-bestand.actval   = art-bestand.actval + l-op.warenwert. */
                           END. 
                           ELSE IF l-op.op-art = 3 OR l-op.op-art = 4 THEN 
                           DO: 
                               art-bestand.outgoing = art-bestand.outgoing + l-op.anzahl. 
                               art-bestand.out-val  = art-bestand.out-val + l-op.anzahl * l-artikel.vk-preis.
                               /*art-bestand.out-val  = art-bestand.out-val + l-op.anzahl * l-op.einzelpreis. */
                               /*art-bestand.out-val  = art-bestand.out-val + l-bestand.wert-ausgang. */
                               art-bestand.actqty   = art-bestand.actqty - l-op.anzahl. 
                               art-bestand.actval  = art-bestand.actval 
                                                    - l-op.anzahl * l-artikel.vk-preis.  
                               /*art-bestand.actval   = art-bestand.actval - l-op.warenwert. */
                           END. 
                        END.
                        /*naufal - bugs ending value stock article moving report NE actual value stock onhand*/
                        /*FIND FIRST l-oh WHERE l-oh.artnr EQ l-bestand.artnr AND l-oh.lager-nr EQ 0 NO-LOCK NO-ERROR.
                        qty = l-oh.anz-anf-best + l-oh.anz-eingang - l-oh.anz-ausgang.
                        wert = l-oh.val-anf-best + l-oh.wert-eingang - l-oh.wert-ausgang.
                        art-bestand.actval = wert * art-bestand.actqty / qty. */
                        /*end naufal*/
                    END.
                END. 
            END. 
        END.
        /* End of modify */
    END.
    ELSE DO:
    /*IF MONTH(to-date) EQ MONTH(tDate) AND MONTH(from-date) EQ MONTH(tDate) THEN */
        IF MONTH(to-date) LE MONTH(tDate) AND MONTH(from-date) LE MONTH(tDate) THEN   /*gerald l-bestand yang terlewat dimunculkan Robot n Co FC049F */
        DO:        
            FOR EACH b-lager WHERE b-lager.lager-nr GE from-lager AND b-lager.lager-nr LE to-lager NO-LOCK: 
                zwkum = 0. 
                t-val = 0. 
                FOR EACH l-bestand WHERE l-bestand.lager-nr = b-lager.lager-nr 
                    AND l-bestand.artnr GE from-art AND l-bestand.artnr LE to-art NO-LOCK, 
                    FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK 
                    BY l-artikel.zwkum BY l-artikel.artnr: 
                    do-it = YES. 
                    /*M
                    IF from-grp > 0 THEN 
                        IF l-artikel.zwkum LT from-grp OR l-artikel.zwkum GT to-grp THEN do-it = NO. 
                    */
            
                    IF do-it THEN 
                    DO: 
                        FIND FIRST art-bestand WHERE art-bestand.artnr EQ l-bestand.artnr 
                            AND art-bestand.lager EQ b-lager.lager-nr NO-ERROR. 
                        IF NOT AVAILABLE art-bestand THEN 
                        DO: 
                            CREATE art-bestand. 
                            art-bestand.bezeich = l-artikel.bezeich. 
                            art-bestand.zwkum = l-artikel.zwkum. 
                            art-bestand.artnr = l-bestand.artnr. 
                            art-bestand.lager = b-lager.lager-nr. 
            
                            /* INITIAL values */ 
                            art-bestand.prevqty = l-bestand.anz-anf-best. 
                            art-bestand.prevval = l-bestand.val-anf-best. 
                            art-bestand.actqty  = l-bestand.anz-anf-best. 
                            art-bestand.actval  = l-bestand.val-anf-best. 
            
                            curr-art = l-bestand.artnr. 
                            curr-lager = b-lager.lager-nr. 
                        END. 
                        out-bestand = 0. 
            
                        /*  calculate the incoming- AND outgoing stocks within the given periods */ 
                        FOR EACH l-op WHERE l-op.lager-nr = b-lager.lager-nr 
                           AND l-op.artnr = l-bestand.artnr 
                           AND (l-op.datum GE from-date AND l-op.datum LE to-date) 
                           AND loeschflag LE 1 NO-LOCK BY l-op.datum: 
                           IF l-op.op-art = 1 OR l-op.op-art = 2 THEN 
                           DO: 
                               art-bestand.incoming = art-bestand.incoming + l-op.anzahl. 
                               art-bestand.in-val   = art-bestand.in-val + l-op.anzahl * l-artikel.vk-preis.
                               /*art-bestand.in-val   = art-bestand.in-val + l-op.anzahl * l-op.einzelpreis. */
                               /*art-bestand.in-val    = art-bestand.in-val + l-bestand.wert-eingang.  */
                               art-bestand.actqty   = art-bestand.actqty + l-op.anzahl. 
                               art-bestand.actval  = art-bestand.actval 
                                                    + l-op.anzahl * l-artikel.vk-preis. 
                               /*art-bestand.actval   = art-bestand.actval + l-op.warenwert. */
                           END. 
                           ELSE IF l-op.op-art = 3 OR l-op.op-art = 4 THEN 
                           DO: 
                               art-bestand.outgoing = art-bestand.outgoing + l-op.anzahl. 
                               art-bestand.out-val  = art-bestand.out-val + l-op.anzahl * l-artikel.vk-preis.
                               /*art-bestand.out-val  = art-bestand.out-val + l-op.anzahl * l-op.einzelpreis. */
                               /*art-bestand.out-val  = art-bestand.out-val + l-bestand.wert-ausgang. */
                               art-bestand.actqty   = art-bestand.actqty - l-op.anzahl. 
                               art-bestand.actval  = art-bestand.actval 
                                                    - l-op.anzahl * l-artikel.vk-preis.  
                               /*art-bestand.actval   = art-bestand.actval - l-op.warenwert. */
                           END. 
                        END.
                        /*naufal - bugs ending value stock article moving report NE actual value stock onhand*/
                        /*FIND FIRST l-oh WHERE l-oh.artnr EQ l-bestand.artnr AND l-oh.lager-nr EQ 0 NO-LOCK NO-ERROR.
                        qty = l-oh.anz-anf-best + l-oh.anz-eingang - l-oh.anz-ausgang.
                        wert = l-oh.val-anf-best + l-oh.wert-eingang - l-oh.wert-ausgang.
                        art-bestand.actval = wert * art-bestand.actqty / qty. */
                        /*end naufal*/
                    END.
                END. 
            END. 
        END.
        /* End of modify */
    END.
    /* FD Comment => For OnHand History is on Lists - Closed INV List
    /* Added by Michael @ 19/07/2018 for displaying Stock On Hand history */
    /*IF MONTH(to-date) LT MONTH(tDate) AND MONTH(tDate) LT MONTH(TODAY) THEN*/
    /*IF MONTH(to-date) LT MONTH(tDate) AND MONTH(from-date) LT MONTH(tDate) THEN*/
    IF to-date LT tDate AND from-date LT tDate THEN
    DO:
        /*MESSAGE "Masuk blok apabila from-date & to-date dibulan yang sudah lewat" VIEW-AS ALERT-BOX INFO.*/
        FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager AND l-lager.lager-nr LE to-lager NO-LOCK: 
            zwkum = 0. 
            t-val = 0. 
            FOR EACH l-besthis WHERE l-besthis.lager-nr = l-lager.lager-nr 
                AND l-besthis.artnr GE from-art AND l-besthis.artnr LE to-art 
                AND l-besthis.anf-best-dat GE from-date AND l-besthis.anf-best-dat LE to-date NO-LOCK, 
                FIRST l-artikel WHERE l-artikel.artnr = l-besthis.artnr NO-LOCK 
                BY l-artikel.zwkum BY l-artikel.artnr: 
                do-it = YES. 
                /*M
                IF from-grp > 0 THEN 
                    IF l-artikel.zwkum LT from-grp OR l-artikel.zwkum GT to-grp THEN do-it = NO. 
                */
        
                IF do-it THEN 
                DO: 
                    FIND FIRST art-bestand WHERE art-bestand.artnr EQ l-besthis.artnr 
                        AND art-bestand.lager EQ l-lager.lager-nr NO-ERROR. 
                    IF NOT AVAILABLE art-bestand THEN 
                    DO: 
                        CREATE art-bestand. 
                        art-bestand.bezeich = l-artikel.bezeich. 
                        art-bestand.zwkum = l-artikel.zwkum. 
                        art-bestand.artnr = l-besthis.artnr. 
                        art-bestand.lager = l-lager.lager-nr. 
        
                        /* INITIAL values */ 
                        art-bestand.prevqty = l-besthis.anz-anf-best. 
                        art-bestand.prevval = l-besthis.val-anf-best. 
                        art-bestand.actqty  = l-besthis.anz-anf-best. 
                        art-bestand.actval  = l-besthis.val-anf-best. 
        
                        curr-art = l-besthis.artnr. 
                        curr-lager = l-lager.lager-nr. 
                    END. 
                    out-bestand = 0. 
        
                    /*  calculate the incoming- AND outgoing stocks within the given periods */ 
                    FOR EACH l-ophis WHERE l-ophis.lager-nr = l-lager.lager-nr 
                       AND l-ophis.artnr = l-besthis.artnr 
                       AND (l-ophis.datum GE from-date AND l-ophis.datum LE to-date) NO-LOCK BY l-ophis.datum: 
                       IF l-ophis.op-art = 1 OR l-ophis.op-art = 2 THEN 
                       DO: 
                           art-bestand.incoming = art-bestand.incoming + l-ophis.anzahl. 
                           art-bestand.in-val   = art-bestand.in-val + l-ophis.anzahl * l-artikel.vk-preis. 
                           art-bestand.actqty   = art-bestand.actqty + l-ophis.anzahl. 
                           art-bestand.actval  = art-bestand.actval 
                                                + l-ophis.anzahl * l-artikel.vk-preis. 
                           /*art-bestand.actval   = art-bestand.actval + l-ophis.warenwert. */
                       END. 
                       ELSE IF l-ophis.op-art = 3 OR l-ophis.op-art = 4 THEN 
                       DO: 
                           art-bestand.outgoing = art-bestand.outgoing + l-ophis.anzahl. 
                           art-bestand.out-val  = art-bestand.out-val + l-ophis.anzahl * l-artikel.vk-preis. 
                           art-bestand.actqty   = art-bestand.actqty - l-ophis.anzahl. 
                           art-bestand.actval  = art-bestand.actval 
                                                - l-ophis.anzahl * l-artikel.vk-preis.
                           /*art-bestand.actval   = art-bestand.actval - l-ophis.warenwert. */
                       END. 
                    END.
                    /*naufal - bugs ending value stock article moving report NE actual value stock onhand*/
                    /*FIND FIRST l-ohis WHERE l-ohis.artnr EQ l-besthis.artnr AND l-ohis.lager-nr EQ 0 
                        AND l-ohis.anf-best-dat GE from-date AND l-ohis.anf-best-dat LE to-date NO-LOCK NO-ERROR.
                    qty = l-ohis.anz-anf-best + l-ohis.anz-eingang - l-ohis.anz-ausgang.
                    wert = l-ohis.val-anf-best + l-ohis.wert-eingang - l-ohis.wert-ausgang.
                    art-bestand.actval = wert * art-bestand.actqty / qty.*/
                    /*end naufal*/
                END.
            END. 
        END.
    END.
    /* End of added */
    */
     
    FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
        AND l-lager.lager-nr LE to-lager NO-LOCK:
        bezeich = "". 
        CREATE stockoh-list. 
        stockoh-list.bezeich = STRING(l-lager.lager-nr, "99") + " - " + STRING(l-lager.bezeich, "x(25)"). 
    
        tot-prev = 0. 
        tot-in = 0. 
        tot-out = 0. 
        tot-value = 0. 
        total-value = 0.
        zwkum = 0.
        t-val = 0. 
    
        FOR EACH art-bestand WHERE art-bestand.lager = l-lager.lager-nr  
            AND art-bestand.artnr GE from-art AND art-bestand.artnr LE to-art NO-LOCK 
            BY art-bestand.zwkum BY art-bestand.bezeich: 

            IF (move-art AND end-notzero) AND (art-bestand.incoming NE 0  
                OR art-bestand.outgoing NE 0 OR art-bestand.actqty NE 0) THEN 
            DO:                 
                IF zwkum = 0 THEN 
                DO: 
                    zwkum = art-bestand.zwkum. 
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                    bezeich = l-untergrup.bezeich. 
                END. 
                IF zwkum NE art-bestand.zwkum THEN 
                DO: 
                    CREATE stockoh-list.    
                    /*M
                    DO j = 1 TO 64: 
                        stockoh-list.s = stockoh-list.s + " ". 
                    END. 
                    */
                    IF NOT long-digit THEN 
                    DO:
                        ASSIGN 
                            stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                    + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                            stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9.99"). 
                    END.                        
                    ELSE 
                    DO:
                        ASSIGN 
                            stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                    + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                            stockoh-list.actval  = STRING(t-val, "->>,>>>,>>>,>>9"). 
                    END.
                        
    
                    t-val = 0. 
                    zwkum = art-bestand.zwkum. 
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                    bezeich = l-untergrup.bezeich. 
                END. 
    
                FIND FIRST l-artikel WHERE l-artikel.artnr = art-bestand.artnr NO-LOCK.
                IF art-bestand.avrg-pr = 0 THEN 
                DO:
                    IF art-bestand.actqty NE 0 THEN
                        art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                    ELSE 
                    DO:
                        ASSIGN  
                            art-bestand.avrg-pr = l-artikel.vk-preis
                            art-bestand.actval  = 0.
                    END.                        
                END.                    
                
                CREATE stockoh-list. 
                IF NOT long-digit THEN 
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)")
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>>,>>>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
                END.                    
                ELSE
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)") 
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
                END.
                       
                t-val = t-val + art-bestand.actval. 
                tot-in = tot-in + art-bestand.in-val. 
                tot-out = tot-out + art-bestand.out-val. 
                tot-prev = tot-prev + art-bestand.prevval. 
                tot-value = tot-value + art-bestand.actval. 
                total-in = total-in + art-bestand.in-val. 
                total-out = total-out + art-bestand.out-val. 
                total-prev = total-prev + art-bestand.prevval. 
                total-value = total-value + art-bestand.actval. 
            END. 
            ELSE IF (move-art AND NOT end-notzero) AND 
                (art-bestand.incoming NE 0 OR art-bestand.outgoing NE 0) THEN 
            DO:                  
                IF zwkum = 0 THEN 
                DO: 
                    zwkum = art-bestand.zwkum. 
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                    bezeich = l-untergrup.bezeich. 
                END. 
                IF zwkum NE art-bestand.zwkum THEN 
                DO: 
                    CREATE stockoh-list.    
                    /*M
                    DO j = 1 TO 64: 
                        stockoh-list.s = stockoh-list.s + " ". 
                    END. 
                    */
                    IF NOT long-digit THEN 
                    DO:
                        ASSIGN 
                            stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                    + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                            stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9.99"). 
                    END.                        
                    ELSE 
                    DO:
                        ASSIGN 
                            stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                    + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                            stockoh-list.actval  = STRING(t-val, "->>,>>>,>>>,>>9"). 
                    END.
                        
    
                    t-val = 0. 
                    zwkum = art-bestand.zwkum. 
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                    bezeich = l-untergrup.bezeich. 
                END. 
    
                FIND FIRST l-artikel WHERE l-artikel.artnr = art-bestand.artnr NO-LOCK.
                IF art-bestand.avrg-pr = 0 THEN 
                DO:
                    IF art-bestand.actqty NE 0 THEN
                        art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                    ELSE 
                    DO:
                        ASSIGN  
                            art-bestand.avrg-pr = l-artikel.vk-preis
                            art-bestand.actval  = 0.
                    END.                        
                END.                    
                
                CREATE stockoh-list. 
                IF NOT long-digit THEN 
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)")
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>>,>>>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
                END.                    
                ELSE
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)") 
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
                END.
                       
                t-val = t-val + art-bestand.actval. 
                tot-in = tot-in + art-bestand.in-val. 
                tot-out = tot-out + art-bestand.out-val. 
                tot-prev = tot-prev + art-bestand.prevval. 
                tot-value = tot-value + art-bestand.actval. 
                total-in = total-in + art-bestand.in-val. 
                total-out = total-out + art-bestand.out-val. 
                total-prev = total-prev + art-bestand.prevval. 
                total-value = total-value + art-bestand.actval. 
            END. 
            ELSE IF (NOT move-art AND end-notzero) AND (art-bestand.actqty NE 0) THEN 
            DO:                  
                IF zwkum = 0 THEN 
                DO: 
                    zwkum = art-bestand.zwkum. 
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                    bezeich = l-untergrup.bezeich. 
                END. 
                IF zwkum NE art-bestand.zwkum THEN 
                DO: 
                    CREATE stockoh-list.    
                    /*M
                    DO j = 1 TO 64: 
                        stockoh-list.s = stockoh-list.s + " ". 
                    END. 
                    */
                    IF NOT long-digit THEN 
                    DO:
                        ASSIGN 
                            stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                    + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                            stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9.99"). 
                    END.                        
                    ELSE 
                    DO:
                        ASSIGN 
                            stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                    + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                            stockoh-list.actval  = STRING(t-val, "->>,>>>,>>>,>>9"). 
                    END.
                        
    
                    t-val = 0. 
                    zwkum = art-bestand.zwkum. 
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                    bezeich = l-untergrup.bezeich. 
                END. 
    
                FIND FIRST l-artikel WHERE l-artikel.artnr = art-bestand.artnr NO-LOCK.
                IF art-bestand.avrg-pr = 0 THEN 
                DO:
                    IF art-bestand.actqty NE 0 THEN
                        art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                    ELSE 
                    DO:
                        ASSIGN  
                            art-bestand.avrg-pr = l-artikel.vk-preis
                            art-bestand.actval  = 0.
                    END.                        
                END.                    
                
                CREATE stockoh-list. 
                IF NOT long-digit THEN 
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)")
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>>,>>>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
                END.                    
                ELSE
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)") 
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
                END.
                       
                t-val = t-val + art-bestand.actval. 
                tot-in = tot-in + art-bestand.in-val. 
                tot-out = tot-out + art-bestand.out-val. 
                tot-prev = tot-prev + art-bestand.prevval. 
                tot-value = tot-value + art-bestand.actval. 
                total-in = total-in + art-bestand.in-val. 
                total-out = total-out + art-bestand.out-val. 
                total-prev = total-prev + art-bestand.prevval. 
                total-value = total-value + art-bestand.actval. 
            END. 
            ELSE IF (NOT move-art AND NOT end-notzero) THEN 
            DO:                  
                IF zwkum = 0 THEN 
                DO: 
                    zwkum = art-bestand.zwkum. 
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                    bezeich = l-untergrup.bezeich. 
                END. 
                IF zwkum NE art-bestand.zwkum THEN 
                DO: 
                    CREATE stockoh-list.    
                    /*M
                    DO j = 1 TO 64: 
                        stockoh-list.s = stockoh-list.s + " ". 
                    END. 
                    */
                    IF NOT long-digit THEN 
                    DO:
                        ASSIGN 
                            stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                    + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                            stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9.99"). 
                    END.                        
                    ELSE 
                    DO:
                        ASSIGN 
                            stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                    + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                            stockoh-list.actval  = STRING(t-val, "->>,>>>,>>>,>>9"). 
                    END.
                        
    
                    t-val = 0. 
                    zwkum = art-bestand.zwkum. 
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                    bezeich = l-untergrup.bezeich. 
                END. 
    
                FIND FIRST l-artikel WHERE l-artikel.artnr = art-bestand.artnr NO-LOCK.
                IF art-bestand.avrg-pr = 0 THEN 
                DO:
                    IF art-bestand.actqty NE 0 THEN
                        art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                    ELSE 
                    DO:
                        ASSIGN  
                            art-bestand.avrg-pr = l-artikel.vk-preis
                            art-bestand.actval  = 0.
                    END.                        
                END.                    
                
                CREATE stockoh-list. 
                IF NOT long-digit THEN 
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)")
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>>,>>>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
                END.                    
                ELSE
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)") 
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
                END.
                       
                t-val = t-val + art-bestand.actval. 
                tot-in = tot-in + art-bestand.in-val. 
                tot-out = tot-out + art-bestand.out-val. 
                tot-prev = tot-prev + art-bestand.prevval. 
                tot-value = tot-value + art-bestand.actval. 
                total-in = total-in + art-bestand.in-val. 
                total-out = total-out + art-bestand.out-val. 
                total-prev = total-prev + art-bestand.prevval. 
                total-value = total-value + art-bestand.actval. 
            END. 
        END. 
        
        IF bezeich NE "" THEN 
        DO: 
            CREATE stockoh-list. 
            IF NOT long-digit THEN 
            DO:
                ASSIGN 
                    stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                            + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                    stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9.99"). 
            END.                
            ELSE
            DO:
                ASSIGN 
                    stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                            + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                    stockoh-list.actval  = STRING(t-val, "->>,>>>,>>>,>>9").
            END.
                
            /*Naufal - Add total value per store*/
            CREATE stockoh-list.
            IF NOT long-digit THEN
            DO:
                ASSIGN 
                    stockoh-list.bezeich = "Ttl " + STRING(l-lager.bezeich, "x(25)") 
                    stockoh-list.actval  = STRING(tot-value, "->,>>>,>>>,>>9.99").
            END.                
            ELSE
            DO:
                ASSIGN
                    stockoh-list.bezeich = "Ttl " + STRING(l-lager.bezeich, "x(25)")
                    stockoh-list.actval  = STRING(tot-value, "->>,>>>,>>>,>>9").
            END.                
            CREATE stockoh-list.
            /*end*/
        END.
    END.
    IF NOT long-digit THEN
    DO:
        ASSIGN
            stockoh-list.bezeich = "G R A N D  T O T A L"
            stockoh-list.actval  = STRING(total-value, "->,>>>,>>>,>>9.99").
    END.        
    ELSE
    DO:
        ASSIGN
            stockoh-list.bezeich = "G R A N D  T O T A L"
            stockoh-list.actval  = STRING(total-value, "->>,>>>,>>>,>>9").
    END.                
     
    FOR EACH art-bestand: 
      DELETE art-bestand. 
    END.
END PROCEDURE.

PROCEDURE create-stock2:
    IF YEAR(to-date) LE YEAR(tDate) AND YEAR(from-date) LE YEAR(tDate) THEN DO:
        IF MONTH(to-date) GT MONTH(tDate) AND MONTH(from-date) GT MONTH(tDate) THEN   
        DO:
             FOR EACH l-bestand WHERE l-bestand.lager-nr EQ 0
                AND l-bestand.artnr GE from-art AND l-bestand.artnr LE to-art NO-LOCK, 
                FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK 
                BY l-artikel.zwkum BY l-artikel.artnr: 
                do-it = YES. 
                /*M
                IF from-grp > 0 THEN 
                    IF l-artikel.zwkum LT from-grp OR l-artikel.zwkum GT to-grp THEN do-it = NO. 
                */
        
                IF do-it THEN 
                DO:                 
                    CREATE art-bestand. 
                    art-bestand.bezeich = l-artikel.bezeich. 
                    art-bestand.zwkum = l-artikel.zwkum. 
                    art-bestand.artnr = l-bestand.artnr. 
                    art-bestand.lager = l-bestand.lager-nr. 
    
                    /* INITIAL values */ 
                    art-bestand.prevqty = l-bestand.anz-anf-best. 
                    art-bestand.prevval = l-bestand.val-anf-best. 
                    art-bestand.actqty  = l-bestand.anz-anf-best. 
                    art-bestand.actval  = l-bestand.val-anf-best.                     
                END.
            END.
                
            /*New Metode calculate the incoming- AND outgoing stocks within the given periods*/ 
            FOR EACH art-bestand NO-LOCK,
                FIRST l-artikel WHERE l-artikel.artnr = art-bestand.artnr NO-LOCK 
                BY art-bestand.zwkum BY art-bestand.artnr: 
    
                FOR EACH l-op WHERE l-op.artnr EQ art-bestand.artnr 
                    AND (l-op.datum GE from-date AND l-op.datum LE to-date) 
                    AND loeschflag LE 1 NO-LOCK BY l-op.datum: 
    
                    IF l-op.op-art = 1 OR l-op.op-art = 2 THEN 
                    DO: 
                        art-bestand.incoming = art-bestand.incoming + l-op.anzahl. 
                        art-bestand.in-val   = art-bestand.in-val + l-op.anzahl * l-artikel.vk-preis.                   
                        art-bestand.actqty   = art-bestand.actqty + l-op.anzahl. 
                        art-bestand.actval   = art-bestand.actval + l-op.anzahl * l-artikel.vk-preis.
                    END. 
                    ELSE IF l-op.op-art = 3 OR l-op.op-art = 4 THEN 
                    DO: 
                        art-bestand.outgoing = art-bestand.outgoing + l-op.anzahl. 
                        art-bestand.out-val  = art-bestand.out-val + l-op.anzahl * l-artikel.vk-preis.                   
                        art-bestand.actqty   = art-bestand.actqty - l-op.anzahl. 
                        art-bestand.actval   = art-bestand.actval - l-op.anzahl * l-artikel.vk-preis.
                    END. 
                END.            
            END.    
        END.
    END.
    ELSE DO:
        IF MONTH(to-date) LE MONTH(tDate) AND MONTH(from-date) LE MONTH(tDate) THEN   /*gerald l-bestand yang terlewat dimunculkan Robot n Co FC049F */
        DO:           
            /*New Metode*/
            FOR EACH l-bestand WHERE l-bestand.lager-nr EQ 0
                AND l-bestand.artnr GE from-art AND l-bestand.artnr LE to-art NO-LOCK, 
                FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr NO-LOCK 
                BY l-artikel.zwkum BY l-artikel.artnr: 
                do-it = YES. 
                /*M
                IF from-grp > 0 THEN 
                    IF l-artikel.zwkum LT from-grp OR l-artikel.zwkum GT to-grp THEN do-it = NO. 
                */
        
                IF do-it THEN 
                DO:                 
                    CREATE art-bestand. 
                    art-bestand.bezeich = l-artikel.bezeich. 
                    art-bestand.zwkum = l-artikel.zwkum. 
                    art-bestand.artnr = l-bestand.artnr. 
                    art-bestand.lager = l-bestand.lager-nr. 
    
                    /* INITIAL values */ 
                    art-bestand.prevqty = l-bestand.anz-anf-best. 
                    art-bestand.prevval = l-bestand.val-anf-best. 
                    art-bestand.actqty  = l-bestand.anz-anf-best. 
                    art-bestand.actval  = l-bestand.val-anf-best.                     
                END.
            END.
                
            /*New Metode calculate the incoming- AND outgoing stocks within the given periods*/ 
            FOR EACH art-bestand NO-LOCK,
                FIRST l-artikel WHERE l-artikel.artnr = art-bestand.artnr NO-LOCK 
                BY art-bestand.zwkum BY art-bestand.artnr: 
    
                FOR EACH l-op WHERE l-op.artnr EQ art-bestand.artnr 
                    AND (l-op.datum GE from-date AND l-op.datum LE to-date) 
                    AND loeschflag LE 1 NO-LOCK BY l-op.datum: 
    
                    IF l-op.op-art = 1 OR l-op.op-art = 2 THEN 
                    DO: 
                        art-bestand.incoming = art-bestand.incoming + l-op.anzahl. 
                        art-bestand.in-val   = art-bestand.in-val + l-op.anzahl * l-artikel.vk-preis.                   
                        art-bestand.actqty   = art-bestand.actqty + l-op.anzahl. 
                        art-bestand.actval   = art-bestand.actval + l-op.anzahl * l-artikel.vk-preis.
                    END. 
                    ELSE IF l-op.op-art = 3 OR l-op.op-art = 4 THEN 
                    DO: 
                        art-bestand.outgoing = art-bestand.outgoing + l-op.anzahl. 
                        art-bestand.out-val  = art-bestand.out-val + l-op.anzahl * l-artikel.vk-preis.                   
                        art-bestand.actqty   = art-bestand.actqty - l-op.anzahl. 
                        art-bestand.actval   = art-bestand.actval - l-op.anzahl * l-artikel.vk-preis.
                    END. 
                END.            
            END.                        
        END.
    END.

    bezeich = "". 
    CREATE stockoh-list. 
    stockoh-list.bezeich = STRING("00") + " - " + STRING("ALL STORE"). 
    
    tot-prev = 0. 
    tot-in = 0. 
    tot-out = 0. 
    tot-value = 0. 
    total-value = 0.
    zwkum = 0.
    t-val = 0. 

    FOR EACH art-bestand WHERE art-bestand.artnr GE from-art 
        AND art-bestand.artnr LE to-art NO-LOCK 
        BY art-bestand.zwkum BY art-bestand.bezeich: 

        IF (move-art AND end-notzero) AND (art-bestand.incoming NE 0  
            OR art-bestand.outgoing NE 0 OR art-bestand.actqty NE 0) THEN 
        DO: 
            IF zwkum = 0 THEN 
            DO: 
                zwkum = art-bestand.zwkum. 
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                bezeich = l-untergrup.bezeich. 
            END. 
            IF zwkum NE art-bestand.zwkum THEN 
            DO: 
                CREATE stockoh-list.    
                /*M
                DO j = 1 TO 64: 
                    stockoh-list.s = stockoh-list.s + " ". 
                END. 
                */
                IF NOT long-digit THEN 
                DO:
                    ASSIGN 
                        stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                        stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9.99"). 
                END.                        
                ELSE 
                DO:
                    ASSIGN 
                        stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                        stockoh-list.actval  = STRING(t-val, "->>,>>>,>>>,>>9"). 
                END.
                    
    
                t-val = 0. 
                zwkum = art-bestand.zwkum. 
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                bezeich = l-untergrup.bezeich. 
            END. 
    
            FIND FIRST l-artikel WHERE l-artikel.artnr = art-bestand.artnr NO-LOCK.
            IF art-bestand.avrg-pr = 0 THEN 
            DO:
                IF art-bestand.actqty NE 0 THEN
                    art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                ELSE 
                DO:
                    ASSIGN  
                        art-bestand.avrg-pr = l-artikel.vk-preis
                        art-bestand.actval  = 0.
                END.                        
            END.                    
            
            CREATE stockoh-list. 
            IF NOT long-digit THEN 
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)")
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>>,>>>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
            END.                    
            ELSE
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)") 
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
            END.
                   
            t-val = t-val + art-bestand.actval. 
            tot-in = tot-in + art-bestand.in-val. 
            tot-out = tot-out + art-bestand.out-val. 
            tot-prev = tot-prev + art-bestand.prevval. 
            tot-value = tot-value + art-bestand.actval. 
            total-in = total-in + art-bestand.in-val. 
            total-out = total-out + art-bestand.out-val. 
            total-prev = total-prev + art-bestand.prevval. 
            total-value = total-value + art-bestand.actval. 
        END. 
        ELSE IF (move-art AND NOT end-notzero) AND 
            (art-bestand.incoming NE 0 OR art-bestand.outgoing NE 0) THEN 
        DO: 
            IF zwkum = 0 THEN 
            DO: 
                zwkum = art-bestand.zwkum. 
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                bezeich = l-untergrup.bezeich. 
            END. 
            IF zwkum NE art-bestand.zwkum THEN 
            DO: 
                CREATE stockoh-list.    
                /*M
                DO j = 1 TO 64: 
                    stockoh-list.s = stockoh-list.s + " ". 
                END. 
                */
                IF NOT long-digit THEN 
                DO:
                    ASSIGN 
                        stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                        stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9.99"). 
                END.                        
                ELSE 
                DO:
                    ASSIGN 
                        stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                        stockoh-list.actval  = STRING(t-val, "->>,>>>,>>>,>>9"). 
                END.
                    
    
                t-val = 0. 
                zwkum = art-bestand.zwkum. 
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                bezeich = l-untergrup.bezeich. 
            END. 
    
            FIND FIRST l-artikel WHERE l-artikel.artnr = art-bestand.artnr NO-LOCK.
            IF art-bestand.avrg-pr = 0 THEN 
            DO:
                IF art-bestand.actqty NE 0 THEN
                    art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                ELSE 
                DO:
                    ASSIGN  
                        art-bestand.avrg-pr = l-artikel.vk-preis
                        art-bestand.actval  = 0.
                END.                        
            END.                    
            
            CREATE stockoh-list. 
            IF NOT long-digit THEN 
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)")
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>>,>>>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
            END.                    
            ELSE
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)") 
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
            END.
                   
            t-val = t-val + art-bestand.actval. 
            tot-in = tot-in + art-bestand.in-val. 
            tot-out = tot-out + art-bestand.out-val. 
            tot-prev = tot-prev + art-bestand.prevval. 
            tot-value = tot-value + art-bestand.actval. 
            total-in = total-in + art-bestand.in-val. 
            total-out = total-out + art-bestand.out-val. 
            total-prev = total-prev + art-bestand.prevval. 
            total-value = total-value + art-bestand.actval. 
        END. 
        IF (NOT move-art AND end-notzero) AND (art-bestand.actqty NE 0) THEN 
        DO: 
            IF zwkum = 0 THEN 
            DO: 
                zwkum = art-bestand.zwkum. 
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                bezeich = l-untergrup.bezeich. 
            END. 
            IF zwkum NE art-bestand.zwkum THEN 
            DO: 
                CREATE stockoh-list.    
                /*M
                DO j = 1 TO 64: 
                    stockoh-list.s = stockoh-list.s + " ". 
                END. 
                */
                IF NOT long-digit THEN 
                DO:
                    ASSIGN 
                        stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                        stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9.99"). 
                END.                        
                ELSE 
                DO:
                    ASSIGN 
                        stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                        stockoh-list.actval  = STRING(t-val, "->>,>>>,>>>,>>9"). 
                END.
                    
    
                t-val = 0. 
                zwkum = art-bestand.zwkum. 
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                bezeich = l-untergrup.bezeich. 
            END. 
    
            FIND FIRST l-artikel WHERE l-artikel.artnr = art-bestand.artnr NO-LOCK.
            IF art-bestand.avrg-pr = 0 THEN 
            DO:
                IF art-bestand.actqty NE 0 THEN
                    art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                ELSE 
                DO:
                    ASSIGN  
                        art-bestand.avrg-pr = l-artikel.vk-preis
                        art-bestand.actval  = 0.
                END.                        
            END.                    
            
            CREATE stockoh-list. 
            IF NOT long-digit THEN 
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)")
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>>,>>>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
            END.                    
            ELSE
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)") 
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
            END.
                   
            t-val = t-val + art-bestand.actval. 
            tot-in = tot-in + art-bestand.in-val. 
            tot-out = tot-out + art-bestand.out-val. 
            tot-prev = tot-prev + art-bestand.prevval. 
            tot-value = tot-value + art-bestand.actval. 
            total-in = total-in + art-bestand.in-val. 
            total-out = total-out + art-bestand.out-val. 
            total-prev = total-prev + art-bestand.prevval. 
            total-value = total-value + art-bestand.actval. 
        END. 
        IF (NOT move-art AND NOT end-notzero) THEN 
        DO: 
            IF zwkum = 0 THEN 
            DO: 
                zwkum = art-bestand.zwkum. 
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                bezeich = l-untergrup.bezeich. 
            END. 
            IF zwkum NE art-bestand.zwkum THEN 
            DO: 
                CREATE stockoh-list.    
                /*M
                DO j = 1 TO 64: 
                    stockoh-list.s = stockoh-list.s + " ". 
                END. 
                */
                IF NOT long-digit THEN 
                DO:
                    ASSIGN 
                        stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                        stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9.99"). 
                END.                        
                ELSE 
                DO:
                    ASSIGN 
                        stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                        stockoh-list.actval  = STRING(t-val, "->>,>>>,>>>,>>9"). 
                END.
                    
    
                t-val = 0. 
                zwkum = art-bestand.zwkum. 
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                bezeich = l-untergrup.bezeich. 
            END. 
    
            FIND FIRST l-artikel WHERE l-artikel.artnr = art-bestand.artnr NO-LOCK.
            IF art-bestand.avrg-pr = 0 THEN 
            DO:
                IF art-bestand.actqty NE 0 THEN
                    art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                ELSE 
                DO:
                    ASSIGN  
                        art-bestand.avrg-pr = l-artikel.vk-preis
                        art-bestand.actval  = 0.
                END.                        
            END.                    
            
            CREATE stockoh-list. 
            IF NOT long-digit THEN 
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)")
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>>,>>>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
            END.                    
            ELSE
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(30)") 
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99")
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
            END.
                   
            t-val = t-val + art-bestand.actval. 
            tot-in = tot-in + art-bestand.in-val. 
            tot-out = tot-out + art-bestand.out-val. 
            tot-prev = tot-prev + art-bestand.prevval. 
            tot-value = tot-value + art-bestand.actval. 
            total-in = total-in + art-bestand.in-val. 
            total-out = total-out + art-bestand.out-val. 
            total-prev = total-prev + art-bestand.prevval. 
            total-value = total-value + art-bestand.actval. 
        END. 
    END. 
      
    IF bezeich NE "" THEN 
    DO: 
        CREATE stockoh-list. 
        IF NOT long-digit THEN 
        DO:
            ASSIGN 
                stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                        + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9.99"). 
        END.                
        ELSE
        DO:
            ASSIGN 
                stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                        + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                stockoh-list.actval  = STRING(t-val, "->>,>>>,>>>,>>9").
        END.
            
        /*FD Comment => Not used for Global OnHand
        /*Naufal - Add total value per store*/
        CREATE stockoh-list.
        IF NOT long-digit THEN
        DO:
            ASSIGN 
                stockoh-list.bezeich = "Ttl " + STRING(l-lager.bezeich, "x(25)") 
                stockoh-list.actval  = STRING(tot-value, "->,>>>,>>>,>>9.99").
        END.                
        ELSE
        DO:
            ASSIGN
                stockoh-list.bezeich = "Ttl " + STRING(l-lager.bezeich, "x(25)")
                stockoh-list.actval  = STRING(tot-value, "->>,>>>,>>>,>>9").
        END.                
        CREATE stockoh-list.
        /*end*/
        */
    END.
    

    CREATE stockoh-list.
    IF NOT long-digit THEN
    DO:
        ASSIGN
            stockoh-list.bezeich = "G R A N D  T O T A L"
            stockoh-list.actval  = STRING(total-value, "->,>>>,>>>,>>9.99").
    END.        
    ELSE
    DO:
        ASSIGN
            stockoh-list.bezeich = "G R A N D  T O T A L"
            stockoh-list.actval  = STRING(total-value, "->>,>>>,>>>,>>9").
    END.                
     
    FOR EACH art-bestand: 
      DELETE art-bestand. 
    END.
END PROCEDURE.
