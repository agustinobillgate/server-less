
 DEFINE TEMP-TABLE cust-list
    FIELD gastnr            LIKE guest.gastnr
    FIELD cust-name         AS CHAR     
    FIELD gesamtumsatz      LIKE guest.gesamtumsatz 
    FIELD logiernachte      LIKE guest.logiernachte 
    FIELD argtumsatz        LIKE guest.argtumsatz 
    FIELD f-b-umsatz        LIKE guest.f-b-umsatz 
    FIELD sonst-umsatz      LIKE guest.sonst-umsatz 
    FIELD wohnort           LIKE guest.wohnort 
    FIELD plz               LIKE guest.plz 
    FIELD land              LIKE guest.land
    FIELD sales-id          LIKE guest.phonetik3
    FIELD ba-umsatz         AS DECIMAL
    FIELD ly-rev            AS DECIMAL
    FIELD region            AS CHAR
    FIELD region1           AS CHAR
    FIELD stayno            AS INT
    FIELD resnr             AS CHAR
    FIELD counter           AS INT
    FIELD counterall        AS INT
    FIELD resno             AS INTEGER
    FIELD reslinnr          AS INTEGER
    FIELD curr-pos          AS INTEGER.

 DEFINE TEMP-TABLE cust-list-detail
    FIELD gastnr            LIKE guest.gastnr
    FIELD cust-name         AS CHAR     
    FIELD gesamtumsatz      AS CHAR
    FIELD logiernachte      AS CHAR  
    FIELD argtumsatz        AS CHAR 
    FIELD f-b-umsatz        AS CHAR 
    FIELD sonst-umsatz      AS CHAR 
    FIELD wohnort           LIKE guest.wohnort 
    FIELD plz               LIKE guest.plz 
    FIELD land              LIKE guest.land
    FIELD sales-id          LIKE guest.phonetik3
    FIELD ba-umsatz         AS CHAR 
    FIELD ly-rev            AS CHAR 
    FIELD region            AS CHAR
    FIELD region1           AS CHAR
    FIELD stayno            AS CHAR 
    FIELD resnr             AS CHAR
    FIELD counter           AS INT
    FIELD counterall        AS INT
    FIELD resno             AS INTEGER
    FIELD reslinnr          AS INTEGER
    FIELD curr-pos          AS INTEGER.

DEFINE TEMP-TABLE cust-list2 LIKE cust-list.

DEFINE TEMP-TABLE t-waehrung LIKE waehrung.

/*MT
DEFINE TEMP-TABLE t-guest LIKE guest
    FIELD cust-name     AS CHARACTER    FORMAT "x(34)".
*/    

DEFINE INPUT PARAMETER cardtype             AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER sort-type            AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER curr-sort1           AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER fdate                AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER tdate                AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER check-ftd            AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER currency             AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER excl-other           AS LOGICAL NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER curr-sort2    AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR cust-list.


DEFINE BUFFER t-genstat FOR genstat.

DEFINE VARIABLE bfast-art   AS INTEGER  NO-UNDO. 
DEFINE VARIABLE lunch-art   AS INTEGER  NO-UNDO. 
DEFINE VARIABLE dinner-art  AS INTEGER  NO-UNDO. 
DEFINE VARIABLE lundin-art  AS INTEGER  NO-UNDO. 

DEFINE VAR service          AS DECIMAL INITIAL 0.
DEFINE VAR vat              AS DECIMAL INITIAL 0.


DEFINE VARIABLE datum AS DATE.
DEFINE VARIABLE end-date AS DATE.


DEFINE VARIABLE net-lodg    AS DECIMAL.
DEFINE VARIABLE Fnet-lodg   AS DECIMAL.

DEFINE VARIABLE tot-breakfast    AS DECIMAL.
DEFINE VARIABLE tot-Lunch        AS DECIMAL.
DEFINE VARIABLE tot-dinner       AS DECIMAL.
DEFINE VARIABLE tot-Other        AS DECIMAL.
DEFINE VARIABLE tot-rmrev        AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-vat          AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-service      AS DECIMAL INITIAL 0.
DEFINE VARIABLE curr-i           AS INT.
DEFINE VARIABLE i                AS INT.
DEFINE VARIABLE found            AS LOGICAL INIT NO.
DEFINE VARIABLE ly-fdate         AS DATE.
DEFINE VARIABLE ly-tdate         AS DATE.
DEFINE VARIABLE ci-date          AS DATE.
DEFINE VARIABLE pos              AS INTEGER INIT 0.
DEFINE VARIABLE curr-gastnr      AS INTEGER.
DEFINE VARIABLE curr-resnr       AS INTEGER.
DEFINE VARIABLE curr-reslinnr    AS INTEGER.

DEFINE VARIABLE t-logiernachte  AS DECIMAL.
DEFINE VARIABLE t-argtumsatz    AS DECIMAL.
DEFINE VARIABLE t-fb-umsatz     AS DECIMAL.
DEFINE VARIABLE t-sonst-umsatz  AS DECIMAL.
DEFINE VARIABLE t-ba-umsatz     AS DECIMAL.
DEFINE VARIABLE t-gesamtumsatz  AS DECIMAL.


DEFINE VARIABLE tot-logiernachte  AS DECIMAL.
DEFINE VARIABLE tot-argtumsatz    AS DECIMAL.
DEFINE VARIABLE tot-fb-umsatz     AS DECIMAL.
DEFINE VARIABLE tot-sonst-umsatz  AS DECIMAL.
DEFINE VARIABLE tot-ba-umsatz     AS DECIMAL.
DEFINE VARIABLE tot-gesamtumsatz  AS DECIMAL.
DEFINE VARIABLE tot-stayno        AS DECIMAL.

DEFINE BUFFER blist FOR cust-list-detail.
DEFINE BUFFER glist FOR guest.
DEFINE BUFFER clist FOR cust-list-detail.

DEFINE VARIABLE loopj    AS INTEGER NO-UNDO.
DEFINE VARIABLE found-it AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE exratenr AS INTEGER NO-UNDO.
DEFINE VARIABLE exrate   AS DECIMAL NO-UNDO.

FIND FIRST htparam WHERE paramnr = 125 NO-LOCK. 
bfast-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */ 
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.

IF currency NE "" THEN DO:
    FIND FIRST waehrung WHERE waehrung.wabkurz = currency NO-LOCK NO-ERROR.
    IF AVAILABLE waehrung THEN 
        ASSIGN 
            exratenr = waehrung.waehrungsnr
            exrate   = waehrung.ankauf.
END.

FOR EACH cust-list:
    DELETE cust-list.
END.

