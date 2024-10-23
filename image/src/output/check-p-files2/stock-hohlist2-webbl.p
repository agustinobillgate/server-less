
DEFINE TEMP-TABLE stockoh-list
    FIELD artnr    AS CHARACTER FORMAT "x(7)" 
    FIELD bezeich  AS CHARACTER FORMAT "x(50)" 
    FIELD prevqty  AS CHARACTER FORMAT "x(13)"
    FIELD prevval  AS CHARACTER FORMAT "x(14)" 
    FIELD incoming AS CHARACTER FORMAT "x(13)" 
    FIELD outgoing AS CHARACTER FORMAT "x(13)" 
    FIELD actqty   AS CHARACTER FORMAT "x(13)" 
    FIELD actval   AS CHARACTER FORMAT "x(14)" 
    FIELD avrg-pr  AS CHARACTER FORMAT "x(14)"
    FIELD incomingval AS CHARACTER FORMAT "x(15)" /*FDL*/
    FIELD outgoingval AS CHARACTER FORMAT "x(15)" /*FDL*/
    .  

DEFINE WORKFILE art-bestand 
    FIELD lager    AS INTEGER FORMAT ">>9" 
    FIELD artnr    AS INTEGER FORMAT ">>>>>>9" 
    FIELD zwkum    AS INTEGER 
    FIELD bezeich  AS CHARACTER FORMAT "x(50)" 
    FIELD incoming AS DECIMAL FORMAT "->,>>>,>>9.99"  
    FIELD in-val   AS DECIMAL FORMAT "->>,>>>,>>9.99" 
    FIELD out-val  AS DECIMAL FORMAT "->>,>>>,>>9.99" 
    FIELD outgoing AS DECIMAL FORMAT "->,>>>,>>9.99"  
    FIELD prevqty  AS DECIMAL FORMAT "->,>>>,>>9.99"  
    FIELD prevval  AS DECIMAL FORMAT "->>,>>>,>>9.99" 
    FIELD adjust   AS DECIMAL FORMAT "->>>,>>9.99"    
    FIELD actqty   AS DECIMAL FORMAT "->,>>>,>>9.99"  
    FIELD actval   AS DECIMAL FORMAT "->>,>>>,>>9.99" 
    FIELD avrg-pr  AS DECIMAL FORMAT "->>,>>>,>>9.99". 

DEFINE TEMP-TABLE t-vkpreis /*FD*/
    FIELD lager    AS INTEGER FORMAT ">>9" 
    FIELD artnr    AS INTEGER FORMAT ">>>>>>9" 
    FIELD zwkum    AS INTEGER 
    FIELD bezeich  AS CHARACTER FORMAT "x(50)"
    FIELD qty-end  AS DECIMAL 
    FIELD val-end  AS DECIMAL 
    FIELD vk-preis AS DECIMAL FORMAT "->>>,>>>,>>9.99999999"
.

DEFINE TEMP-TABLE tot-t-vkpreis
    FIELD lager    AS INTEGER FORMAT ">>9" 
    FIELD artnr    AS INTEGER FORMAT ">>>>>>9"
    FIELD tot-val  AS INTEGER
.

DEFINE INPUT PARAMETER from-lager   AS INTEGER.
DEFINE INPUT PARAMETER to-lager     AS INTEGER.
DEFINE INPUT PARAMETER from-art     AS INTEGER.
DEFINE INPUT PARAMETER to-art       AS INTEGER.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER move-art     AS LOGICAL.
DEFINE INPUT PARAMETER end-notzero  AS LOGICAL.
DEFINE INPUT PARAMETER global-oh    AS LOGICAL.
DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR stockoh-list.

DEFINE VARIABLE do-it        AS LOGICAL. 

DEFINE VARIABLE curr-art     AS INTEGER. 
DEFINE VARIABLE curr-lager   AS INTEGER. 
DEFINE VARIABLE out-bestand  AS DECIMAL. 

DEFINE VARIABLE zwkum AS INTEGER. 
DEFINE VARIABLE t-val AS DECIMAL. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE VARIABLE j AS INTEGER. 

DEFINE VARIABLE tot-prev            AS DECIMAL. 
DEFINE VARIABLE tot-value           AS DECIMAL. 
DEFINE VARIABLE tot-in              AS DECIMAL. 
DEFINE VARIABLE tot-out             AS DECIMAL. 
DEFINE VARIABLE total-in            AS DECIMAL. 
DEFINE VARIABLE total-out           AS DECIMAL. 
DEFINE VARIABLE total-prev          AS DECIMAL. 
DEFINE VARIABLE total-value         AS DECIMAL. 
DEFINE VARIABLE start-from-date     AS DATE.
DEFINE VARIABLE loop                AS INTEGER.
DEFINE VARIABLE loop-date           AS DATE.
DEFINE VARIABLE diff-month          AS INTEGER.

/***************************************************************************/
DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

