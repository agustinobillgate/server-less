/*FT 280513 ubah perhitungan nett-lamt*/
/*FT 041113 ubah qty1 =  res-line.zimmeranz , add fargt-betrag*/
{supertrans.i} 
DEF VAR lvCAREA AS CHAR INITIAL "occ-fcast1". 

DEF INPUT  PARAMETER recid-resline  AS INT.
DEF INPUT  PARAMETER datum          AS DATE.
DEF INPUT  PARAMETER curr-i         AS INTEGER.
DEF INPUT  PARAMETER curr-date      AS DATE.
DEF INPUT  PARAMETER banquet-dept   AS CHARACTER.
DEF INPUT  PARAMETER commision      AS CHARACTER.
DEF INPUT  PARAMETER payable        AS CHARACTER.
DEF OUTPUT PARAMETER Fnet-lodging   AS DECIMAL FORMAT "->,>>>,>>9.99".
DEF OUTPUT PARAMETER Lnet-lodging   AS DECIMAL FORMAT "->,>>>,>>9.99".

DEF OUTPUT PARAMETER net-breakfast  AS DECIMAL FORMAT "->,>>>,>>9.99".
DEF OUTPUT PARAMETER net-lunch      AS DECIMAL FORMAT "->,>>>,>>9.99".
DEF OUTPUT PARAMETER net-dinner     AS DECIMAL FORMAT "->,>>>,>>9.99".
DEF OUTPUT PARAMETER net-others     AS DECIMAL FORMAT "->,>>>,>>9.99".

DEF OUTPUT PARAMETER tot-rmrev      AS DECIMAL INITIAL 0. 
/* always include tax and service */

DEF OUTPUT PARAMETER nett-vat       AS DECIMAL INITIAL 0. 
DEF OUTPUT PARAMETER nett-service   AS DECIMAL INITIAL 0.

DEF OUTPUT PARAMETER net-banquet    AS DECIMAL FORMAT "->,>>>,>>9.99".
DEF OUTPUT PARAMETER net-commision  AS DECIMAL FORMAT "->,>>>,>>9.99".
DEF OUTPUT PARAMETER net-payable    AS DECIMAL FORMAT "->,>>>,>>9.99".

/*FT
def var banquet-dept   AS CHARACTER.
def var commision      AS CHARACTER.
def var payable        AS CHARACTER.
def var net-banquet    AS DECIMAL FORMAT "->,>>>,>>9.99".
def var net-commision  AS DECIMAL FORMAT "->,>>>,>>9.99".
def var net-payable    AS DECIMAL FORMAT "->,>>>,>>9.99".
DEF var recid-resline  AS INT.
DEF var datum          AS DATE INIT 01/10/16.
DEF var curr-i         AS INTEGER INIT 1.
DEF var curr-date      AS DATE INIT 01/10/16.
DEF var Fnet-lodging   AS DECIMAL FORMAT "->,>>>,>>9.99".
DEF var Lnet-lodging   AS DECIMAL FORMAT "->,>>>,>>9.99".

DEF var net-breakfast  AS DECIMAL FORMAT "->,>>>,>>9.99".
DEF var net-lunch      AS DECIMAL FORMAT "->,>>>,>>9.99".
DEF var net-dinner     AS DECIMAL FORMAT "->,>>>,>>9.99".
DEF var net-others     AS DECIMAL FORMAT "->,>>>,>>9.99".

DEF var tot-rmrev      AS DECIMAL INITIAL 0. 
/* always include tax and service */

DEF var nett-vat        AS DECIMAL INITIAL 0. 
DEF VAR nett-service    AS DECIMAL INITIAL 0. 

DEFINE BUFFER bres FOR res-line.
FIND FIRST bres WHERE bres.resnr = 18995 AND bres.reslinnr = 1.
recid-resline = RECID(bres).
*/

DEFINE VARIABLE exrate          AS DECIMAL. 
DEFINE VARIABLE frate           AS DECIMAL. 
DEFINE VARIABLE price-decimal   AS INTEGER. 
DEFINE VARIABLE new-contrate    AS LOGICAL INITIAL NO NO-UNDO. 
DEFINE VARIABLE bonus-array     AS LOGICAL EXTENT 999 INITIAL NO. 
DEFINE VARIABLE wd-array AS INTEGER EXTENT 8 
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

DEFINE VARIABLE rm-vat     AS LOGICAL NO-UNDO.
DEFINE VARIABLE rm-serv    AS LOGICAL NO-UNDO.
DEFINE VARIABLE nett-rmrev AS DECIMAL INITIAL 0.

DEFINE VARIABLE j                AS INTEGER INIT 0   NO-UNDO.
DEFINE VARIABLE ex-article       AS CHARACTER        NO-UNDO.
DEFINE VARIABLE done             AS LOGICAL          NO-UNDO.