IF cardtype = 3 THEN DO:
    IF NOT check-ftd THEN
    DO: 
        DEFINE VARIABLE curr-resnr2   AS INTEGER NO-UNDO.
        DEFINE VARIABLE curr-reslinnr2 AS INTEGER NO-UNDO.

        FOR EACH genstat WHERE /*genstat.resstatus NE 13
            AND*/ genstat.segmentcode NE 0 
            AND genstat.nationnr NE 0
            AND genstat.zinr NE ""
            AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */ ,
            FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK BY guest.gesamtumsatz descending
            BY guest.logiernachte descending BY guest.name:
    
            FIND FIRST cust-list WHERE cust-list.gastnr = guest.gastnr NO-ERROR.
            IF NOT AVAILABLE cust-list THEN
            DO:
                CREATE cust-list.
                ASSIGN
                  cust-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                       + guest.anredefirm)
                  cust-list.gastnr    = guest.gastnr
                  cust-list.wohnort   = guest.wohnort 
                  cust-list.plz       = guest.plz 
                  cust-list.land      = guest.land
                  cust-list.sales-id  = guest.phonetik3 /*MT 22/05/12*/.
    
                FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                        cust-list.region = queasy.char1.
                END.
                ELSE cust-list.region = "UNKOWN".
            END.
            
            FIND FIRST artikel WHERE artikel.zwkum = bfast-art NO-LOCK NO-ERROR.
            IF AVAILABLE artikel THEN
                 RUN calc-servvat.p(artikel.departement, artikel.artnr, genstat.datum, 
                       artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).

            IF currency NE " " THEN DO:
                FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                IF AVAILABLE exrate THEN 
                    ASSIGN
                        cust-list.f-b-umsatz   = cust-list.f-b-umsatz + ((genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]) / exrate.betrag)
                        cust-list.sonst-umsatz = cust-list.sonst-umsatz + (genstat.res-deci[5] / exrate.betrag)
                        cust-list.argtumsatz   = cust-list.argtumsatz + (genstat.logis / exrate.betrag)
                        cust-list.gesamtumsatz = cust-list.gesamtumsatz + ((genstat.logis + genstat.res-deci[2] 
                                                 + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]) / exrate.betrag)
                        cust-list.logiernachte = cust-list.logiernachte + 1.

            END.
            ELSE DO:
                ASSIGN
                    cust-list.f-b-umsatz   = cust-list.f-b-umsatz + genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]
                    cust-list.sonst-umsatz = cust-list.sonst-umsatz + genstat.res-deci[5] 
                    cust-list.argtumsatz   = cust-list.argtumsatz + genstat.logis
                    cust-list.gesamtumsatz = cust-list.gesamtumsatz + genstat.logis + genstat.res-deci[2] 
                                             + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]
                    cust-list.logiernachte = cust-list.logiernachte + 1.
            END.
            
            IF excl-other = NO THEN DO:
                /*Revenue from other*/
                IF curr-resnr2 NE genstat.resnr OR curr-reslinnr2 NE genstat.res-int[1] THEN DO:
                    ASSIGN
                        curr-resnr2 = genstat.resnr 
                        curr-reslinnr2 = genstat.res-int[1].
        
                    /*FIND FIRST bill WHERE bill.resnr = genstat.resnr
                        AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK NO-ERROR.*/
                    FOR EACH bill WHERE bill.resnr = genstat.resnr
                        AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK:
                        FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                            AND bill-line.bill-datum = genstat.datum NO-LOCK,
                            FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                                AND artikel.departement = bill-line.departement 
                                AND artikel.artart = 0 NO-LOCK :
                            IF currency NE "" THEN DO:
                                FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                                IF AVAILABLE exrate THEN 
                                    ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + (bill-line.betrag / exrate.betrag)
                                           cust-list.gesamtumsatz = cust-list.gesamtumsatz + (bill-line.betrag / exrate.betrag).
                            END.
                            ELSE ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + bill-line.betrag
                                       cust-list.gesamtumsatz = cust-list.gesamtumsatz + bill-line.betrag.
                        END.
                    END.
                END.
            END.
            
            /*
            IF AVAILABLE bill THEN DO:
                FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                    AND bill-line.bill-datum = genstat.datum NO-LOCK,
                    FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                        AND artikel.departement = bill-line.departement 
                        AND artikel.artart = 0 NO-LOCK :
                    IF currency NE "" THEN DO:
                        FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                        IF AVAILABLE exrate THEN 
                            ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + (bill-line.betrag / exrate.betrag)
                                   cust-list.gesamtumsatz = cust-list.gesamtumsatz + (bill-line.betrag / exrate.betrag).
                    END.
                    ELSE ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + bill-line.betrag
                               cust-list.gesamtumsatz = cust-list.gesamtumsatz + bill-line.betrag.
                END.
            END.*/        
        END.
        
        IF excl-other = NO THEN DO:
            /*Revenue from outlet*/
            FOR EACH guest-queasy WHERE guest-queasy.KEY = "gast-info"
                AND guest-queasy.date1 GE fdate
                AND guest-queasy.date1 LE tdate NO-LOCK :
          
                FIND FIRST genstat WHERE genstat.resnr = guest-queasy.number2 
                    AND genstat.res-int[1] = guest-queasy.number3 
                    AND genstat.datum = guest-queasy.date1
                    AND genstat.res-logic[2] EQ YES NO-LOCK NO-ERROR.
                IF AVAILABLE genstat THEN DO:
                    FIND FIRST cust-list WHERE cust-list.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
                    IF AVAILABLE cust-list THEN DO:
                        DO loopj = 1 TO NUM-ENTRIES(cust-list.resnr, ";"):
                            IF ENTRY(loopj, cust-list.resnr, ";") = STRING(genstat.resnr) THEN DO:
                                ASSIGN found-it = YES.
                                LEAVE.
                            END.
                            ELSE found-it = NO.
                        END.
                        IF found-it = YES THEN DO:
                            IF currency NE " " THEN DO:
                                FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                                IF AVAILABLE exrate THEN 
                                    ASSIGN
                                        cust-list.f-b-umsatz   = cust-list.f-b-umsatz + ((guest-queasy.deci1 + guest-queasy.deci2) / exrate.betrag)
                                        cust-list.sonst-umsatz = cust-list.sonst-umsatz + (guest-queasy.deci3 / exrate.betrag)
                                        cust-list.gesamtumsatz = cust-list.gesamtumsatz + ((guest-queasy.deci1 + guest-queasy.deci2 + guest-queasy.deci3) / exrate.betrag).   
                            END.
                            ELSE 
                                ASSIGN
                                    cust-list.f-b-umsatz   = cust-list.f-b-umsatz + guest-queasy.deci1 + guest-queasy.deci2
                                    cust-list.sonst-umsatz = cust-list.sonst-umsatz + guest-queasy.deci3
                                    cust-list.gesamtumsatz = cust-list.gesamtumsatz + guest-queasy.deci1 + guest-queasy.deci2 + guest-queasy.deci3.   
                        END.
                                        
                    END.           
                END.
             END.
        END.
        
        FOR EACH t-genstat WHERE t-genstat.datum GE fdate AND t-genstat.datum LE tdate
              AND t-genstat.res-deci[7] NE 0,
              FIRST guest WHERE guest.gastnr = t-genstat.gastnr NO-LOCK BY guest.gesamtumsatz descending
              BY guest.logiernachte descending BY guest.name :
        
              FIND FIRST cust-list WHERE cust-list.gastnr = t-genstat.gastnr NO-LOCK NO-ERROR.
              IF AVAILABLE cust-list THEN DO:
                  IF currency NE "" THEN DO:
                      FIND FIRST exrate WHERE exrate.datum = t-genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                      IF AVAILABLE exrate THEN 
                            ASSIGN                  
                                cust-list.ba-umsatz = t-genstat.res-deci[7] / exrate.betrag
                                cust-list.gesamtumsatz = cust-list.gesamtumsatz + (t-genstat.res-deci[7] / exrate.betrag).
                  END.
                  ELSE
                    ASSIGN cust-list.ba-umsatz = cust-list.ba-umsatz + t-genstat.res-deci[7]
                           cust-list.gesamtumsatz = cust-list.gesamtumsatz + t-genstat.res-deci[7].
              END.
              ELSE DO:
                  CREATE cust-list.
                  ASSIGN
                    cust-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                         + guest.anredefirm) 
                    cust-list.gastnr    = guest.gastnr
                    cust-list.wohnort   = guest.wohnort 
                    cust-list.plz       = guest.plz 
                    cust-list.land      = guest.land
                    cust-list.sales-id  = guest.phonetik3 /*MT 22/05/12*/.
                   
                  IF currency NE " " THEN DO:
                        FIND FIRST exrate WHERE exrate.datum = t-genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                        IF AVAILABLE exrate THEN 
                            ASSIGN                  
                                cust-list.ba-umsatz = t-genstat.res-deci[7] / exrate.betrag
                                cust-list.gesamtumsatz = cust-list.gesamtumsatz + (t-genstat.res-deci[7] / exrate.betrag).
                  END.
                  ELSE 
                      ASSIGN                  
                        cust-list.ba-umsatz = t-genstat.res-deci[7]
                        cust-list.gesamtumsatz = cust-list.gesamtumsatz + t-genstat.res-deci[7].

                  FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
                  IF AVAILABLE nation THEN
                  DO:
                    FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                      cust-list.region = queasy.char1.
                  END.
                  ELSE cust-list.region = "UNKNOWN".
              END.
        END.
    END.
    ELSE RUN cr-ftd-all. 
    
    IF tdate NE ? AND tdate GE ci-date AND check-ftd THEN
        RUN create-forecast-all.