start-from-date = DATE(MONTH(from-date), 1 , YEAR(from-date)).
RUN calc-month-diff (from-date, to-date, OUTPUT diff-month).

/*STATUS DEFAULT "Processing...". */

IF global-oh EQ ? THEN global-oh  = NO.
IF end-notzero EQ ? THEN end-notzero = NO.

IF NOT global-oh THEN RUN create-stock1.
ELSE RUN create-stock2.

/****************************************************************************/
PROCEDURE calc-month-diff:
    DEFINE INPUT PARAMETER from-date AS DATE.
    DEFINE INPUT PARAMETER to-date AS DATE.
    DEFINE OUTPUT PARAMETER diff-month AS INTEGER.

    DEFINE VARIABLE year-from-date AS INTEGER.
    DEFINE VARIABLE year-to-date AS INTEGER.
    DEFINE VARIABLE month-from-date AS INTEGER.
    DEFINE VARIABLE month-to-date AS INTEGER.
    DEFINE VARIABLE diff-year AS INTEGER.

    year-from-date = YEAR(from-date).
    year-to-date = YEAR(to-date).
    month-from-date = MONTH(from-date).
    month-to-date = MONTH(to-date).

    diff-year  = year-to-date - year-from-date.
    diff-month = (month-to-date + (12 * diff-year)) - month-from-date.

END PROCEDURE.