DEF BUFFER waehrung1 FOR waehrung.
DEFINE STREAM s1.

FIND FIRST res-line WHERE RECID(res-line) = recid-resline NO-LOCK.
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.

RUN calc-lodging2.

FUNCTION get-rackrate RETURNS DECIMAL 
    (INPUT erwachs AS INTEGER, 
     INPUT kind1 AS INTEGER, 
     INPUT kind2 AS INTEGER). 
  DEF VAR rate AS DECIMAL INITIAL 0. 
  IF erwachs GE 1 AND erwachs LE 4 THEN 
      rate = rate + katpreis.perspreis[erwachs]. 
  rate = rate + kind1 * katpreis.kindpreis[1] + kind2 * katpreis.kindpreis[2]. 
  RETURN rate. 
END FUNCTION. 

/* START Breakfast lunch Dinner other From Room Rev*/
PROCEDURE calc-lodging2:
    DEF VAR qty AS INTEGER. 
    DEFINE VARIABLE fixed-rate AS LOGICAL INITIAL NO NO-UNDO.
    DEFINE VARIABLE it-exist   AS LOGICAL INITIAL NO NO-UNDO.
    DEFINE VARIABLE rmrate     AS DECIMAL FORMAT ">,>>>,>>>9.99" NO-UNDO.
    DEFINE VARIABLE gpax       AS INTEGER NO-UNDO.
    DEFINE VARIABLE bill-date  AS DATE    NO-UNDO.
    DEFINE VARIABLE ebdisc-flag             AS LOGICAL              NO-UNDO.
    DEFINE VARIABLE kbdisc-flag             AS LOGICAL              NO-UNDO.
    DEFINE VARIABLE rate-found              AS LOGICAL              NO-UNDO.
    DEFINE VARIABLE restricted-disc         AS LOGICAL INITIAL NO   NO-UNDO.
    DEFINE VARIABLE kback-flag              AS LOGICAL              NO-UNDO.
    DEFINE VARIABLE curr-zikatnr            AS INTEGER              NO-UNDO. 
    DEFINE VARIABLE w-day                   AS INTEGER              NO-UNDO. 
    DEFINE VARIABLE rack-rate               AS LOGICAL INITIAL NO   NO-UNDO. 
    DEFINE VARIABLE vat                     AS DECIMAL.
    DEFINE VARIABLE service                 AS DECIMAL.
    DEFINE VARIABLE vat-art                 AS DECIMAL.
    DEFINE VARIABLE service-art             AS DECIMAL.
    DEFINE BUFFER wrung FOR waehrung.

/* start breakfast lunch dinner other */

    DEF VAR qty1            AS INTEGER.
    DEF VAR take-it         AS LOGICAL.
    DEF VAR post-it         AS LOGICAL.
    DEF VAR bfast-art       AS INTEGER.
    DEF VAR fb-dept         AS INTEGER.
    DEF VAR lunch-art       AS INTEGER.
    DEF VAR dinner-art      AS INTEGER.
    DEF VAR lundin-art      AS INTEGER.
    DEF VAR contcode        AS CHAR.
    DEF VAR ct              AS CHAR.
    DEF VAR prcode          AS INTEGER.
    DEF VAR f-betrag        AS DECIMAL.
    DEF VAR argt-betrag     AS DECIMAL.
    DEF VAR fcost           AS DECIMAL.
    DEF VAR fact            AS DECIMAL.
    DEF VAR nett-lamt       AS DECIMAL.
    DEF VAR gross-lamt      AS DECIMAL.
    DEF VAR nett-lserv      AS DECIMAL.
    DEF VAR nett-ltax       AS DECIMAL.
    DEF VAR nett-famt       AS DECIMAL.
    DEF VAR nett-fserv      AS DECIMAL.
    DEF VAR nett-ftax       AS DECIMAL.
    DEF VAR price-decimal   AS INTEGER.
    DEF VAR argtnr          AS CHAR.

    DEFINE BUFFER rguest FOR guest.

    DEF VAR tot-fbreakfast  AS DECIMAL.
    DEF VAR tot-flunch      AS DECIMAL.
    DEF VAR tot-fdinner     AS DECIMAL.
    DEF VAR tot-fother      AS DECIMAL.

    DEF VAR tot-lbreakfast  AS DECIMAL.
    DEF VAR tot-llunch      AS DECIMAL.
    DEF VAR tot-ldinner     AS DECIMAL.
    DEF VAR tot-lother      AS DECIMAL.

    /*DEF VAR nett-service    AS DECIMAL.
    DEF VAR nett-vat        AS DECIMAL.*/

    FIND FIRST htparam WHERE paramnr = 125 NO-LOCK. 
    bfast-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */ 
    FIND FIRST htparam WHERE paramnr = 126 NO-LOCK. 
    fb-dept = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

    FIND FIRST artikel WHERE artikel.zwkum = bfast-art 
      AND artikel.departement = fb-dept NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE artikel AND bfast-art NE 0 THEN 
    DO: 
      hide MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("B'fast SubGrp not yed defined (Grp 7)",lvCAREA,"") 
        VIEW-AS ALERT-BOX INFORMATION. 
      RETURN. 
    END. 

    FIND FIRST htparam WHERE paramnr = 227 NO-LOCK. 
    lunch-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
    FIND FIRST artikel WHERE artikel.zwkum = lunch-art 
      AND artikel.departement = fb-dept NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE artikel AND lunch-art NE 0 THEN 
    DO: 
      hide MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("Lunch SubGrp not yed defined (Grp 7)",lvCAREA,"") 
        VIEW-AS ALERT-BOX INFORMATION. 
      RETURN. 
    END. 

    FIND FIRST htparam WHERE paramnr = 228 NO-LOCK. 
    dinner-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
    FIND FIRST artikel WHERE artikel.zwkum = dinner-art 
      AND artikel.departement = fb-dept NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE artikel AND dinner-art NE 0 THEN 
    DO: 
      hide MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("Dinner SubGrp not yed defined (Grp 7)",lvCAREA,"") 
        VIEW-AS ALERT-BOX INFORMATION. 
      RETURN. 
    END. 

    FIND FIRST htparam WHERE paramnr = 229 NO-LOCK. 
    lundin-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
    FIND FIRST artikel WHERE artikel.zwkum = lundin-art 
      AND artikel.departement = fb-dept NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE artikel AND lundin-art NE 0 THEN 
    DO: 
      hide MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("HalfBoard SubGrp not yed defined (Grp 7)",lvCAREA,"") 
        VIEW-AS ALERT-BOX INFORMATION. 
      RETURN. 
    END. 