END.
ELSE DO:
    IF NOT check-ftd THEN
    DO:
        DEFINE VARIABLE curr-resnr1   AS INTEGER NO-UNDO.
        DEFINE VARIABLE curr-reslinnr1 AS INTEGER NO-UNDO.

        FOR EACH genstat WHERE /*genstat.resstatus NE 13
            AND*/ genstat.segmentcode NE 0 
            AND genstat.nationnr NE 0
            AND genstat.zinr NE ""
            AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */ ,
            FIRST guest WHERE guest.gastnr = genstat.gastnr
            AND guest.karteityp = cardtype NO-LOCK BY guest.gesamtumsatz descending
            BY guest.logiernachte descending BY guest.name:
    
            FIND FIRST cust-list WHERE cust-list.gastnr = guest.gastnr NO-ERROR.
            IF NOT AVAILABLE cust-list THEN
            DO:
                CREATE cust-list.
                ASSIGN
                  cust-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                       + guest.anredefirm)
                  cust-list.gastnr    = guest.gastnr
                  cust-list.wohnort   = guest.wohnort 
                  cust-list.plz       = guest.plz 
                  cust-list.land      = guest.land
                  cust-list.sales-id  = guest.phonetik3 /*MT 22/05/12*/.
    
                FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN cust-list.region = queasy.char1.
                END.
                ELSE cust-list.region = "UNKOWN".
            END.
            
            FIND FIRST artikel WHERE artikel.zwkum = bfast-art NO-LOCK NO-ERROR.
            IF AVAILABLE artikel THEN
                 RUN calc-servvat.p(artikel.departement, artikel.artnr, genstat.datum, 
                       artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).

            IF currency NE " " THEN DO:
                FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                IF AVAILABLE exrate THEN 
                    ASSIGN
                        cust-list.f-b-umsatz   = cust-list.f-b-umsatz + ((genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]) / exrate.betrag)
                        cust-list.sonst-umsatz = cust-list.sonst-umsatz + (genstat.res-deci[5] / exrate.betrag)
                        cust-list.argtumsatz   = cust-list.argtumsatz + (genstat.logis / exrate.betrag)
                        cust-list.gesamtumsatz = cust-list.gesamtumsatz + ((genstat.logis + genstat.res-deci[2] 
                                                 + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]) / exrate.betrag)
                        cust-list.logiernachte = cust-list.logiernachte + 1.
            END.
            ELSE 
                ASSIGN
                    cust-list.f-b-umsatz   = cust-list.f-b-umsatz + genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]
                    cust-list.sonst-umsatz = cust-list.sonst-umsatz + genstat.res-deci[5] 
                    cust-list.argtumsatz   = cust-list.argtumsatz + genstat.logis
                    cust-list.gesamtumsatz = cust-list.gesamtumsatz + genstat.logis + genstat.res-deci[2] 
                                                 + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]
                    cust-list.logiernachte = cust-list.logiernachte + 1.

            IF excl-other = NO THEN DO:
                /*Revenue from other*/
                IF curr-resnr1 NE genstat.resnr OR curr-reslinnr1 NE genstat.res-int[1] THEN DO:
                    ASSIGN
                        curr-resnr1 = genstat.resnr 
                        curr-reslinnr1 = genstat.res-int[1].
        
                    /*FIND FIRST bill WHERE bill.resnr = genstat.resnr
                        AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK NO-ERROR.*/
                    FOR EACH bill WHERE bill.resnr = genstat.resnr
                        AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK:
                        FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                            AND bill-line.bill-datum = genstat.datum NO-LOCK,
                            FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                                AND artikel.departement = bill-line.departement 
                                AND artikel.artart = 0 NO-LOCK :
                            IF currency NE " " THEN DO:
                                FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                                IF AVAILABLE exrate THEN 
                                        ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + (bill-line.betrag / exrate.betrag)
                                               cust-list.gesamtumsatz = cust-list.gesamtumsatz + (bill-line.betrag / exrate.betrag).
                            END.
                            ELSE 
                                ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + bill-line.betrag
                                       cust-list.gesamtumsatz = cust-list.gesamtumsatz + bill-line.betrag.
                        END.
                    END.
                END.
            END.
            
    
            /*IF AVAILABLE bill THEN DO:
                FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                    AND bill-line.bill-datum = genstat.datum NO-LOCK,
                    FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                        AND artikel.departement = bill-line.departement 
                        AND artikel.artart = 0 NO-LOCK :
                    IF currency NE " " THEN DO:
                        FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                        IF AVAILABLE exrate THEN 
                                ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + (bill-line.betrag / exrate.betrag)
                                       cust-list.gesamtumsatz = cust-list.gesamtumsatz + (bill-line.betrag / exrate.betrag).
                    END.
                    ELSE 
                        ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + bill-line.betrag
                               cust-list.gesamtumsatz = cust-list.gesamtumsatz + bill-line.betrag.
                END.
            END.  */      
        END.

        IF excl-other = NO THEN DO:
            /*Revenue from outlet*/
            FOR EACH guest-queasy WHERE guest-queasy.KEY = "gast-info"
                    AND guest-queasy.date1 GE fdate
                    AND guest-queasy.date1 LE tdate NO-LOCK :
              
                    FIND FIRST genstat WHERE genstat.resnr = guest-queasy.number2 
                        AND genstat.res-int[1] = guest-queasy.number3 
                        AND genstat.datum = guest-queasy.date1
                        AND genstat.res-logic[2] EQ YES NO-LOCK NO-ERROR.
                    IF AVAILABLE genstat THEN DO:
                        FIND FIRST cust-list WHERE cust-list.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
                        IF AVAILABLE cust-list THEN DO:
                            DO loopj = 1 TO NUM-ENTRIES(cust-list.resnr, ";"):
                                IF ENTRY(loopj, cust-list.resnr, ";") = STRING(genstat.resnr) THEN DO:
                                    ASSIGN found-it = YES.
                                    LEAVE.
                                END.
                                ELSE found-it = NO.
                            END.
                            IF found-it = YES THEN DO:
                                IF currency NE " " THEN DO:
                                    FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                                    IF AVAILABLE exrate THEN 
                                        ASSIGN
                                            cust-list.f-b-umsatz   = cust-list.f-b-umsatz + ((guest-queasy.deci1 + guest-queasy.deci2) / exrate.betrag)
                                            cust-list.sonst-umsatz = cust-list.sonst-umsatz + (guest-queasy.deci3 / exrate.betrag)
                                            cust-list.gesamtumsatz = cust-list.gesamtumsatz + ((guest-queasy.deci1 + guest-queasy.deci2 + guest-queasy.deci3) / exrate.betrag). 
                                END.
                                ELSE
                                    ASSIGN
                                        cust-list.f-b-umsatz   = cust-list.f-b-umsatz + guest-queasy.deci1 + guest-queasy.deci2
                                        cust-list.sonst-umsatz = cust-list.sonst-umsatz + guest-queasy.deci3
                                        cust-list.gesamtumsatz = cust-list.gesamtumsatz + guest-queasy.deci1 + guest-queasy.deci2 + guest-queasy.deci3.               
                            END.
                        END.           
                    END.
             END.
        END.

        FOR EACH t-genstat WHERE t-genstat.datum GE fdate AND t-genstat.datum LE tdate
              AND t-genstat.res-deci[7] NE 0,
              FIRST guest WHERE guest.gastnr = t-genstat.gastnr
              AND guest.karteityp = cardtype NO-LOCK BY guest.gesamtumsatz descending
              BY guest.logiernachte descending BY guest.name :
        
              FIND FIRST cust-list WHERE cust-list.gastnr = t-genstat.gastnr NO-LOCK NO-ERROR.
              IF AVAILABLE cust-list THEN DO:
                   IF currency NE " " THEN DO:
                        FIND FIRST exrate WHERE exrate.datum = t-genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                        IF AVAILABLE exrate THEN 
                            ASSIGN cust-list.ba-umsatz = cust-list.ba-umsatz + (t-genstat.res-deci[7] / exrate.betrag)
                                   cust-list.gesamtumsatz = cust-list.gesamtumsatz + (t-genstat.res-deci[7] / exrate.betrag).
                   END.
                   ELSE
                        ASSIGN cust-list.ba-umsatz = cust-list.ba-umsatz + t-genstat.res-deci[7]
                               cust-list.gesamtumsatz = cust-list.gesamtumsatz + t-genstat.res-deci[7].
              END.
              ELSE DO:
                  CREATE cust-list.
                  ASSIGN
                    cust-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                         + guest.anredefirm) 
                    cust-list.gastnr    = guest.gastnr
                    cust-list.wohnort   = guest.wohnort 
                    cust-list.plz       = guest.plz 
                    cust-list.land      = guest.land
                    cust-list.sales-id  = guest.phonetik3 /*MT 22/05/12*/.
                    
                  IF currency NE " " THEN DO:
                        FIND FIRST exrate WHERE exrate.datum = t-genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                        IF AVAILABLE exrate THEN 
                            ASSIGN
                                cust-list.ba-umsatz    = (t-genstat.res-deci[7] / exrate.betrag)
                                cust-list.gesamtumsatz = cust-list.gesamtumsatz + (t-genstat.res-deci[7] / exrate.betrag).
                  END.
                  ELSE
                      ASSIGN
                        cust-list.ba-umsatz    = t-genstat.res-deci[7]
                        cust-list.gesamtumsatz = cust-list.gesamtumsatz + t-genstat.res-deci[7].

                  FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
                  IF AVAILABLE nation THEN
                  DO:
                    FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                      cust-list.region = queasy.char1.
                  END.
                  ELSE cust-list.region = "UNKNOWN".
              END.
        END.
    END.
    ELSE 
         RUN cr-ftd.
    
    IF tdate NE ? AND tdate GE ci-date AND check-ftd THEN RUN create-forecast.
END.