PROCEDURE create-stock1:

    FOR EACH t-vkpreis:
        DELETE t-vkpreis.
    END.

    /* FOR EACH l-besthis WHERE l-besthis.lager-nr = 0 AND l-besthis.anf-best-dat EQ from-date
    AND l-besthis.artnr GE from-art AND l-besthis.artnr LE to-art NO-LOCK,
    FIRST l-artikel WHERE l-artikel.artnr = l-besthis.artnr NO-LOCK 
    BY l-artikel.zwkum BY l-artikel.artnr:
    
        CREATE t-vkpreis.
        ASSIGN
            t-vkpreis.lager     = l-besthis.lager-nr
            t-vkpreis.artnr     = l-besthis.artnr
            t-vkpreis.zwkum     = l-artikel.zwkum
            t-vkpreis.bezeich   = l-artikel.bezeich   
            t-vkpreis.qty-end   = l-besthis.anz-anf-best + l-besthis.anz-eingang - l-besthis.anz-ausgang
            t-vkpreis.val-end   = l-besthis.val-anf-best + l-besthis.wert-eingang - l-besthis.wert-ausgang
        .

        IF t-vkpreis.val-end EQ 0 OR t-vkpreis.qty-end EQ 0 THEN 
            t-vkpreis.vk-preis = l-artikel.vk-preis.
        ELSE
            t-vkpreis.vk-preis = t-vkpreis.val-end / t-vkpreis.qty-end.
    END. */

    /*FD Sept 15, 2021 => 861F7E Dwi S get vk-preis don't from l-artikel, but calculate l-besthis*/
    FOR EACH l-besthis WHERE l-besthis.lager-nr = 0 
    AND l-besthis.anf-best-dat GE DATE(MONTH(from-date), 1 , YEAR(from-date))
    AND l-besthis.anf-best-dat LE DATE(MONTH(to-date), 1 , YEAR(to-date))
    AND l-besthis.artnr GE from-art AND l-besthis.artnr LE to-art NO-LOCK,
    FIRST l-artikel WHERE l-artikel.artnr = l-besthis.artnr NO-LOCK 
    BY l-artikel.zwkum BY l-artikel.artnr:

        FIND FIRST t-vkpreis WHERE t-vkpreis.artnr EQ l-besthis.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE t-vkpreis THEN
        DO:
            t-vkpreis.qty-end   = t-vkpreis.qty-end + (l-besthis.anz-anf-best + l-besthis.anz-eingang - l-besthis.anz-ausgang).
            t-vkpreis.val-end   = t-vkpreis.val-end + (l-besthis.val-anf-best + l-besthis.wert-eingang - l-besthis.wert-ausgang).

            IF t-vkpreis.val-end EQ 0 OR t-vkpreis.qty-end EQ 0 THEN 
                t-vkpreis.vk-preis = t-vkpreis.vk-preis + l-artikel.vk-preis.
            ELSE
                t-vkpreis.vk-preis = t-vkpreis.vk-preis + (t-vkpreis.val-end / (t-vkpreis.qty-end)).
        END.
        ELSE
        DO:
            CREATE t-vkpreis.
            ASSIGN
                t-vkpreis.lager     = l-besthis.lager-nr
                t-vkpreis.artnr     = l-besthis.artnr
                t-vkpreis.zwkum     = l-artikel.zwkum
                t-vkpreis.bezeich   = l-artikel.bezeich   
                t-vkpreis.qty-end   = l-besthis.anz-anf-best + l-besthis.anz-eingang - l-besthis.anz-ausgang
                t-vkpreis.val-end   = l-besthis.val-anf-best + l-besthis.wert-eingang - l-besthis.wert-ausgang
            .
    
            IF t-vkpreis.val-end EQ 0 OR t-vkpreis.qty-end EQ 0 THEN 
                t-vkpreis.vk-preis = l-artikel.vk-preis.
            ELSE
                t-vkpreis.vk-preis = t-vkpreis.val-end / (t-vkpreis.qty-end).
        END.
    END.
    /*End FD*/

    FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager AND l-lager.lager-nr LE to-lager NO-LOCK: 
        zwkum = 0. 
        t-val = 0. 
        FOR EACH l-besthis WHERE l-besthis.lager-nr = l-lager.lager-nr 
        AND l-besthis.anf-best-dat EQ start-from-date
        AND l-besthis.artnr GE from-art AND l-besthis.artnr LE to-art NO-LOCK, 
        FIRST t-vkpreis WHERE t-vkpreis.artnr = l-besthis.artnr NO-LOCK 
        BY t-vkpreis.zwkum BY t-vkpreis.artnr: 
            do-it = YES. 
            /*M
            IF from-grp > 0 THEN 
                IF l-artikel.zwkum LT from-grp OR l-artikel.zwkum GT to-grp THEN do-it = NO. 
            */
    
            IF do-it THEN 
            DO: 
                FIND FIRST art-bestand WHERE art-bestand.artnr EQ l-besthis.artnr AND art-bestand.lager EQ l-lager.lager-nr NO-ERROR. 
                IF NOT AVAILABLE art-bestand THEN 
                DO: 
                    CREATE art-bestand. 
                    art-bestand.bezeich = t-vkpreis.bezeich. 
                    art-bestand.zwkum = t-vkpreis.zwkum. 
                    art-bestand.artnr = l-besthis.artnr. 
                    art-bestand.lager = l-lager.lager-nr. 
    
                    /* INITIAL values */ 
                    art-bestand.prevqty  = l-besthis.anz-anf-best. 
                    art-bestand.prevval  = l-besthis.val-anf-best. 
                    art-bestand.actqty   = l-besthis.anz-anf-best. 
                    art-bestand.actval   = l-besthis.val-anf-best.
    
                    curr-art   = l-besthis.artnr. 
                    curr-lager = l-lager.lager-nr. 
                END. 
                out-bestand = 0.

                /* modify logic to count moving stock by period by Oscar (12 September 2024) - 9D6DDE */
    
                /* start of 9D6DDE */
                /* calculate the incoming- AND outgoing stocks within the given periods */ 
                FOR EACH l-ophis WHERE l-ophis.lager-nr = l-lager.lager-nr 
                AND l-ophis.artnr = l-besthis.artnr 
                AND (l-ophis.datum GE start-from-date AND l-ophis.datum LE to-date) 
                AND NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*" NO-LOCK BY l-ophis.datum:
                   IF l-ophis.op-art = 1 OR l-ophis.op-art = 2 THEN 
                   DO: 
                       art-bestand.incoming = art-bestand.incoming + l-ophis.anzahl. 
                       art-bestand.in-val = art-bestand.in-val + l-ophis.anzahl * (t-vkpreis.vk-preis / (diff-month + 1)). 

                       art-bestand.actqty  = art-bestand.actqty + l-ophis.anzahl.
                       /*art-bestand.actval  = art-bestand.actval  
                                            + l-ophis.anzahl * t-vkpreis.vk-preis.*/ /*FD Comment*/                  
                   END.
                   ELSE IF l-ophis.op-art = 3 OR l-ophis.op-art = 4 THEN 
                   DO: 
                       art-bestand.outgoing = art-bestand.outgoing + l-ophis.anzahl. 
                       art-bestand.out-val = art-bestand.out-val + l-ophis.anzahl * (t-vkpreis.vk-preis / (diff-month + 1)).

                       art-bestand.actqty  = art-bestand.actqty - l-ophis.anzahl.
                       /*art-bestand.actval  = art-bestand.actval 
                                            - l-ophis.anzahl * t-vkpreis.vk-preis.*/ /*FD Comment*/
                   END. 
                END. 

                
                FOR EACH l-ophis WHERE l-ophis.lager-nr = l-lager.lager-nr 
                AND l-ophis.artnr = l-besthis.artnr 
                AND (l-ophis.datum GE start-from-date AND l-ophis.datum LE from-date) 
                AND NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*" NO-LOCK BY l-ophis.datum:

                   IF l-ophis.op-art = 1 OR l-ophis.op-art = 2 THEN 
                   DO: 
                        /* ingoing */        
                        art-bestand.incoming = art-bestand.incoming - l-ophis.anzahl. 
                        art-bestand.in-val = art-bestand.in-val - l-ophis.anzahl * (t-vkpreis.vk-preis / (diff-month + 1)).

                        art-bestand.prevqty  = art-bestand.prevqty + l-ophis.anzahl.
                   END.
                   ELSE IF l-ophis.op-art = 3 OR l-ophis.op-art = 4 THEN 
                   DO: 
                        /* outgoing */
                        art-bestand.outgoing = art-bestand.outgoing - l-ophis.anzahl. 
                        art-bestand.out-val  = art-bestand.out-val - l-ophis.anzahl * (t-vkpreis.vk-preis / (diff-month + 1)).

                        art-bestand.prevqty  = art-bestand.prevqty - l-ophis.anzahl.
                   END. 
                END.

                art-bestand.prevval  = art-bestand.prevqty * (t-vkpreis.vk-preis / (diff-month + 1)).
                /* end of 9D6DDE */

                art-bestand.actval   = art-bestand.actqty * (t-vkpreis.vk-preis / (diff-month + 1)). /*FD*/
                
            END.
        END. 
    END. 
     
    FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager 
    AND l-lager.lager-nr LE to-lager NO-LOCK: 
        bezeich = "". 
        CREATE stockoh-list. 
        stockoh-list.bezeich = STRING(l-lager.lager-nr, "99") + " - " + STRING(l-lager.bezeich, "x(20)"). 
    
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
            
            IF (move-art AND end-notzero) 
            AND (art-bestand.incoming NE 0 OR art-bestand.outgoing NE 0
            OR art-bestand.actqty NE 0) THEN /*Moving True, Not Zero True*/
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
                            stockoh-list.actval  = STRING(t-val, "->>,>>>,>>9.99"). 
                    END.
                        
                    ELSE 
                    DO:
                        ASSIGN 
                            stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                            stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9").
                    END.
                         
                    CREATE stockoh-list.

                    t-val = 0. 
                    zwkum = art-bestand.zwkum. 
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                    bezeich = l-untergrup.bezeich. 
                END. 
                
                FIND FIRST t-vkpreis WHERE t-vkpreis.artnr = art-bestand.artnr NO-LOCK. 
                IF art-bestand.avrg-pr = 0 THEN 
                DO:
                    IF art-bestand.actqty NE 0 THEN
                        art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                    ELSE 
                    DO:
                        ASSIGN  
                            art-bestand.avrg-pr = (t-vkpreis.vk-preis / (diff-month + 1))
                            art-bestand.actval  = 0.
                    END.                     
                END.
                                
                CREATE stockoh-list. 
                IF NOT long-digit THEN 
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)")
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
                END.                
                ELSE 
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)") 
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, ">>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
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
            ELSE IF (move-art AND NOT end-notzero) 
            AND (art-bestand.incoming NE 0
            OR art-bestand.outgoing NE 0) THEN  /*Moving True, Not Zero False*/
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
                            stockoh-list.actval  = STRING(t-val, "->>,>>>,>>9.99"). 
                    END.
                        
                    ELSE 
                    DO:
                        ASSIGN 
                            stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                            stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9").
                    END.
                         
                    CREATE stockoh-list.
                
                    t-val = 0. 
                    zwkum = art-bestand.zwkum. 
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                    bezeich = l-untergrup.bezeich. 
                END. 
                
                FIND FIRST t-vkpreis WHERE t-vkpreis.artnr = art-bestand.artnr NO-LOCK. 
                IF art-bestand.avrg-pr = 0 THEN 
                DO:
                    IF art-bestand.actqty NE 0 THEN
                        art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                    ELSE 
                    DO:
                        ASSIGN  
                            art-bestand.avrg-pr = (t-vkpreis.vk-preis / (diff-month + 1))
                            art-bestand.actval  = 0.
                    END.                     
                END.
                                
                CREATE stockoh-list. 
                IF NOT long-digit THEN 
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)")
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
                END.                
                ELSE 
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)") 
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, ">>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
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
            ELSE IF (NOT move-art AND end-notzero) 
            AND (art-bestand.actqty NE 0) THEN /*Moving False, Not Zero True*/
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
                            stockoh-list.actval  = STRING(t-val, "->>,>>>,>>9.99"). 
                    END.
                        
                    ELSE 
                    DO:
                        ASSIGN 
                            stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                            stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9").
                    END.
                    
                    CREATE stockoh-list.     
                
                    t-val = 0. 
                    zwkum = art-bestand.zwkum. 
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                    bezeich = l-untergrup.bezeich. 
                END. 
                
                FIND FIRST t-vkpreis WHERE t-vkpreis.artnr = art-bestand.artnr NO-LOCK. 
                IF art-bestand.avrg-pr = 0 THEN 
                DO:
                    IF art-bestand.actqty NE 0 THEN
                        art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                    ELSE 
                    DO:
                        ASSIGN  
                            art-bestand.avrg-pr = (t-vkpreis.vk-preis / (diff-month + 1))
                            art-bestand.actval  = 0.
                    END.                     
                END.
                                
                CREATE stockoh-list. 
                IF NOT long-digit THEN 
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)")
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
                END.                
                ELSE 
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)") 
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, ">>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
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
            ELSE IF (NOT move-art AND NOT end-notzero) THEN /*Moving False, Not Zero False*/
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
                            stockoh-list.actval  = STRING(t-val, "->>,>>>,>>9.99"). 
                    END.
                        
                    ELSE 
                    DO:
                        ASSIGN 
                            stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                                + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                            stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9").
                    END.
                         
                    CREATE stockoh-list.
                
                    t-val = 0. 
                    zwkum = art-bestand.zwkum. 
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                    bezeich = l-untergrup.bezeich. 
                END. 
                
                FIND FIRST t-vkpreis WHERE t-vkpreis.artnr = art-bestand.artnr NO-LOCK. 
                IF art-bestand.avrg-pr = 0 THEN 
                DO:
                    IF art-bestand.actqty NE 0 THEN
                        art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                    ELSE 
                    DO:
                        ASSIGN  
                            art-bestand.avrg-pr = (t-vkpreis.vk-preis / (diff-month + 1))
                            art-bestand.actval  = 0.
                    END.                     
                END.
                                
                CREATE stockoh-list. 
                IF NOT long-digit THEN 
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)")
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
                END.                
                ELSE 
                DO:
                    ASSIGN 
                        stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                        stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)") 
                        stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                        stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                        stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                        stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                        stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                        /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                        stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                        stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                        stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, ">>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
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
                    stockoh-list.actval  = STRING(t-val, "->>,>>>,>>9.99"). 
            END.            
            ELSE 
            DO:
                ASSIGN 
                    stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                        + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                    stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9").
            END.          
                 
            CREATE stockoh-list. 
        END. 
    END.     
     
    FOR EACH art-bestand: 
      DELETE art-bestand. 
    END. 