/* end breakfast lunch dinner other */

    ASSIGN
        qty1      = res-line.zimmeranz /*FT 041113*/
        rmrate    = res-line.zipreis
        bill-date = datum.
/*      tot-rmrev = tot-rmrev + res-line.zipreis.    */

    FIND FIRST wrung NO-LOCK WHERE wrung.waehrungsnr = res-line.betriebsnr NO-ERROR. 
    IF AVAILABLE wrung THEN exrate = wrung.ankauf / wrung.einheit.
    ELSE exrate = 1.
    
    IF res-line.resstatus = 6 AND res-line.reserve-dec GT 0 THEN 
        frate = reserve-dec.
    ELSE frate = exrate.

    FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr 
        NO-LOCK NO-ERROR.

    FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement
        NO-LOCK NO-ERROR.
    
    FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr 
        AND artikel.departement = 0 NO-LOCK NO-ERROR. 
    service = 0. 
    vat = 0.
    IF AVAILABLE artikel THEN
    DO:
        RUN calc-servvat.p(artikel.departement, artikel.artnr, bill-date,
                           artikel.service-code, artikel.mwst-code,
                           OUTPUT service, OUTPUT vat).
    END.

    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
        AND reslin-queasy.resnr = res-line.resnr 
        AND reslin-queasy.reslinnr = res-line.reslinnr 
        AND datum GE reslin-queasy.date1 
        AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
    IF AVAILABLE reslin-queasy THEN 
    DO:
        fixed-rate = YES.
        rmrate = reslin-queasy.deci1.
        IF reslin-queasy.number3 NE 0 THEN gpax = reslin-queasy.number3.
        IF reslin-queasy.char1 NE "" THEN 
        FIND FIRST arrangement WHERE 
            arrangement.arrangement = reslin-queasy.char1 NO-LOCK. 
        argtnr = arrangement.arrangement.
        /*RUN usr-prog1(datum, INPUT-OUTPUT rmrate, OUTPUT it-exist).*/
    END.
    IF NOT fixed-rate THEN
    DO:
        /*RUN usr-prog1(datum, INPUT-OUTPUT rmrate, OUTPUT it-exist).*/ 
        IF NOT it-exist THEN
        DO:
            IF AVAILABLE guest-pr THEN
            DO:
                FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                      = res-line.reserve-int NO-LOCK NO-ERROR. 
                IF AVAILABLE queasy AND queasy.logi3 THEN 
                     bill-date = res-line.ankunft. 

                IF new-contrate THEN
                    RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, res-line.reslinnr, guest-pr.CODE, 
                      ?, bill-date, res-line.ankunft, res-line.abreise, res-line.reserve-int, argtnr,
                      res-line.zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2, res-line.reserve-dec, 
                      res-line.betriebsnr, OUTPUT rate-found,
                      OUTPUT rmrate, OUTPUT restricted-disc, OUTPUT kback-flag).
                ELSE
                DO:
                    RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                      guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                      res-line.reserve-int, /*arrangement.argtnr*/ argtnr, curr-zikatnr, 
                      res-line.erwachs, res-line.kind1, res-line.kind2,
                      res-line.reserve-dec, res-line.betriebsnr, 
                      OUTPUT rmrate, OUTPUT rate-found).
                      /*RUN usr-prog2(datum, INPUT-OUTPUT rmrate, OUTPUT it-exist).*/
                      IF it-exist THEN rate-found = YES.
                      IF curr-i NE 0 THEN
                          IF NOT it-exist AND bonus-array[curr-i] = YES THEN rmrate = 0.
                END. /* old contrate*/
            END. /* available guest pr*/

            IF NOT rate-found THEN
            DO: 
              w-day = wd-array[WEEKDAY(bill-date)]. 
              IF (bill-date = curr-date) OR (bill-date = res-line.ankunft) THEN 
              DO: 
                rmrate = res-line.zipreis. 
                FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                    AND katpreis.argtnr = arrangement.argtnr 
                    AND katpreis.startperiode LE bill-date 
                    AND katpreis.endperiode GE bill-date 
                    AND katpreis.betriebsnr = w-day 
                    NO-LOCK NO-ERROR. 
                IF NOT AVAILABLE katpreis THEN 
                FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                    AND katpreis.argtnr = arrangement.argtnr 
                    AND katpreis.startperiode LE bill-date 
                    AND katpreis.endperiode GE bill-date 
                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                    res-line.kind1, res-line.kind2) = rmrate 
                THEN rack-rate = YES. 
              END. 
              ELSE IF rack-rate THEN 
              DO: 
                FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                    AND katpreis.argtnr = arrangement.argtnr 
                    AND katpreis.startperiode LE bill-date 
                    AND katpreis.endperiode GE bill-date 
                    AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
                IF NOT AVAILABLE katpreis THEN 
                FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                    AND katpreis.argtnr = arrangement.argtnr 
                    AND katpreis.startperiode LE bill-date 
                    AND katpreis.endperiode GE bill-date 
                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                    res-line.kind1, res-line.kind2) > 0 
                THEN 
                  rmrate = get-rackrate(res-line.erwachs, 
                    res-line.kind1, res-line.kind2). 
              END. /* if rack-rate   */ 
              IF curr-i NE 0 THEN
                  IF bonus-array[curr-i] = YES THEN rmrate = 0.  
            END.   /* publish rate   */  
        END. /*Not it-exist*/
    END. /*Not fix-rate*/
    
    ASSIGN tot-rmrev = rmrate. /* room rate for date = datum */
   
    
    /* start argt-line breakfast lunch dinner other */
    contcode = "".
    FIND FIRST rguest WHERE rguest.gastnr = res-line.gastnr NO-LOCK. 
    IF res-line.reserve-int NE 0 THEN /* MarkNr -> contract rate exists */ 
      FIND FIRST guest-pr WHERE guest-pr.gastnr = rguest.gastnr 
        NO-LOCK NO-ERROR. 
    IF AVAILABLE guest-pr THEN 
    DO: 
      contcode = guest-pr.CODE.
      ct = res-line.zimmer-wunsch.
      IF ct MATCHES("*$CODE$*") THEN
      DO:
        ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
        contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
      END.
      IF new-contrate THEN RUN ratecode-seek.p(res-line.resnr, 
        res-line.reslinnr, contcode, datum /*curr-date*/, OUTPUT prcode).
      ELSE
      DO:
        FIND FIRST pricecod WHERE pricecod.code = contcode 
          AND pricecod.marknr = res-line.reserve-int 
          AND pricecod.argtnr = arrangement.argtnr 
          AND pricecod.zikatnr = curr-zikatnr 
          AND datum /*curr-date*/ GE pricecod.startperiode 
          AND datum /*curr-date*/ LE pricecod.endperiode NO-LOCK NO-ERROR. 
        IF AVAILABLE pricecod THEN prcode = RECID(pricecod). 
      END.
    END.  

    gross-lamt = 0.
    
    IF argtnr = "" THEN argtnr = res-line.arrangement.
    FIND FIRST arrangement WHERE arrangement.arrangement = argtnr
        NO-LOCK NO-ERROR.
    FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
        AND NOT argt-line.kind2
        AND argt-line.kind1,
        FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
            AND artikel.departement = argt-line.departement NO-LOCK: 
        RUN get-argtline-rate(datum, contcode, RECID(argt-line), OUTPUT take-it,
                              OUTPUT f-betrag, OUTPUT argt-betrag, OUTPUT qty).
        
        service-art = 0. 
        vat-art = 0.
        
        RUN calc-servvat.p(artikel.departement, artikel.artnr, bill-date,
                           artikel.service-code, artikel.mwst-code,
                           OUTPUT service-art, OUTPUT vat-art).


        IF take-it THEN 
        DO: 
            ASSIGN
                nett-lamt = ((argt-betrag )  * qty1)
                /*nett-lserv = ROUND(nett-lamt * service, price-decimal)
                nett-ltax =  ROUND(nett-lamt * vat, price-decimal)
                nett-lamt = ((argt-betrag )  * qty1) - nett-lserv - nett-ltax FT 280513*/
                gross-lamt =  gross-lamt + ((argt-betrag )  * qty1)
                nett-lamt = nett-lamt / (1 + service-art + vat-art )

                nett-famt = ((argt-betrag) * frate) * qty1
                /*nett-fserv = ROUND(nett-famt * service, price-decimal)
                nett-ftax =  ROUND(nett-famt * vat, price-decimal)
                nett-famt = (((argt-betrag) * frate) * qty1) - nett-fserv - nett-ftax FT 280513*/
                nett-famt = nett-famt / (1 + service-art + vat-art ).
          
          done = NO.
          IF commision NE "" THEN
          DO j = 1 TO NUM-ENTRIES(commision,";"):
            ex-article = ENTRY(j, commision, ";").
            IF artikel.artnr = INT(ENTRY(1, ex-article, "-"))
                AND artikel.departement = INT(ENTRY(2, ex-article, "-")) THEN
                    ASSIGN
                    done = YES
                    net-commision = net-commision + nett-lamt * frate.
          END.
          IF payable NE "" AND done EQ NO THEN
          DO j = 1 TO NUM-ENTRIES(payable,";"):
                ex-article = ENTRY(j, payable, ";").
                IF artikel.artnr = INT(ENTRY(1, ex-article, "-"))
                    AND artikel.departement = INT(ENTRY(2, ex-article, "-")) THEN
                        ASSIGN
                        done = YES
                        net-payable = net-payable + nett-lamt * frate.
          END.
          
          IF NOT done THEN
          DO:              
              IF banquet-dept NE "" AND artikel.departement = INT(banquet-dept) THEN
              DO:
                  net-banquet = net-banquet + nett-lamt * frate.
              END.          
              ELSE IF artikel.umsatzart = 3 OR artikel.umsatzart GE 5 THEN 
              DO:
                  ASSIGN
                      tot-lbreakfast = tot-lbreakfast + nett-lamt * frate
                      tot-fbreakfast = tot-fbreakfast + nett-famt.
              END.               
              ELSE 
              DO: 
                  ASSIGN
                      tot-lother = tot-lother + nett-lamt * frate
                      tot-fother = tot-fother + nett-famt.
              END.
          END.
      END.
    END.

    FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
        AND fixleist.reslinnr = res-line.reslinnr NO-LOCK: 
        RUN check-fixleist-posted(datum , fixleist.artnr, fixleist.departement, 
          fixleist.sequenz, fixleist.dekade, 
          fixleist.lfakt, OUTPUT post-it). 
        ASSIGN
            service-art = 0
            vat-art = 0.

        IF post-it THEN 
        DO: 
          
            FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr 
              AND artikel.departement = fixleist.departement NO-LOCK NO-ERROR.
            IF AVAILABLE artikel THEN
            DO:
              RUN calc-servvat.p(artikel.departement, artikel.artnr, bill-date,
                                 artikel.service-code, artikel.mwst-code,
                                 OUTPUT service-art, OUTPUT vat-art).
            END.

            ASSIGN
                fcost = fixleist.betrag * fixleist.number
                fcost = fcost / (1 + service-art + vat-art).
            
            done = NO.
            IF commision NE "" THEN
            DO j = 1 TO NUM-ENTRIES(commision,";"):
            ex-article = ENTRY(j, commision, ";").
            IF artikel.artnr = INT(ENTRY(1, ex-article, "-"))
                AND artikel.departement = INT(ENTRY(2, ex-article, "-")) THEN
                    ASSIGN
                    done = YES
                    net-commision = net-commision + fcost * frate.
            END.
            IF payable NE "" AND done EQ NO THEN
            DO j = 1 TO NUM-ENTRIES(payable,";"):
                ex-article = ENTRY(j, payable, ";").
                IF artikel.artnr = INT(ENTRY(1, ex-article, "-"))
                    AND artikel.departement = INT(ENTRY(2, ex-article, "-")) THEN
                        ASSIGN
                        done = YES
                        net-payable = net-payable + fcost * frate.
            END.

            IF NOT done THEN
            DO:                
                IF banquet-dept NE "" AND artikel.departement = int(banquet-dept) THEN
                DO:
                    net-banquet = net-banquet + fcost * frate.
                END.   
                ELSE IF artikel.umsatzart = 3 OR artikel.umsatzart GE 5 THEN
                DO:
                    ASSIGN
                        tot-lbreakfast = tot-lbreakfast + fcost * frate
                        tot-fbreakfast = tot-fbreakfast + fcost. 
                END.
                ELSE
                DO:
                    ASSIGN
                        tot-lother = tot-lother + fcost * frate
                        tot-fother = tot-fother + fcost.
                END.
            END.
        END. 
    END.
    /* end argt-line breakfast lunch dinner other */
    rmrate = rmrate * qty1.
    FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK. 
    rm-vat = htparam.flogical. 

    IF rm-vat THEN /* room rate includes Tax [and service] */
    ASSIGN
        rmrate = rmrate - gross-lamt
        nett-rmrev   = rmrate / (1 + vat + service)
        nett-service = nett-rmrev * service 
        nett-vat     = nett-rmrev * vat 
    .
    ELSE
    ASSIGN
        rmrate = rmrate - nett-lamt
        nett-rmrev   = rmrate
        nett-service = rmrate * service 
        nett-vat     = rmrate * vat 
        tot-rmrev    = rmrate + nett-service + nett-vat
        
    .
    
    ASSIGN
        net-breakfast  = tot-lbreakfast
        net-lunch      = tot-llunch
        net-dinner     = tot-ldinner
        net-others     = tot-lother.
    
    IF rmrate NE 0 THEN
    DO:
        RUN get-lodging(argtnr, rmrate, bill-date, OUTPUT Fnet-lodging,
                        OUTPUT Lnet-lodging).

        IF rm-vat THEN /* room rate includes Tax [and service] */
            ASSIGN
                Fnet-lodging = Fnet-lodging / (1 + vat + service)
                Lnet-lodging = Lnet-lodging / (1 + vat + service).
        
            /*Lnet-lodging = Lnet-lodging - net-breakfast - net-lunch - net-dinner - net-others.*/

    END.
    ELSE 
        ASSIGN
            Lnet-lodging = 0
            Fnet-lodging = 0.