PROCEDURE create-forecast:
    DEFINE VARIABLE do-it   AS LOGICAL INIT YES.
    DEFINE VARIABLE datum   AS DATE. 
    DEFINE VARIABLE datum1  AS DATE. 
    DEFINE VARIABLE datum2  AS DATE. 
    DEFINE VARIABLE d2      AS DATE.
    DEFINE VARIABLE curr-resnr    AS INTEGER NO-UNDO.
    DEFINE VARIABLE curr-reslinnr AS INTEGER NO-UNDO.

    IF fdate NE ci-date AND fdate LT ci-date THEN fdate = ci-date.
    datum1 = fdate. 
    IF tdate LT (ci-date - 1) THEN d2 = tdate.
    ELSE d2 = ci-date - 1. 
    d2 = d2 + 1. 

    FOR EACH res-line WHERE 
        (res-line.active-flag LE 1 AND res-line.resstatus LE 13 
         AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
         AND NOT (res-line.ankunft GT tdate) AND 
         NOT (res-line.abreise LE fdate)) 
         OR (res-line.active-flag = 2 AND res-line.resstatus = 8
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
        USE-INDEX gnrank_ix NO-LOCK,
        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = cardtype 
        BY res-line.gastnr BY res-line.resnr BY res-line.reslinnr: /*MT 13/08/12 */


        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
            NO-LOCK NO-ERROR.
        FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart
            NO-LOCK NO-ERROR.

        ASSIGN 
            curr-i = 0
            do-it = YES.

        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
        ASSIGN do-it = AVAILABLE segment AND segment.vip-level = 0.

        /*IF res-line.zinr NE "" THEN
        DO:
            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
            IF AVAILABLE zimmer AND NOT zimmer.sleeping THEN do-it = NO.
        END.*/

        IF do-it AND res-line.resstatus = 8 THEN
        DO:
            FIND FIRST arrangement WHERE arrangement.arrangement 
              =  res-line.arrangement NO-LOCK. 
            FIND FIRST bill-line WHERE bill-line.departement = 0
              AND bill-line.artnr = arrangement.argt-artikelnr
              AND bill-line.bill-datum = ci-date
              AND bill-line.massnr = res-line.resnr
              AND bill-line.billin-nr = res-line.reslinnr
              USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
            do-it = AVAILABLE bill-line.
        END.

        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
        IF do-it AND AVAILABLE zimmer THEN 
        DO: 
            FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
              AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
            IF zimmer.sleeping THEN 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 EQ res-line.gastnr THEN 
                  do-it = NO. 
            END. 
            ELSE 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN . 
                ELSE do-it = NO. 
            END. 
        END.                                    


        IF do-it THEN
        DO:
            FIND FIRST cust-list WHERE cust-list.gastnr = res-line.gastnr NO-ERROR.
            IF NOT AVAILABLE cust-list THEN
            DO:
                CREATE cust-list.
                ASSIGN
                    cust-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                         + guest.anredefirm) 
                    cust-list.gastnr    = guest.gastnr
                    cust-list.wohnort   = guest.wohnort 
                    cust-list.plz       = guest.plz 
                    cust-list.land      = guest.land
                    cust-list.sales-id  = guest.phonetik3 /*MT 22/05/12*/.
    
                FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                        cust-list.region = queasy.char1.
                END.
                ELSE cust-list.region = "UNKNOWN".
            END.
    
            found = NO.
    
            IF cust-list.resnr NE "" THEN
            DO:
              DO i = 1 TO NUM-ENTRIES(cust-list.resnr,";"):
                  IF ENTRY(i,cust-list.resnr,";") NE "" THEN
                  DO:
                      IF INT(ENTRY(i,cust-list.resnr,";")) = res-line.resnr THEN
                      DO:
                          found = YES.
                          LEAVE.
                      END.      
                  END.
              END.
              IF NOT found THEN
                  cust-list.resnr     = cust-list.resnr + STRING(res-line.resnr) + ";".
            END.    
            ELSE
              cust-list.resnr     = cust-list.resnr + STRING(res-line.resnr) + ";".
            
            IF res-line.ankunft GT fdate THEN datum1 = res-line.ankunft. 
            ELSE datum1 = fdate.
            IF res-line.abreise LT tdate THEN datum2 = res-line.abreise - 1.
            ELSE datum2 = tdate.
                
            DO datum = datum1 TO datum2:
                ASSIGN
                    curr-i        = curr-i + 1 
                    net-lodg      = 0
                    Fnet-lodg     = 0
                    tot-breakfast = 0
                    tot-lunch     = 0 
                    tot-dinner    = 0
                    tot-other     = 0
                    tot-rmrev     = 0
                    tot-vat       = 0
                    tot-service   = 0.  
    
                RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, ci-date,
                    OUTPUT Fnet-lodg, OUTPUT net-lodg,
                    OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                    OUTPUT tot-dinner, OUTPUT tot-other,
                    OUTPUT tot-rmrev, OUTPUT tot-vat,
                    OUTPUT tot-service).

                IF currency NE " " THEN 
                    ASSIGN
                        cust-list.gesamtumsatz = cust-list.gesamtumsatz + ((net-lodg + tot-breakfast 
                                                 + tot-lunch + tot-dinner + tot-other) / exrate)
                        cust-list.argtumsatz = cust-list.argtumsatz + (net-lodg / exrate)
                        cust-list.f-b-umsatz = cust-list.f-b-umsatz + ((tot-breakfast + tot-lunch + tot-dinner) / exrate)
                        cust-list.sonst-umsatz = cust-list.sonst-umsatz + (tot-other / exrate).
                ELSE    
                    ASSIGN
                        cust-list.gesamtumsatz = cust-list.gesamtumsatz + net-lodg + tot-breakfast 
                                                 + tot-lunch + tot-dinner + tot-other
                        cust-list.argtumsatz = cust-list.argtumsatz + net-lodg
                        cust-list.f-b-umsatz = cust-list.f-b-umsatz + tot-breakfast + tot-lunch + tot-dinner
                        cust-list.sonst-umsatz = cust-list.sonst-umsatz + tot-other.

                IF excl-other = NO THEN DO:
                    /*Revenue from other*/
                    IF curr-resnr NE res-line.resnr OR curr-reslinnr NE res-line.reslinnr THEN DO:
                        ASSIGN
                            curr-resnr = res-line.resnr 
                            curr-reslinnr = res-line.reslinnr.
            
                        /*FIND FIRST bill WHERE bill.resnr = res-line.resnr
                            AND bill.reslinnr = res-line.reslinnr USE-INDEX reserv_index NO-LOCK NO-ERROR.*/
                        FOR EACH bill WHERE bill.resnr = res-line.resnr
                            AND bill.reslinnr = res-line.reslinnr USE-INDEX reserv_index NO-LOCK :
                            FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                                AND bill-line.bill-datum = datum NO-LOCK,
                                FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                                    AND artikel.departement = bill-line.departement 
                                    AND artikel.artart = 0 NO-LOCK :
                                IF currency NE " " THEN 
                                    ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + (bill-line.betrag / exrate)
                                           cust-list.gesamtumsatz = cust-list.gesamtumsatz + (bill-line.betrag / exrate).
                                ELSE
                                    ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + bill-line.betrag
                                           cust-list.gesamtumsatz = cust-list.gesamtumsatz + bill-line.betrag.
                            END.
                        END.
                    END.
                END.
                
                /*
                IF AVAILABLE bill THEN DO:
                    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                        AND bill-line.bill-datum = datum NO-LOCK,
                        FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                            AND artikel.departement = bill-line.departement 
                            AND artikel.artart = 0 NO-LOCK :
                        IF currency NE " " THEN 
                            ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + (bill-line.betrag / exrate)
                                   cust-list.gesamtumsatz = cust-list.gesamtumsatz + (bill-line.betrag / exrate).
                        ELSE
                            ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + bill-line.betrag
                                   cust-list.gesamtumsatz = cust-list.gesamtumsatz + bill-line.betrag.
                    END.
                END.       */ 
                
                IF ((res-line.ankunft LT res-line.abreise) AND res-line.abreise NE datum) 
                    OR (res-line.ankunft = res-line.abreise) THEN 
                DO:                     
                    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                        AND res-line.resstatus NE 3 AND NOT res-line.zimmerfix THEN DO:                        
                            /*ASSIGN cust-list.logiernachte = cust-list.logiernachte + res-line.zimmeranz.*/
                            ASSIGN cust-list.logiernachte = cust-list.logiernachte + 1.
                    END.
                END.
            END. 
        END.
    END.
    
    IF excl-other = NO THEN DO:
        /*Revenue from outlet*/
        FOR EACH guest-queasy WHERE guest-queasy.KEY = "gast-info"
            AND guest-queasy.date1 GE fdate
            AND guest-queasy.date1 LE tdate NO-LOCK :
      
            FIND FIRST res-line WHERE 
                res-line.resnr EQ guest-queasy.number2 AND
                res-line.reslinnr EQ guest-queasy.number3 NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN DO:
                FIND FIRST cust-list WHERE cust-list.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE cust-list THEN DO:
                    DO loopj = 1 TO NUM-ENTRIES(cust-list.resnr, ";"):
                        IF ENTRY(loopj, cust-list.resnr, ";") = STRING(res-line.resnr) THEN DO:
                            ASSIGN found-it = YES.
                            LEAVE.
                        END.
                        ELSE found-it = NO.
                    END.
                    IF found-it = YES THEN DO:
                        IF currency NE " " THEN
                            ASSIGN
                                cust-list.f-b-umsatz   = cust-list.f-b-umsatz + ((guest-queasy.deci1 + guest-queasy.deci2) / exrate)
                                cust-list.sonst-umsatz = cust-list.sonst-umsatz + (guest-queasy.deci3 / exrate)
                                cust-list.gesamtumsatz = cust-list.gesamtumsatz + ((guest-queasy.deci1 + guest-queasy.deci2 + guest-queasy.deci3) / exrate).    
                        END.
                        ELSE
                            ASSIGN
                                cust-list.f-b-umsatz   = cust-list.f-b-umsatz + guest-queasy.deci1 + guest-queasy.deci2
                                cust-list.sonst-umsatz = cust-list.sonst-umsatz + guest-queasy.deci3
                                cust-list.gesamtumsatz = cust-list.gesamtumsatz + guest-queasy.deci1 + guest-queasy.deci2 + guest-queasy.deci3.  
                    END.                      
            END.
        END.
    END.
    

    IF DAY(fdate) = 29 AND MONTH(fdate) = 2 THEN
        ly-fdate = DATE(MONTH(fdate),28,YEAR(fdate) - 1).
    ELSE ly-fdate = DATE(MONTH(fdate),DAY(fdate),YEAR(fdate) - 1).

    IF DAY(tdate) = 29 AND MONTH(tdate) = 2 THEN
        ly-tdate = DATE(MONTH(tdate),28,YEAR(tdate) - 1).
    ELSE ly-tdate = DATE(MONTH(tdate),DAY(tdate),YEAR(tdate) - 1).

    FOR EACH genstat WHERE 
        genstat.datum GE ly-fdate
        AND genstat.datum LE ly-tdate
        /*AND genstat.resstatus NE 13*/
        AND genstat.segmentcode NE 0 
        AND genstat.nationnr NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */ ,
        FIRST guest WHERE guest.gastnr = genstat.gastnr
        AND guest.karteityp = cardtype NO-LOCK BY guest.gesamtumsatz DESCENDING BY guest.logiernachte DESCENDING BY guest.NAME :
        
        FIND FIRST cust-list WHERE cust-list.gastnr = guest.gastnr NO-ERROR.
        IF AVAILABLE cust-list THEN
        DO:
            IF currency NE " " THEN DO:
                  FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                  IF AVAILABLE exrate THEN 
                        ASSIGN cust-list.ly-rev = cust-list.ly-rev + ((genstat.logis + genstat.res-deci[2] +
                                                  genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]) / exrate.betrag).
            END.
            ELSE ASSIGN cust-list.ly-rev = cust-list.ly-rev + genstat.logis + genstat.res-deci[2] +
                                           genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5].
        END.                                                                                         
    END.