END PROCEDURE.

PROCEDURE create-stock2:

    FOR EACH t-vkpreis:
        DELETE t-vkpreis.
    END.
    
    /*FD Sept 15, 2021 => 861F7E Dwi S get vk-preis don't from l-artikel, but calculate l-besthis*/
    /* FOR EACH l-besthis WHERE l-besthis.lager-nr = 0 AND l-besthis.anf-best-dat EQ from-date
    AND l-besthis.artnr GE from-art AND l-besthis.artnr LE to-art NO-LOCK,
    FIRST l-artikel WHERE l-artikel.artnr = l-besthis.artnr NO-LOCK 
    BY l-artikel.zwkum BY l-artikel.artnr:
    
        CREATE t-vkpreis.
        ASSIGN
            t-vkpreis.lager     = l-besthis.lager-nr
            t-vkpreis.artnr     = l-besthis.artnr
            t-vkpreis.zwkum     = l-artikel.zwkum
            t-vkpreis.bezeich   = l-artikel.bezeich   
            t-vkpreis.qty-end   = l-besthis.anz-anf-best + l-besthis.anz-eingang - l-besthis.anz-ausgang
            t-vkpreis.val-end   = l-besthis.val-anf-best + l-besthis.wert-eingang - l-besthis.wert-ausgang
        .

        IF t-vkpreis.val-end EQ 0 OR t-vkpreis.qty-end EQ 0 THEN 
            t-vkpreis.vk-preis = l-artikel.vk-preis.
        ELSE
            t-vkpreis.vk-preis = t-vkpreis.val-end / t-vkpreis.qty-end.
    END. */
    /*End FD*/

    FOR EACH l-besthis WHERE l-besthis.lager-nr = 0 
    AND l-besthis.anf-best-dat GE DATE(MONTH(from-date), 1 , YEAR(from-date))
    AND l-besthis.anf-best-dat LE DATE(MONTH(to-date), 1 , YEAR(to-date))
    AND l-besthis.artnr GE from-art AND l-besthis.artnr LE to-art NO-LOCK,
    FIRST l-artikel WHERE l-artikel.artnr = l-besthis.artnr NO-LOCK 
    BY l-artikel.zwkum BY l-artikel.artnr:

        FIND FIRST t-vkpreis WHERE t-vkpreis.artnr EQ l-besthis.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE t-vkpreis THEN
        DO:
            t-vkpreis.qty-end   = t-vkpreis.qty-end + (l-besthis.anz-anf-best + l-besthis.anz-eingang - l-besthis.anz-ausgang).
            t-vkpreis.val-end   = t-vkpreis.val-end + (l-besthis.val-anf-best + l-besthis.wert-eingang - l-besthis.wert-ausgang).

            IF t-vkpreis.val-end EQ 0 OR t-vkpreis.qty-end EQ 0 THEN 
                t-vkpreis.vk-preis = t-vkpreis.vk-preis + l-artikel.vk-preis.
            ELSE
                t-vkpreis.vk-preis = t-vkpreis.vk-preis + (t-vkpreis.val-end / (t-vkpreis.qty-end)).
        END.
        ELSE
        DO:
            CREATE t-vkpreis.
            ASSIGN
                t-vkpreis.lager     = l-besthis.lager-nr
                t-vkpreis.artnr     = l-besthis.artnr
                t-vkpreis.zwkum     = l-artikel.zwkum
                t-vkpreis.bezeich   = l-artikel.bezeich   
                t-vkpreis.qty-end   = l-besthis.anz-anf-best + l-besthis.anz-eingang - l-besthis.anz-ausgang
                t-vkpreis.val-end   = l-besthis.val-anf-best + l-besthis.wert-eingang - l-besthis.wert-ausgang
            .
    
            IF t-vkpreis.val-end EQ 0 OR t-vkpreis.qty-end EQ 0 THEN 
                t-vkpreis.vk-preis = l-artikel.vk-preis.
            ELSE
                t-vkpreis.vk-preis = t-vkpreis.val-end / (t-vkpreis.qty-end).
        END.
    END.
    /*End FD*/
    
    /*New Metode*/
    FOR EACH l-besthis WHERE l-besthis.anf-best-dat EQ from-date AND l-besthis.lager-nr EQ 0
    AND l-besthis.artnr GE from-art AND l-besthis.artnr LE to-art NO-LOCK, 
    FIRST t-vkpreis WHERE t-vkpreis.artnr = l-besthis.artnr NO-LOCK 
    BY t-vkpreis.zwkum BY t-vkpreis.artnr: 
        do-it = YES. 
        /*M
        IF from-grp > 0 THEN 
            IF l-artikel.zwkum LT from-grp OR l-artikel.zwkum GT to-grp THEN do-it = NO. 
        */
    
        IF do-it THEN 
        DO:             
            CREATE art-bestand. 
            art-bestand.bezeich = t-vkpreis.bezeich. 
            art-bestand.zwkum = t-vkpreis.zwkum. 
            art-bestand.artnr = l-besthis.artnr. 
            art-bestand.lager = l-besthis.lager-nr. 

            /* INITIAL values */ 
            art-bestand.prevqty = l-besthis.anz-anf-best. 
            art-bestand.prevval = l-besthis.val-anf-best. 
            art-bestand.actqty  = l-besthis.anz-anf-best. 
            art-bestand.actval  = l-besthis.val-anf-best.              
        END.         
    END.

    /* New Metode calculate the incoming- AND outgoing stocks within the given periods */ 
    FOR EACH art-bestand NO-LOCK,
    FIRST t-vkpreis WHERE t-vkpreis.artnr = art-bestand.artnr NO-LOCK 
    BY art-bestand.zwkum BY art-bestand.artnr:

        /* FOR EACH l-ophis WHERE l-ophis.artnr EQ art-bestand.artnr 
        AND (l-ophis.datum GE from-date AND l-ophis.datum LE to-date) 
        AND NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*"  NO-LOCK BY l-ophis.datum: 
             
            IF l-ophis.op-art = 1 OR l-ophis.op-art = 2 THEN 
            DO: 
                art-bestand.incoming = art-bestand.incoming + l-ophis.anzahl. 
                art-bestand.in-val = art-bestand.in-val 
                                     + l-ophis.anzahl * t-vkpreis.vk-preis. 
                art-bestand.actqty  = art-bestand.actqty + l-ophis.anzahl. 
                /*art-bestand.actval  = art-bestand.actval  
                                     + l-ophis.anzahl * t-vkpreis.vk-preis.*/ /*FD Comment*/                  
            END.                                                            
            ELSE IF l-ophis.op-art = 3 OR l-ophis.op-art = 4 THEN 
            DO: 
                art-bestand.outgoing = art-bestand.outgoing + l-ophis.anzahl. 
                art-bestand.out-val = art-bestand.out-val 
                                     + l-ophis.anzahl * t-vkpreis.vk-preis. 
                art-bestand.actqty  = art-bestand.actqty - l-ophis.anzahl. 
                /*art-bestand.actval  = art-bestand.actval 
                                     - l-ophis.anzahl * t-vkpreis.vk-preis.*/ /*FD Comment*/
            END. 
        END. 

        art-bestand.actval = art-bestand.actqty * t-vkpreis.vk-preis. /*FD*/ */ 

        /* modify logic to count moving stock by period by Oscar (12 September 2024) - 9D6DDE */
    
        /* start of 9D6DDE */
        /* calculate the incoming- AND outgoing stocks within the given periods */ 

        FOR EACH l-ophis WHERE l-ophis.artnr EQ art-bestand.artnr 
        AND (l-ophis.datum GE start-from-date AND l-ophis.datum LE to-date) 
        AND NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*"  NO-LOCK BY l-ophis.datum: 
            IF l-ophis.op-art = 1 OR l-ophis.op-art = 2 THEN 
            DO: 
                art-bestand.incoming = art-bestand.incoming + l-ophis.anzahl. 
                art-bestand.in-val = art-bestand.in-val + l-ophis.anzahl * (t-vkpreis.vk-preis / (diff-month + 1)). 

                art-bestand.actqty  = art-bestand.actqty + l-ophis.anzahl.
                /*art-bestand.actval  = art-bestand.actval  
                                    + l-ophis.anzahl * t-vkpreis.vk-preis.*/ /*FD Comment*/                  
            END.
            ELSE IF l-ophis.op-art = 3 OR l-ophis.op-art = 4 THEN 
            DO: 
                art-bestand.outgoing = art-bestand.outgoing + l-ophis.anzahl. 
                art-bestand.out-val = art-bestand.out-val + l-ophis.anzahl * (t-vkpreis.vk-preis / (diff-month + 1)).

                art-bestand.actqty  = art-bestand.actqty - l-ophis.anzahl.
                /*art-bestand.actval  = art-bestand.actval 
                                    - l-ophis.anzahl * t-vkpreis.vk-preis.*/ /*FD Comment*/
            END. 
        END. 

        
        FOR EACH l-ophis WHERE l-ophis.artnr EQ art-bestand.artnr 
        AND (l-ophis.datum GE start-from-date AND l-ophis.datum LE from-date) 
        AND NOT vhp.l-ophis.fibukonto MATCHES "*;CANCELLED*"  NO-LOCK BY l-ophis.datum:

            IF l-ophis.op-art = 1 OR l-ophis.op-art = 2 THEN 
            DO: 
                /* ingoing */        
                art-bestand.incoming = art-bestand.incoming - l-ophis.anzahl. 
                art-bestand.in-val = art-bestand.in-val - l-ophis.anzahl * (t-vkpreis.vk-preis / (diff-month + 1)).

                art-bestand.prevqty  = art-bestand.prevqty + l-ophis.anzahl.
            END.
            ELSE IF l-ophis.op-art = 3 OR l-ophis.op-art = 4 THEN 
            DO: 
                /* outgoing */
                art-bestand.outgoing = art-bestand.outgoing - l-ophis.anzahl. 
                art-bestand.out-val  = art-bestand.out-val - l-ophis.anzahl * (t-vkpreis.vk-preis / (diff-month + 1)).

                art-bestand.prevqty  = art-bestand.prevqty - l-ophis.anzahl.
            END. 
        END.

        art-bestand.prevval  = art-bestand.prevqty * (t-vkpreis.vk-preis / (diff-month + 1)).
        /* end of 9D6DDE */

        art-bestand.actval   = art-bestand.actqty * (t-vkpreis.vk-preis / (diff-month + 1)). /*FD*/
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
        
        IF (move-art AND end-notzero) 
        AND (art-bestand.incoming NE 0 
        OR art-bestand.outgoing NE 0
        OR art-bestand.actqty NE 0) THEN /*Moving True, Not Zero True*/
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
                        stockoh-list.actval  = STRING(t-val, "->>,>>>,>>9.99"). 
                END.
                    
                ELSE 
                DO:
                    ASSIGN 
                        stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                            + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                        stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9").
                END.
                     
                CREATE stockoh-list.
            
                t-val = 0. 
                zwkum = art-bestand.zwkum. 
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                bezeich = l-untergrup.bezeich. 
            END. 
            
            FIND FIRST t-vkpreis WHERE t-vkpreis.artnr = art-bestand.artnr NO-LOCK. 
            IF art-bestand.avrg-pr = 0 THEN 
            DO:
                IF art-bestand.actqty NE 0 THEN
                    art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                ELSE 
                DO:
                    ASSIGN  
                        art-bestand.avrg-pr = (t-vkpreis.vk-preis / (diff-month + 1))
                        art-bestand.actval  = 0.
                END.                     
            END.
                            
            CREATE stockoh-list. 
            IF NOT long-digit THEN 
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)")
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
            END.                
            ELSE 
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)") 
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, ">>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
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
            (art-bestand.incoming NE 0 OR art-bestand.outgoing NE 0) THEN  /*Moving True, Not Zero False*/
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
                        stockoh-list.actval  = STRING(t-val, "->>,>>>,>>9.99"). 
                END.
                    
                ELSE 
                DO:
                    ASSIGN 
                        stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                            + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                        stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9").
                END.
                     
                CREATE stockoh-list.
            
                t-val = 0. 
                zwkum = art-bestand.zwkum. 
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                bezeich = l-untergrup.bezeich. 
            END. 
            
            FIND FIRST t-vkpreis WHERE t-vkpreis.artnr = art-bestand.artnr NO-LOCK. 
            IF art-bestand.avrg-pr = 0 THEN 
            DO:
                IF art-bestand.actqty NE 0 THEN
                    art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                ELSE 
                DO:
                    ASSIGN  
                        art-bestand.avrg-pr = (t-vkpreis.vk-preis / (diff-month + 1))
                        art-bestand.actval  = 0.
                END.                     
            END.
                            
            CREATE stockoh-list. 
            IF NOT long-digit THEN 
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)")
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
            END.                
            ELSE 
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)") 
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, ">>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
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
        ELSE IF (NOT move-art AND end-notzero) AND (art-bestand.actqty NE 0) THEN /*Moving False, Not Zero True*/
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
                        stockoh-list.actval  = STRING(t-val, "->>,>>>,>>9.99"). 
                END.
                    
                ELSE 
                DO:
                    ASSIGN 
                        stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                            + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                        stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9").
                END.
                     
                CREATE stockoh-list.
            
                t-val = 0. 
                zwkum = art-bestand.zwkum. 
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                bezeich = l-untergrup.bezeich. 
            END. 
            
            FIND FIRST t-vkpreis WHERE t-vkpreis.artnr = art-bestand.artnr NO-LOCK. 
            IF art-bestand.avrg-pr = 0 THEN 
            DO:
                IF art-bestand.actqty NE 0 THEN
                    art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                ELSE 
                DO:
                    ASSIGN  
                        art-bestand.avrg-pr = (t-vkpreis.vk-preis / (diff-month + 1))
                        art-bestand.actval  = 0.
                END.                     
            END.
                            
            CREATE stockoh-list. 
            IF NOT long-digit THEN 
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)")
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
            END.                
            ELSE 
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)") 
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, ">>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
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
        ELSE IF (NOT move-art AND NOT end-notzero) THEN /*Moving False, Not Zero False*/
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
                        stockoh-list.actval  = STRING(t-val, "->>,>>>,>>9.99"). 
                END.
                    
                ELSE 
                DO:
                    ASSIGN 
                        stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                            + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                        stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9").
                END.
                     
                CREATE stockoh-list.
            
                t-val = 0. 
                zwkum = art-bestand.zwkum. 
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = zwkum NO-LOCK. 
                bezeich = l-untergrup.bezeich. 
            END. 
            
            FIND FIRST t-vkpreis WHERE t-vkpreis.artnr = art-bestand.artnr NO-LOCK. 
            IF art-bestand.avrg-pr = 0 THEN 
            DO:
                IF art-bestand.actqty NE 0 THEN
                    art-bestand.avrg-pr = art-bestand.actval / art-bestand.actqty.
                ELSE 
                DO:
                    ASSIGN  
                        art-bestand.avrg-pr = (t-vkpreis.vk-preis / (diff-month + 1))
                        art-bestand.actval  = 0.
                END.                     
            END.
                            
            CREATE stockoh-list. 
            IF NOT long-digit THEN 
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999")
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)")
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99") 
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->>,>>>,>>9.99") /*M STRING(art-bestand.prevval, "->>>,>>>,>>9.99") */ /* add 1 */ 
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>>,>>9.99")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->>,>>>,>>9.99") /*M STRING(art-bestand.actval, "->>>,>>>,>>9.99") */ /* add 1 */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, "->>,>>>,>>9.99") /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>9.99") */ /* add 2 */. 
            END.                
            ELSE 
            DO:
                ASSIGN 
                    stockoh-list.artnr    = STRING(art-bestand.artnr, "9999999") 
                    stockoh-list.bezeich  = STRING(art-bestand.bezeich, "x(50)") 
                    stockoh-list.prevqty  = STRING(art-bestand.prevqty, "->,>>>,>>9.99")
                    stockoh-list.prevval  = STRING(art-bestand.prevval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.prevval, "->>,>>>,>>>,>>9") */
                    stockoh-list.incoming = STRING(art-bestand.incoming, "->,>>>,>>9.99") 
                    stockoh-list.outgoing = STRING(art-bestand.outgoing, "->,>>>,>>9.99")
                    stockoh-list.outgoingval = STRING(art-bestand.out-val, "->>>,>>>,>>9.99") /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    stockoh-list.incomingval = STRING(art-bestand.in-val, "->>>,>>>,>>9.99")  /*FDL Dec 30, 2022 _2bl => ticket 96F3D5*/
                    /* stockoh-list.adjust   = STRING(art-bestand.adjust, "->>,>>>,>>9")  */
                    stockoh-list.actqty   = STRING(art-bestand.actqty, "->,>>>,>>9.99") 
                    stockoh-list.actval   = STRING(art-bestand.actval, "->,>>>,>>>,>>9") /*M STRING(art-bestand.actval, "->>,>>>,>>>,>>9") */
                    stockoh-list.avrg-pr  = STRING(art-bestand.avrg-pr, ">>,>>>,>>>,>>9"). /*M STRING(art-bestand.avrg-pr, ">>>,>>>,>>>,>>9"). */
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
                stockoh-list.actval  = STRING(t-val, "->>,>>>,>>9.99"). 
        END.            
        ELSE 
        DO:
            ASSIGN 
                stockoh-list.bezeich = "Ttl " + STRING(SUBSTR(bezeich,1,9), "x(9)") 
                                    + STRING(SUBSTR(bezeich, 10, 13), "x(13)") 
                stockoh-list.actval  = STRING(t-val, "->,>>>,>>>,>>9").
        END.
             
        CREATE stockoh-list. 
    END.  
    
    FOR EACH art-bestand: 
      DELETE art-bestand. 
    END. 

END PROCEDURE.