END.

PROCEDURE get-argtline-rate: 
DEFINE INPUT PARAMETER curr-date AS DATE.
DEFINE INPUT PARAMETER contcode AS CHAR. 
DEFINE INPUT PARAMETER argt-recid AS INTEGER. 
DEFINE OUTPUT PARAMETER add-it AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER f-betrag AS DECIMAL. 
DEFINE OUTPUT PARAMETER argt-betrag AS DECIMAL INITIAL 0. 
DEFINE OUTPUT PARAMETER qty AS INTEGER INITIAL 0. 
 
DEFINE VARIABLE curr-zikatnr AS INTEGER NO-UNDO. 
DEFINE BUFFER argtline FOR argt-line. 
 
  IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
  ELSE curr-zikatnr = res-line.zikatnr. 
 
  FIND FIRST argtline WHERE RECID(argtline) = argt-recid NO-LOCK. 
  IF argt-line.vt-percnt = 0 THEN 
  DO: 
    IF argt-line.betriebsnr = 0 THEN qty = res-line.erwachs. 
    ELSE qty = argt-line.betriebsnr. 
  END. 
  ELSE IF argt-line.vt-percnt = 1 THEN qty = res-line.kind1. 
  ELSE IF argt-line.vt-percnt = 2 THEN qty = res-line.kind2. 
  IF qty GT 0 THEN 
  DO: 
    IF argtline.fakt-modus = 1 THEN add-it = YES. 
    ELSE IF argtline.fakt-modus = 2 THEN 
    DO: 
      IF res-line.ankunft EQ curr-date THEN add-it = YES. 
    END. 
    ELSE IF argtline.fakt-modus = 3 THEN 
    DO: 
      IF (res-line.ankunft + 1) EQ curr-date THEN add-it = YES. 
    END. 
    ELSE IF argtline.fakt-modus = 4 
      AND day(curr-date) = 1 THEN add-it = YES. 
    ELSE IF argtline.fakt-modus = 5 
      AND day(curr-date + 1) = 1 THEN add-it = YES. 
    ELSE IF argtline.fakt-modus = 6 THEN 
    DO: 
      IF (res-line.ankunft + (argtline.intervall - 1)) GE curr-date 
      THEN add-it = YES. 
    END. 
  END. 

  IF add-it THEN 
  DO: 
    FIND FIRST reslin-queasy WHERE key = "fargt-line" 
        AND reslin-queasy.char1 = "" 
        AND reslin-queasy.resnr = res-line.resnr 
        AND reslin-queasy.reslinnr = res-line.reslinnr 
        AND reslin-queasy.number1 = argtline.departement 
        AND reslin-queasy.number2 =  argtline.argtnr 
        AND reslin-queasy.number3 = argtline.argt-artnr 
        AND curr-date GE reslin-queasy.date1 
        AND curr-date LE reslin-queasy.date2 
        USE-INDEX argt1_ix NO-LOCK NO-ERROR. 
    IF AVAILABLE reslin-queasy THEN 
    DO: 
      argt-betrag = reslin-queasy.deci1 * qty. 
      f-betrag = argt-betrag. 
      FIND FIRST waehrung WHERE RECID(waehrung) = RECID(waehrung1) NO-LOCK NO-ERROR. 
      IF argt-betrag = 0 THEN add-it = NO. 
      RETURN. 
    END. 

    IF contcode NE "" THEN 
    DO: 
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
        AND reslin-queasy.char1 = contcode 
        AND reslin-queasy.number1 = res-line.reserve-int 
        AND reslin-queasy.number2 = arrangement.argtnr 
        AND reslin-queasy.number3 = argtline.argt-artnr 
        AND reslin-queasy.resnr = argtline.departement 
        AND reslin-queasy.reslinnr = curr-zikatnr 
        AND curr-date GE reslin-queasy.date1 
        AND curr-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN 
      DO: 
        argt-betrag = reslin-queasy.deci1 * qty. 
        f-betrag = argt-betrag. 
        
        FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR.
        FIND FIRST waehrung WHERE RECID(waehrung) = RECID(waehrung1) NO-LOCK NO-ERROR. 
        IF argt-betrag = 0 THEN add-it = NO. 
        RETURN. 
      END. 
    END. 
    argt-betrag = argt-line.betrag. 
    FIND FIRST arrangement WHERE arrangement.argtnr = argt-line.argtnr 
      NO-LOCK. 
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = arrangement.betriebsnr 
      NO-LOCK NO-ERROR. 
    f-betrag = argt-betrag * qty. 
    
    IF res-line.betriebsnr NE arrangement.betriebsnr THEN 
      argt-betrag = argt-betrag * (waehrung.ankauf / waehrung.einheit) / frate. 
    argt-betrag = argt-betrag * qty. 
    IF argt-betrag = 0 THEN add-it = NO. 
  END.