END.

PROCEDURE cr-ftd:
  DEFINE VARIABLE t-argtumsatz  AS INT.
  DEFINE VARIABLE rate          AS DECIMAL INITIAL 1. 
  DEFINE VARIABLE frate         AS DECIMAL INITIAL 1. 
  DEFINE VARIABLE rmnite        AS INTEGER  NO-UNDO INIT 0.

  DEFINE VARIABLE curr-resnr    AS INTEGER NO-UNDO.
  DEFINE VARIABLE curr-reslinnr AS INTEGER NO-UNDO.

  

  FOR EACH cust-list2 :
      DELETE cust-list2.
    END.

  FOR EACH genstat WHERE 
      genstat.datum GE fdate
      AND genstat.datum LE tdate
      /*AND genstat.resstatus NE 13*/
      AND genstat.segmentcode NE 0 
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */ ,
      FIRST guest WHERE guest.gastnr = genstat.gastnr
      AND guest.karteityp = cardtype NO-LOCK 
      BY genstat.gastnr BY genstat.resnr BY guest.land :

      FIND FIRST cust-list WHERE cust-list.gastnr = guest.gastnr NO-ERROR.
      IF NOT AVAILABLE cust-list THEN
      DO:
          CREATE cust-list.
          ASSIGN
            cust-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                 + guest.anredefirm) 
            cust-list.gastnr    = guest.gastnr
            cust-list.wohnort   = guest.wohnort 
            cust-list.plz       = guest.plz 
            cust-list.land      = guest.land
            cust-list.sales-id  = guest.phonetik3 /*MT 22/05/12*/.

          FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
          IF AVAILABLE nation THEN
          DO:
            FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
              cust-list.region = queasy.char1.
          END.
          ELSE cust-list.region = "UNKNOWN".
      END.

      found = NO.

      IF cust-list.resnr NE "" THEN
      DO:
          DO i = 1 TO NUM-ENTRIES(cust-list.resnr,";"):
              IF ENTRY(i,cust-list.resnr,";") NE "" THEN
              DO:
                  IF INT(ENTRY(i,cust-list.resnr,";")) = genstat.resnr THEN
                  DO:
                      found = YES.
                      LEAVE.
                  END.      
              END.
          END.
          IF NOT found THEN
              cust-list.resnr     = cust-list.resnr + STRING(genstat.resnr) + ";".
      END.    
      ELSE
          cust-list.resnr     = cust-list.resnr + STRING(genstat.resnr) + ";".

      FIND FIRST artikel WHERE artikel.zwkum = bfast-art NO-LOCK NO-ERROR.
      IF AVAILABLE artikel THEN
             RUN calc-servvat.p(artikel.departement, artikel.artnr, genstat.datum, 
                   artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).

      IF currency NE " " THEN DO:
            FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
            IF AVAILABLE exrate THEN 
                ASSIGN
                    cust-list.f-b-umsatz   = cust-list.f-b-umsatz + ((genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]) / exrate.betrag)
                    cust-list.sonst-umsatz = cust-list.sonst-umsatz + (genstat.res-deci[5] / exrate.betrag)
                    cust-list.argtumsatz   = cust-list.argtumsatz + (genstat.logis / exrate.betrag)
                    cust-list.gesamtumsatz = cust-list.gesamtumsatz + ((genstat.logis + genstat.res-deci[2]
                                             + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]) / exrate.betrag).
      END.
      ELSE 
          ASSIGN
                cust-list.f-b-umsatz   = cust-list.f-b-umsatz + genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]
                cust-list.sonst-umsatz = cust-list.sonst-umsatz + genstat.res-deci[5]
                cust-list.argtumsatz   = cust-list.argtumsatz + genstat.logis
                cust-list.gesamtumsatz = cust-list.gesamtumsatz + genstat.logis + genstat.res-deci[2]
                                         + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5].

       IF genstat.resstatus NE 13 THEN ASSIGN cust-list.logiernachte = cust-list.logiernachte + 1.            

       IF excl-other = NO THEN DO:
            /*Revenue from other*/
            IF curr-resnr NE genstat.resnr OR curr-reslinnr NE genstat.res-int[1] THEN DO:
                ASSIGN
                    curr-resnr = genstat.resnr 
                    curr-reslinnr = genstat.res-int[1].
    
                /*FIND FIRST bill WHERE bill.resnr = genstat.resnr
                    AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK NO-ERROR.*/
                FOR EACH bill WHERE bill.resnr = genstat.resnr
                    AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK :
                    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                        AND bill-line.bill-datum = genstat.datum NO-LOCK,
                        FIRST artikel WHERE artikel.artnr = bill-line.artnr AND artikel.departement = bill-line.departement 
                            AND artikel.artart = 0 NO-LOCK :
                        IF currency NE " " THEN DO:
                            FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                            IF AVAILABLE exrate THEN 
                                    ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + (bill-line.betrag / exrate.betrag)
                                           cust-list.gesamtumsatz = cust-list.gesamtumsatz + (bill-line.betrag / exrate.betrag).
                        END.
                        ELSE
                            ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + bill-line.betrag
                                   cust-list.gesamtumsatz = cust-list.gesamtumsatz + bill-line.betrag.
                    END.
                END.
            END.
       END.
        

        /*IF AVAILABLE bill THEN DO:
            FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                AND bill-line.bill-datum = genstat.datum NO-LOCK,
                FIRST artikel WHERE artikel.artnr = bill-line.artnr AND artikel.departement = bill-line.departement 
                    AND artikel.artart = 0 NO-LOCK :
                IF currency NE " " THEN DO:
                    FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                    IF AVAILABLE exrate THEN 
                            ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + (bill-line.betrag / exrate.betrag)
                                   cust-list.gesamtumsatz = cust-list.gesamtumsatz + (bill-line.betrag / exrate.betrag).
                END.
                ELSE
                    ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + bill-line.betrag
                           cust-list.gesamtumsatz = cust-list.gesamtumsatz + bill-line.betrag.
            END.
        END.        */
  END.
    
  IF excl-other = NO THEN DO:
      /*Revenue from outlet*/
      FOR EACH guest-queasy WHERE guest-queasy.KEY = "gast-info"
            AND guest-queasy.date1 GE fdate
            AND guest-queasy.date1 LE tdate NO-LOCK BY guest-queasy.number2:
      
            FIND FIRST genstat WHERE genstat.resnr = guest-queasy.number2 
                AND genstat.res-int[1] = guest-queasy.number3 
                AND genstat.datum = guest-queasy.date1
                AND genstat.res-logic[2] EQ YES NO-LOCK NO-ERROR.
            IF AVAILABLE genstat THEN DO:
                FIND FIRST cust-list WHERE cust-list.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE cust-list THEN DO:
                    /*IF genstat.gastnr = 6920 THEN DISP genstat.gastnr genstat.resnr cust-list.resnr FORMAT "x(80)".*/                    
                    DO loopj = 1 TO NUM-ENTRIES(cust-list.resnr, ";"):                        
                        IF ENTRY(loopj, cust-list.resnr, ";") = STRING(genstat.resnr) THEN DO:
                            ASSIGN found-it = YES.
                            LEAVE.
                        END.
                        ELSE found-it = NO.                        
                    END.
                    IF found-it = YES THEN DO:
                        IF currency NE " " THEN DO:
                            FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                            IF AVAILABLE exrate THEN 
                                ASSIGN
                                    cust-list.f-b-umsatz   = cust-list.f-b-umsatz + ((guest-queasy.deci1 + guest-queasy.deci2) / exrate.betrag)
                                    cust-list.sonst-umsatz = cust-list.sonst-umsatz + (guest-queasy.deci3 / exrate.betrag)
                                    cust-list.gesamtumsatz = cust-list.gesamtumsatz + ((guest-queasy.deci1 + guest-queasy.deci2 + guest-queasy.deci3) / exrate.betrag).    
                        END.
                        ELSE 
                            ASSIGN
                                cust-list.f-b-umsatz   = cust-list.f-b-umsatz + guest-queasy.deci1 + guest-queasy.deci2
                                cust-list.sonst-umsatz = cust-list.sonst-umsatz + guest-queasy.deci3
                                cust-list.gesamtumsatz = cust-list.gesamtumsatz + guest-queasy.deci1 + guest-queasy.deci2 + guest-queasy.deci3.               
                    END.                        
                END.
            END.
      END.
  END.
  
  
  FOR EACH cust-list2 NO-LOCK BY cust-list2.gesamtumsatz descending 
      BY cust-list2.logiernachte descending BY cust-list2.cust-name:
      CREATE cust-list.
      BUFFER-COPY cust-list2 TO cust-list.
  END.

  FOR EACH t-genstat WHERE t-genstat.datum GE fdate AND t-genstat.datum LE tdate
      AND t-genstat.res-deci[7] NE 0,
      FIRST guest WHERE guest.gastnr = t-genstat.gastnr
      AND guest.karteityp = cardtype NO-LOCK /*BY guest.gesamtumsatz descending
      BY guest.logiernachte descending BY guest.name*/ :

      FIND FIRST cust-list WHERE cust-list.gastnr = t-genstat.gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE cust-list THEN DO:
          IF currency NE " " THEN DO:
                FIND FIRST exrate WHERE exrate.datum = t-genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                IF AVAILABLE exrate THEN 
                    ASSIGN cust-list.ba-umsatz    = cust-list.ba-umsatz + (t-genstat.res-deci[7] / exrate.betrag)
                           cust-list.gesamtumsatz = cust-list.gesamtumsatz + (t-genstat.res-deci[7] / exrate.betrag).
          END.
          ELSE
            ASSIGN cust-list.ba-umsatz    = cust-list.ba-umsatz + t-genstat.res-deci[7]
                   cust-list.gesamtumsatz = cust-list.gesamtumsatz + t-genstat.res-deci[7].
      END.
      ELSE DO:
          CREATE cust-list.
          ASSIGN
            cust-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                 + guest.anredefirm) 
            cust-list.gastnr    = guest.gastnr
            cust-list.wohnort   = guest.wohnort 
            cust-list.plz       = guest.plz 
            cust-list.land      = guest.land
            cust-list.sales-id  = guest.phonetik3 /*MT 22/05/12*/.

          IF currency NE " " THEN DO:
                FIND FIRST exrate WHERE exrate.datum = t-genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                IF AVAILABLE exrate THEN 
                    ASSIGN 
                        cust-list.ba-umsatz    = (t-genstat.res-deci[7] / exrate.betrag)
                        cust-list.gesamtumsatz = cust-list.gesamtumsatz + (t-genstat.res-deci[7] / exrate.betrag).
          END.
          ELSE
            ASSIGN 
                cust-list.ba-umsatz    = t-genstat.res-deci[7]
                cust-list.gesamtumsatz = cust-list.gesamtumsatz + t-genstat.res-deci[7].

          FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
          IF AVAILABLE nation THEN
          DO:
            FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
              cust-list.region = queasy.char1.
          END.
          ELSE cust-list.region = "UNKNOWN".
      END.
  END.
END.


PROCEDURE create-forecast-all:
    DEFINE VARIABLE do-it   AS LOGICAL INIT YES.
    DEFINE VARIABLE datum   AS DATE. 
    DEFINE VARIABLE datum1  AS DATE. 
    DEFINE VARIABLE datum2  AS DATE. 
    DEFINE VARIABLE d2      AS DATE.
    DEFINE VARIABLE curr-resnr    AS INTEGER NO-UNDO.
    DEFINE VARIABLE curr-reslinnr AS INTEGER NO-UNDO.

    IF fdate NE ci-date AND fdate LT ci-date THEN fdate = ci-date.
    datum1 = fdate. 
    IF tdate LT (ci-date - 1) THEN d2 = tdate.
    ELSE d2 = ci-date - 1. 
    d2 = d2 + 1. 

    FOR EACH res-line WHERE 
        (res-line.active-flag LE 1 AND res-line.resstatus LE 13 
         AND res-line.resstatus NE 4 AND res-line.resstatus NE 12
         AND NOT (res-line.ankunft GT tdate) AND 
         NOT (res-line.abreise LE fdate)) 
         OR (res-line.active-flag = 2 AND res-line.resstatus = 8
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
        USE-INDEX gnrank_ix NO-LOCK,
        FIRST guest WHERE guest.gastnr = res-line.gastnr 
        BY res-line.gastnr BY res-line.resnr BY res-line.reslinnr: /*MT 13/08/12 */


        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
            NO-LOCK NO-ERROR.
        FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart
            NO-LOCK NO-ERROR.

        ASSIGN 
            curr-i = 0
            do-it = YES.

        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
        ASSIGN do-it = AVAILABLE segment AND segment.vip-level = 0.

        /*IF res-line.zinr NE "" THEN
        DO:
            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
            IF AVAILABLE zimmer AND NOT zimmer.sleeping THEN do-it = NO.
        END.*/

        IF do-it AND res-line.resstatus = 8 THEN
        DO:
            FIND FIRST arrangement WHERE arrangement.arrangement 
              =  res-line.arrangement NO-LOCK. 
            FIND FIRST bill-line WHERE bill-line.departement = 0
              AND bill-line.artnr = arrangement.argt-artikelnr
              AND bill-line.bill-datum = ci-date
              AND bill-line.massnr = res-line.resnr
              AND bill-line.billin-nr = res-line.reslinnr
              USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
            do-it = AVAILABLE bill-line.
        END.

        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
        IF do-it AND AVAILABLE zimmer THEN 
        DO: 
            FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
              AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
            IF zimmer.sleeping THEN 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 EQ res-line.gastnr THEN 
                  do-it = NO. 
            END. 
            ELSE 
            DO: 
                IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN . 
                ELSE do-it = NO. 
            END. 
        END.                                    


        IF do-it THEN
        DO:
            FIND FIRST cust-list WHERE cust-list.gastnr = res-line.gastnr NO-ERROR.
            IF NOT AVAILABLE cust-list THEN
            DO:
                CREATE cust-list.
                ASSIGN
                    cust-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                         + guest.anredefirm) 
                    cust-list.gastnr    = guest.gastnr
                    cust-list.wohnort   = guest.wohnort 
                    cust-list.plz       = guest.plz 
                    cust-list.land      = guest.land
                    cust-list.sales-id  = guest.phonetik3 /*MT 22/05/12*/.
    
                FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN
                DO:
                    FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                        cust-list.region = queasy.char1.
                END.
                ELSE cust-list.region = "UNKNOWN".
            END.
    
            found = NO.
    
            IF cust-list.resnr NE "" THEN
            DO:
              DO i = 1 TO NUM-ENTRIES(cust-list.resnr,";"):
                  IF ENTRY(i,cust-list.resnr,";") NE "" THEN
                  DO:
                      IF INT(ENTRY(i,cust-list.resnr,";")) = res-line.resnr THEN
                      DO:
                          found = YES.
                          LEAVE.
                      END.      
                  END.
              END.
              IF NOT found THEN
                  cust-list.resnr     = cust-list.resnr + STRING(res-line.resnr) + ";".
            END.    
            ELSE
              cust-list.resnr     = cust-list.resnr + STRING(res-line.resnr) + ";".
            
            IF res-line.ankunft GT fdate THEN datum1 = res-line.ankunft. 
            ELSE datum1 = fdate.
            IF res-line.abreise LT tdate THEN datum2 = res-line.abreise - 1.
            ELSE datum2 = tdate.
                
            DO datum = datum1 TO datum2:
                ASSIGN
                    curr-i        = curr-i + 1 
                    net-lodg      = 0
                    Fnet-lodg     = 0
                    tot-breakfast = 0
                    tot-lunch     = 0 
                    tot-dinner    = 0
                    tot-other     = 0
                    tot-rmrev     = 0
                    tot-vat       = 0
                    tot-service   = 0.  
    
                RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, ci-date,
                    OUTPUT Fnet-lodg, OUTPUT net-lodg,
                    OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                    OUTPUT tot-dinner, OUTPUT tot-other,
                    OUTPUT tot-rmrev, OUTPUT tot-vat,
                    OUTPUT tot-service).

                IF currency NE " " THEN 
                    ASSIGN
                        cust-list.gesamtumsatz = cust-list.gesamtumsatz + ((net-lodg + tot-breakfast 
                                                 + tot-lunch + tot-dinner + tot-other) / exrate)
                        cust-list.argtumsatz = cust-list.argtumsatz + (net-lodg / exrate)
                        cust-list.f-b-umsatz = cust-list.f-b-umsatz + (tot-breakfast + tot-lunch + tot-dinner / exrate)
                        cust-list.sonst-umsatz = cust-list.sonst-umsatz + (tot-other / exrate).

                ELSE    
                    ASSIGN
                        cust-list.gesamtumsatz = cust-list.gesamtumsatz + net-lodg + tot-breakfast 
                                                 + tot-lunch + tot-dinner + tot-other
                        cust-list.argtumsatz = cust-list.argtumsatz + net-lodg
                        cust-list.f-b-umsatz = cust-list.f-b-umsatz + tot-breakfast + tot-lunch + tot-dinner
                        cust-list.sonst-umsatz = cust-list.sonst-umsatz + tot-other.

                IF excl-other = NO THEN DO:
                     /*Revenue from other*/
                    IF curr-resnr NE res-line.resnr OR curr-reslinnr NE res-line.reslinnr THEN DO:
                        ASSIGN
                            curr-resnr = res-line.resnr 
                            curr-reslinnr = res-line.reslinnr.
            
                        /*FIND FIRST bill WHERE bill.resnr = res-line.resnr
                            AND bill.reslinnr = res-line.reslinnr USE-INDEX reserv_index NO-LOCK NO-ERROR.*/
                        FOR EACH bill WHERE bill.resnr = res-line.resnr
                            AND bill.reslinnr = res-line.reslinnr USE-INDEX reserv_index NO-LOCK :
    
                            FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                                AND bill-line.bill-datum = datum NO-LOCK,
                                FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                                    AND artikel.departement = bill-line.departement 
                                    AND artikel.artart = 0 NO-LOCK :
                                IF currency NE " " THEN
                                    ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + (bill-line.betrag / exrate)
                                           cust-list.gesamtumsatz = cust-list.gesamtumsatz + (bill-line.betrag / exrate).
                                ELSE
                                    ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + bill-line.betrag
                                           cust-list.gesamtumsatz = cust-list.gesamtumsatz + bill-line.betrag.
                            END.
                        END.
                    END.
                END.
                
                /*
                IF AVAILABLE bill THEN DO:
                    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                        AND bill-line.bill-datum = datum NO-LOCK,
                        FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                            AND artikel.departement = bill-line.departement 
                            AND artikel.artart = 0 NO-LOCK :
                        IF currency NE " " THEN
                            ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + (bill-line.betrag / exrate)
                                   cust-list.gesamtumsatz = cust-list.gesamtumsatz + (bill-line.betrag / exrate).
                        ELSE
                            ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + bill-line.betrag
                                   cust-list.gesamtumsatz = cust-list.gesamtumsatz + bill-line.betrag.
                    END.
                END.      */  
                
                IF ((res-line.ankunft LT res-line.abreise) AND res-line.abreise NE datum) 
                    OR (res-line.ankunft = res-line.abreise) THEN 
                DO:                     
                    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                        AND res-line.resstatus NE 3 AND NOT res-line.zimmerfix THEN DO:                        
                            /*ASSIGN cust-list.logiernachte = cust-list.logiernachte + res-line.zimmeranz.*/
                            ASSIGN cust-list.logiernachte = cust-list.logiernachte + 1.
                    END.
                END.
            END. 
        END.
    END.
    
    IF excl-other = NO THEN DO:
        /*Revenue from outlet*/
        FOR EACH guest-queasy WHERE guest-queasy.KEY = "gast-info"
            AND guest-queasy.date1 GE fdate
            AND guest-queasy.date1 LE tdate NO-LOCK :
      
            FIND FIRST res-line WHERE 
                res-line.resnr EQ guest-queasy.number2 AND
                res-line.reslinnr EQ guest-queasy.number3 NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN DO:
                FIND FIRST cust-list WHERE cust-list.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE cust-list THEN DO:
                    DO loopj = 1 TO NUM-ENTRIES(cust-list.resnr, ";"):
                        IF ENTRY(loopj, cust-list.resnr, ";") = STRING(res-line.resnr) THEN DO:
                            ASSIGN found-it = YES.
                            LEAVE.
                        END.
                        ELSE found-it = NO.
                    END.
                    IF found-it = YES THEN DO:
                        IF currency NE " " THEN
                            ASSIGN
                                cust-list.f-b-umsatz   = cust-list.f-b-umsatz + ((guest-queasy.deci1 + guest-queasy.deci2) / exrate)
                                cust-list.sonst-umsatz = cust-list.sonst-umsatz + (guest-queasy.deci3 / exrate)
                                cust-list.gesamtumsatz = cust-list.gesamtumsatz + ((guest-queasy.deci1 + guest-queasy.deci2 + guest-queasy.deci3) / exrate).
                        ELSE
                            ASSIGN
                                cust-list.f-b-umsatz   = cust-list.f-b-umsatz + guest-queasy.deci1 + guest-queasy.deci2
                                cust-list.sonst-umsatz = cust-list.sonst-umsatz + guest-queasy.deci3
                                cust-list.gesamtumsatz = cust-list.gesamtumsatz + guest-queasy.deci1 + guest-queasy.deci2 + guest-queasy.deci3.               
                    END.
                END.                      
            END.
        END.
    END.
    

    IF DAY(fdate) = 29 AND MONTH(fdate) = 2 THEN
        ly-fdate = DATE(MONTH(fdate),28,YEAR(fdate) - 1).
    ELSE ly-fdate = DATE(MONTH(fdate),DAY(fdate),YEAR(fdate) - 1).

    IF DAY(tdate) = 29 AND MONTH(tdate) = 2 THEN
        ly-tdate = DATE(MONTH(tdate),28,YEAR(tdate) - 1).
    ELSE ly-tdate = DATE(MONTH(tdate),DAY(tdate),YEAR(tdate) - 1).

    FOR EACH genstat WHERE 
        genstat.datum GE ly-fdate
        AND genstat.datum LE ly-tdate
        /*AND genstat.resstatus NE 13*/
        AND genstat.segmentcode NE 0 
        AND genstat.nationnr NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */ ,
        FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK BY guest.gesamtumsatz descending
        BY guest.logiernachte descending BY guest.NAME :
        
        FIND FIRST cust-list WHERE cust-list.gastnr = guest.gastnr NO-ERROR.
        IF AVAILABLE cust-list THEN
        DO:
            IF currency NE " " THEN DO:
                FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                IF AVAILABLE exrate THEN 
                       ASSIGN cust-list.ly-rev = cust-list.ly-rev + ((genstat.logis + genstat.res-deci[2] +
                                                 genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]) / exrate.betrag).
            END.
            ELSE
                ASSIGN cust-list.ly-rev = cust-list.ly-rev + genstat.logis + genstat.res-deci[2] +
                                          genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5].
        END.                                                                                         
    END.