END. 

PROCEDURE check-fixleist-posted: 
DEFINE INPUT PARAMETER curr-date AS DATE.
DEFINE INPUT PARAMETER artnr AS INTEGER. 
DEFINE INPUT PARAMETER dept AS INTEGER. 
DEFINE INPUT PARAMETER fakt-modus AS INTEGER. 
DEFINE INPUT PARAMETER intervall AS INTEGER. 
DEFINE INPUT PARAMETER lfakt AS DATE. 
DEFINE OUTPUT PARAMETER post-it AS LOGICAL INITIAL NO. 
DEFINE VARIABLE delta AS INTEGER. 
DEFINE VARIABLE start-date AS DATE. 
 
  IF fakt-modus = 1 THEN post-it = YES. 
  ELSE IF fakt-modus = 2 THEN 
  DO: 
    IF res-line.ankunft = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 3 THEN 
  DO: 
    IF (res-line.ankunft + 1) = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 4 THEN   /* 1st day OF month  */ 
  DO: 
    IF day(curr-date) EQ 1 THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 5 THEN   /* LAST day OF month */ 
  DO: 
    IF day(curr-date + 1) EQ 1 THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 6 THEN 
  DO: 
    IF lfakt = ? THEN delta = 0. 
    ELSE 
    DO: 
      delta = lfakt - res-line.ankunft. 
      IF delta LT 0 THEN delta = 0. 
    END. 
    start-date = res-line.ankunft + delta. 
    IF (res-line.abreise - start-date) LT intervall 
      THEN start-date = res-line.ankunft. 
    IF curr-date LE (start-date + (intervall - 1)) 
    THEN post-it = YES. 
    IF curr-date LT start-date THEN post-it = no. /* may NOT post !! */ 
  END. 
END. 

PROCEDURE get-lodging:
DEFINE INPUT PARAMETER argtnr AS CHAR.
DEFINE INPUT PARAMETER zipreis AS DECIMAL.
DEFINE INPUT PARAMETER bill-date AS DATE. 
DEFINE OUTPUT PARAMETER Flodg-betrag AS DECIMAL. 
DEFINE OUTPUT PARAMETER Llodg-betrag AS DECIMAL. 
DEFINE VARIABLE service AS DECIMAL. 
DEFINE VARIABLE vat AS DECIMAL. 
DEFINE VARIABLE qty AS INTEGER. 
DEFINE VARIABLE argt-betrag AS DECIMAL. 
DEFINE VARIABLE fargt-betrag AS DECIMAL. 
DEFINE VARIABLE add-it AS LOGICAL. 
DEFINE VARIABLE marknr AS INTEGER. 
  IF argtnr = "" THEN argtnr = res-line.arrangement.
  FIND FIRST arrangement WHERE arrangement.arrangement 
    = /*MTres-line.arrangement*/ argtnr NO-LOCK. 
  FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr 
    AND artikel.departement = 0 NO-LOCK NO-ERROR. 
  service = 0. 
  vat = 0. 
  IF AVAILABLE artikel THEN
  DO:
    FIND FIRST htparam WHERE htparam.paramnr = artikel.service-code 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
      service = htparam.fdecimal / 100. 
    FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    vat = htparam.fdecimal / 100. 
    FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
    IF htparam.flogical THEN vat = vat + vat * service. 
    vat = round(vat, 2).
  END. 
 
  Flodg-betrag = zipreis.
  Llodg-betrag = zipreis * frate.
  /*FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
      AND NOT argt-line.kind2 
      AND argt-line.kind1
      NO-LOCK: 
      FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
        AND artikel.departement = argt-line.departement NO-LOCK. 
      argt-betrag = 0. 
      add-it = NO. 

      RUN argt-betrag.p(RECID(res-line), RECID(argt-line), 
                        OUTPUT argt-betrag, OUTPUT frate).

      fargt-betrag = ROUND(argt-betrag, price-decimal). /*FT 041113*/
      argt-betrag = ROUND(argt-betrag * frate, price-decimal).

      Llodg-betrag = Llodg-betrag - argt-betrag.
      Flodg-betrag = Flodg-betrag - fargt-betrag.
  END. */
  Llodg-betrag = round(Llodg-betrag, price-decimal).
  Flodg-betrag = round(Flodg-betrag, price-decimal).