END.

PROCEDURE cr-ftd-all:
  DEFINE VARIABLE t-argtumsatz  AS INT.
  DEFINE VARIABLE rate          AS DECIMAL INITIAL 1. 
  DEFINE VARIABLE frate         AS DECIMAL INITIAL 1. 
  DEFINE VARIABLE rmnite        AS INTEGER  NO-UNDO INIT 0.

  DEFINE VARIABLE curr-resnr    AS INTEGER NO-UNDO.
  DEFINE VARIABLE curr-reslinnr AS INTEGER NO-UNDO.

  

  FOR EACH cust-list2 :
      DELETE cust-list2.
    END.

  FOR EACH genstat WHERE 
      genstat.datum GE fdate
      AND genstat.datum LE tdate
      /*AND genstat.resstatus NE 13*/
      AND genstat.segmentcode NE 0 
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */ ,
      FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK 
      BY genstat.gastnr BY genstat.resnr BY guest.land :

      FIND FIRST cust-list WHERE cust-list.gastnr = guest.gastnr NO-ERROR.
      IF NOT AVAILABLE cust-list THEN
      DO:
          CREATE cust-list.
          ASSIGN
            cust-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                 + guest.anredefirm) 
            cust-list.gastnr    = guest.gastnr
            cust-list.wohnort   = guest.wohnort 
            cust-list.plz       = guest.plz 
            cust-list.land      = guest.land
            cust-list.sales-id  = guest.phonetik3 /*MT 22/05/12*/.

          FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
          IF AVAILABLE nation THEN
          DO:
            FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
              cust-list.region = queasy.char1.
          END.
          ELSE cust-list.region = "UNKNOWN".
      END.

      found = NO.

      IF cust-list.resnr NE "" THEN
      DO:
          DO i = 1 TO NUM-ENTRIES(cust-list.resnr,";"):
              IF ENTRY(i,cust-list.resnr,";") NE "" THEN
              DO:
                  IF INT(ENTRY(i,cust-list.resnr,";")) = genstat.resnr THEN
                  DO:
                      found = YES.
                      LEAVE.
                  END.      
              END.
          END.
          IF NOT found THEN
              cust-list.resnr     = cust-list.resnr + STRING(genstat.resnr) + ";".
      END.    
      ELSE
          cust-list.resnr     = cust-list.resnr + STRING(genstat.resnr) + ";".

      FIND FIRST artikel WHERE artikel.zwkum = bfast-art NO-LOCK NO-ERROR.
      IF AVAILABLE artikel THEN
             RUN calc-servvat.p(artikel.departement, artikel.artnr, genstat.datum, 
                   artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).
      IF currency NE " " THEN DO:
            FIND FIRST exrate WHERE exrate.datum = t-genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
            IF AVAILABLE exrate THEN 
                ASSIGN
                    cust-list.f-b-umsatz   = cust-list.f-b-umsatz + ((genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]) / exrate.betrag)
                    cust-list.sonst-umsatz = cust-list.sonst-umsatz + (genstat.res-deci[5] / exrate.betrag)
                    cust-list.argtumsatz   = cust-list.argtumsatz + (genstat.logis / exrate.betrag)
                    cust-list.gesamtumsatz = cust-list.gesamtumsatz + ((genstat.logis + genstat.res-deci[2]
                                                 + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5]) / exrate.betrag).
      END.
      ELSE 
          ASSIGN
                cust-list.f-b-umsatz   = cust-list.f-b-umsatz + genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]
                cust-list.sonst-umsatz = cust-list.sonst-umsatz + genstat.res-deci[5]
                cust-list.argtumsatz   = cust-list.argtumsatz + genstat.logis
                cust-list.gesamtumsatz = cust-list.gesamtumsatz + genstat.logis + genstat.res-deci[2]
                                             + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5].

       IF genstat.resstatus NE 13 THEN 
           ASSIGN cust-list.logiernachte = cust-list.logiernachte + 1.
       
       IF excl-other = NO THEN DO:
            /*Revenue from other*/
            IF curr-resnr NE genstat.resnr OR curr-reslinnr NE genstat.res-int[1] THEN DO:
                ASSIGN
                    curr-resnr = genstat.resnr 
                    curr-reslinnr = genstat.res-int[1].
    
                /*FIND FIRST bill WHERE bill.resnr = genstat.resnr
                    AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK NO-ERROR.*/
                FOR EACH bill WHERE bill.resnr = genstat.resnr
                    AND bill.reslinnr = genstat.res-int[1] USE-INDEX reserv_index NO-LOCK:
                    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                        AND bill-line.bill-datum = genstat.datum NO-LOCK,
                        FIRST artikel WHERE artikel.artnr = bill-line.artnr AND artikel.departement = bill-line.departement 
                            AND artikel.artart = 0 NO-LOCK :
        
                        IF currency NE " " THEN DO:
                            FIND FIRST exrate WHERE exrate.datum = t-genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                            IF AVAILABLE exrate THEN 
                                ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + (bill-line.betrag / exrate.betrag)
                                       cust-list.gesamtumsatz = cust-list.gesamtumsatz + (bill-line.betrag / exrate.betrag).
                        END.
                        ELSE 
                            ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + bill-line.betrag
                                   cust-list.gesamtumsatz = cust-list.gesamtumsatz + bill-line.betrag.
                    END.
                END.
            END.
       END.
        
        /*
        IF AVAILABLE bill THEN DO:
            FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr
                AND bill-line.bill-datum = genstat.datum NO-LOCK,
                FIRST artikel WHERE artikel.artnr = bill-line.artnr AND artikel.departement = bill-line.departement 
                    AND artikel.artart = 0 NO-LOCK :

                IF currency NE " " THEN DO:
                    FIND FIRST exrate WHERE exrate.datum = t-genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                    IF AVAILABLE exrate THEN 
                        ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + (bill-line.betrag / exrate.betrag)
                               cust-list.gesamtumsatz = cust-list.gesamtumsatz + (bill-line.betrag / exrate.betrag).
                END.
                ELSE 
                    ASSIGN cust-list.sonst-umsatz = cust-list.sonst-umsatz + bill-line.betrag
                           cust-list.gesamtumsatz = cust-list.gesamtumsatz + bill-line.betrag.
            END.
        END.*/        
  END.
    
  IF excl-other = NO THEN DO:
    /*Revenue from outlet*/
      FOR EACH guest-queasy WHERE guest-queasy.KEY = "gast-info"
            AND guest-queasy.date1 GE fdate
            AND guest-queasy.date1 LE tdate NO-LOCK BY guest-queasy.number2:
      
            FIND FIRST genstat WHERE genstat.resnr = guest-queasy.number2 
                AND genstat.res-int[1] = guest-queasy.number3 
                AND genstat.datum = guest-queasy.date1
                AND genstat.res-logic[2] EQ YES NO-LOCK NO-ERROR.
            IF AVAILABLE genstat THEN DO:
                FIND FIRST cust-list WHERE cust-list.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE cust-list THEN DO:
                    /*IF genstat.gastnr = 6920 THEN DISP genstat.gastnr genstat.resnr cust-list.resnr FORMAT "x(80)".*/
                    DO loopj = 1 TO NUM-ENTRIES(cust-list.resnr, ";"):
                        IF ENTRY(loopj, cust-list.resnr, ";") = STRING(genstat.resnr) THEN DO:
                            ASSIGN found-it = YES.
                            LEAVE.
                        END.
                        ELSE found-it = NO.
                    END.
                    IF found-it = YES THEN DO:
                        IF currency NE " " THEN DO:
                            FIND FIRST exrate WHERE exrate.datum = genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                            IF AVAILABLE exrate THEN 
                                ASSIGN
                                    cust-list.f-b-umsatz   = cust-list.f-b-umsatz + ((guest-queasy.deci1 + guest-queasy.deci2) / exrate.betrag)
                                    cust-list.sonst-umsatz = cust-list.sonst-umsatz + (guest-queasy.deci3 / exrate.betrag)
                                    cust-list.gesamtumsatz = cust-list.gesamtumsatz + ((guest-queasy.deci1 + guest-queasy.deci2 + guest-queasy.deci3) / exrate.betrag).    
                        END.
                        ELSE                    
                            ASSIGN
                                cust-list.f-b-umsatz   = cust-list.f-b-umsatz + guest-queasy.deci1 + guest-queasy.deci2
                                cust-list.sonst-umsatz = cust-list.sonst-umsatz + guest-queasy.deci3
                                cust-list.gesamtumsatz = cust-list.gesamtumsatz + guest-queasy.deci1 + guest-queasy.deci2 + guest-queasy.deci3.               
                    END.
                END.
            END.
      END.
  END.
  
  
  FOR EACH cust-list2 NO-LOCK BY cust-list2.gesamtumsatz descending 
      BY cust-list2.logiernachte descending BY cust-list2.cust-name:
      CREATE cust-list.
      BUFFER-COPY cust-list2 TO cust-list.
  END.

  FOR EACH t-genstat WHERE t-genstat.datum GE fdate AND t-genstat.datum LE tdate
      AND t-genstat.res-deci[7] NE 0,
      FIRST guest WHERE guest.gastnr = t-genstat.gastnr NO-LOCK /*BY guest.gesamtumsatz descending
      BY guest.logiernachte descending BY guest.name*/ :

      FIND FIRST cust-list WHERE cust-list.gastnr = t-genstat.gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE cust-list THEN DO:
           IF currency NE " " THEN DO:
                FIND FIRST exrate WHERE exrate.datum = t-genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                IF AVAILABLE exrate THEN 
                    ASSIGN cust-list.ba-umsatz    = cust-list.ba-umsatz + (t-genstat.res-deci[7] / exrate.betrag)
                           cust-list.gesamtumsatz = cust-list.gesamtumsatz + (t-genstat.res-deci[7] / exrate.betrag).
           END.
           ELSE
                ASSIGN cust-list.ba-umsatz = cust-list.ba-umsatz + t-genstat.res-deci[7]
                       cust-list.gesamtumsatz = cust-list.gesamtumsatz + t-genstat.res-deci[7].
      END.
      ELSE DO:
          CREATE cust-list.
          ASSIGN
            cust-list.cust-name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
                                 + guest.anredefirm) 
            cust-list.gastnr    = guest.gastnr
            cust-list.wohnort   = guest.wohnort 
            cust-list.plz       = guest.plz 
            cust-list.land      = guest.land
            cust-list.sales-id  = guest.phonetik3 /*MT 22/05/12*/.
            
          IF currency NE " " THEN DO:
                FIND FIRST exrate WHERE exrate.datum = t-genstat.datum AND exrate.artnr = exratenr NO-LOCK NO-ERROR.
                IF AVAILABLE exrate THEN 
                    ASSIGN cust-list.ba-umsatz    = (t-genstat.res-deci[7] / exrate.betrag)
                           cust-list.gesamtumsatz = cust-list.gesamtumsatz + (t-genstat.res-deci[7] / exrate.betrag).
          END.
          ELSE
              ASSIGN
                cust-list.ba-umsatz    = t-genstat.res-deci[7]
                cust-list.gesamtumsatz = cust-list.gesamtumsatz + t-genstat.res-deci[7].

          FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
          IF AVAILABLE nation THEN
          DO:
            FIND FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
              cust-list.region = queasy.char1.
          END.
          ELSE cust-list.region = "UNKNOWN".
      END.
  END.
END.