END. 

/* END Breakfast lunch Dinner other From Room Rev*/
/*
PROCEDURE usr-prog1: 
DEFINE INPUT PARAMETER bill-date AS DATE. 
DEFINE INPUT-OUTPUT PARAMETER roomrate AS DECIMAL. 
DEFINE OUTPUT PARAMETER it-exist AS LOGICAL INITIAL NO. 
DEFINE VARIABLE prog-str AS CHAR INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "rate-prog" 
    AND reslin-queasy.number1 = resnr 
    AND reslin-queasy.number2 = 0 AND reslin-queasy.char1 = "" 
    AND reslin-queasy.reslinnr = 1 USE-INDEX argt_ix NO-LOCK NO-ERROR. 
  IF AVAILABLE reslin-queasy THEN prog-str = reslin-queasy.char3. 
  IF prog-str NE "" THEN 
  DO: 
    OUTPUT STREAM s1 TO ".\_rate.p". 
    DO i = 1 TO length(prog-str): 
      PUT STREAM s1 SUBSTR(prog-str, i, 1) FORMAT "x(1)". 
    END. 
    OUTPUT STREAM s1 CLOSE. 
    compile value(".\_rate.p"). 
    dos silent "del .\_rate.p". 
    IF NOT compiler:ERROR THEN 
    DO: 
      RUN value(".\_rate.p") (0, res-line.resnr, res-line.reslinnr, 
      bill-date, roomrate, NO, OUTPUT roomrate). 
      it-exist = YES. 
    END. 
  END. 
END. 
 
PROCEDURE usr-prog2: 
DEFINE INPUT PARAMETER bill-date AS DATE. 
DEFINE INPUT-OUTPUT PARAMETER roomrate AS DECIMAL. 
DEFINE OUTPUT PARAMETER it-exist AS LOGICAL INITIAL NO. 
DEFINE VARIABLE prog-str AS CHAR INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
  FIND FIRST queasy WHERE queasy.key = 2 
    AND queasy.char1 = guest-pr.code NO-LOCK NO-ERROR. 
  IF AVAILABLE queasy THEN prog-str = queasy.char3. 
  IF prog-str NE "" THEN 
  DO: 
    OUTPUT STREAM s1 TO ".\_rate.p". 
    DO i = 1 TO length(prog-str): 
      PUT STREAM s1 SUBSTR(prog-str, i, 1) FORMAT "x(1)". 
    END. 
    OUTPUT STREAM s1 CLOSE. 
    compile value(".\_rate.p"). 
    dos silent "del .\_rate.p". 
    IF NOT compiler:ERROR THEN 
    DO: 
      RUN value(".\_rate.p") (0, res-line.resnr, res-line.reslinnr, 
      bill-date, roomrate, NO, OUTPUT roomrate). 
      it-exist = YES. 
    END. 
  END. 
END. */

