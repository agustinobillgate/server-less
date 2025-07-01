DEFINE TEMP-TABLE output-list
  FIELD rmNo        AS CHAR
  FIELD flag        AS CHAR
  FIELD STR         AS CHAR
  FIELD rmno1       AS CHAR
  FIELD rmtype      AS CHAR
  FIELD rm          AS INTEGER
  FIELD pax         AS INTEGER
  FIELD rm-rev      AS DECIMAL 
  FIELD percent     AS DECIMAL 
  FIELD mtdrm       AS INTEGER
  FIELD pax1        AS INTEGER
  FIELD rm-rev1     AS DECIMAL 
  FIELD percent1    AS DECIMAL
  FIELD ftdrm       AS INTEGER
  FIELD pax2        AS INTEGER
  FIELD rm-rev2     AS DECIMAL 
  FIELD percent3    AS DECIMAL 
.

DEFINE TEMP-TABLE cl-list 
  FIELD flag       AS CHAR 
  FIELD zinr       LIKE zimmer.zinr /*MT 24/07/12 */
  FIELD rmcat      AS CHAR FORMAT "x(6)" 
  FIELD anz        AS INTEGER FORMAT ">>9" 
  FIELD pax        AS INTEGER FORMAT ">>9"
  FIELD net        AS DECIMAL FORMAT "->>>,>>>,>>9.99"
  FIELD proz       AS DECIMAL FORMAT "->>9.99"
  FIELD manz       AS INTEGER FORMAT /*">>,>>9"*/  ">>>>9"
  FIELD mpax       AS INTEGER FORMAT ">>,>>9" 
  FIELD mnet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz1      AS DECIMAL FORMAT "->>9.99" INITIAL 0 
  FIELD yanz       AS INTEGER FORMAT ">>>,>>9"
  FIELD ypax       AS INTEGER FORMAT ">>>,>>9" 
  FIELD ynet       AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0 
  FIELD proz2      AS DECIMAL FORMAT "->>9.99" INITIAL 0. 

DEFINE INPUT  PARAMETER m-ftd        AS LOGICAL. 
DEFINE INPUT  PARAMETER m-ytd        AS LOGICAL. 
DEFINE INPUT  PARAMETER f-date       AS DATE.
DEFINE INPUT  PARAMETER t-date       AS DATE.
DEFINE INPUT  PARAMETER to-date      AS DATE.
DEFINE INPUT  PARAMETER rm-no        AS CHAR.
DEFINE INPUT  PARAMETER sorttype     AS INTEGER.
DEFINE INPUT  PARAMETER lod_rev      AS LOGICAL.
DEFINE INPUT  PARAMETER excl-compl   AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.


DEFINE VARIABLE i                   AS INTEGER. 
DEFINE VARIABLE anz                 AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE manz                AS INTEGER FORMAT /*">>,>>9"*/ ">>>>9".
DEFINE VARIABLE yanz                AS INTEGER FORMAT ">>>,>>9". 
DEFINE VARIABLE pax                 AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mpax                AS INTEGER FORMAT ">>,>>9". 
DEFINE VARIABLE ypax                AS INTEGER FORMAT ">>>,>>9". 
DEFINE VARIABLE mnet                AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEFINE VARIABLE ynet                AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEFINE VARIABLE net                 AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEFINE VARIABLE t-anz               AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE t-manz              AS INTEGER FORMAT ">>,>>9". 
DEFINE VARIABLE t-yanz              AS INTEGER FORMAT /*">>>,>>9"*/ ">>>>9".
DEFINE VARIABLE t-pax               AS INTEGER FORMAT ">>,>>9". 
DEFINE VARIABLE t-mpax              AS INTEGER FORMAT ">>,>>9". 
DEFINE VARIABLE t-ypax              AS INTEGER FORMAT ">>>,>>9". 
DEFINE VARIABLE t-net               AS DECIMAL FORMAT "->>,>>>,>>9.99". 
DEFINE VARIABLE t-mnet              AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEFINE VARIABLE t-ynet              AS DECIMAL FORMAT "->>>,>>>,>>9.99". 
DEFINE VARIABLE from-bez            AS CHAR FORMAT "x(22)". 
DEFINE VARIABLE to-bez              AS CHAR FORMAT "x(22)". 
DEFINE VARIABLE price-decimal       AS INTEGER. 
DEFINE VARIABLE from-date           AS DATE LABEL "F&rom Date". 
/*DEFINE VARIABLE to-date             AS DATE LABEL "To &Date". */
DEFINE VARIABLE curr-zeit           AS INTEGER.

DEFINE VARIABLE ci-date             AS DATE. 
DEFINE VARIABLE do-it               AS LOGICAL.

RUN htpdate.p(87, OUTPUT ci-date).

IF m-ftd AND f-date GE ci-date AND t-date GE ci-date THEN /*FDL June 10, 2024 => Ticket 23EAEE*/
DO:
    RUN create-resline.
END.
ELSE 
DO:
    IF lod_rev = YES THEN RUN create-genstat. 
    ELSE RUN create-zinrstat.
END.

/************************* PROCEDURE **********************/
PROCEDURE create-resline:
    DEFINE VARIABLE datum               AS DATE.
    DEFINE VARIABLE s-datum             AS DATE.
    DEFINE VARIABLE e-datum             AS DATE.
    DEFINE VARIABLE amount-rmrev        AS DECIMAL.
    DEFINE VARIABLE amount-rmargt       AS DECIMAL.
    DEFINE VARIABLE frate               AS DECIMAL INITIAL 1.
    DEFINE VARIABLE price-decimal       AS INTEGER.
    DEFINE VARIABLE argt-betrag         AS DECIMAL.
    DEFINE VARIABLE ex-rate             AS DECIMAL. 
    DEFINE VARIABLE last-zikatnr        AS INTEGER INITIAL 0.
    DEFINE VARIABLE found-zikatnr       AS LOGICAL.
    DEFINE VARIABLE count-k             AS INTEGER INITIAL 0.
    DEFINE VARIABLE last-zinr           AS CHARACTER.
    DEFINE VARIABLE last-rmtype         AS CHARACTER.

    FIND FIRST htparam WHERE htparam.paramnr EQ 491 NO-LOCK. 
    price-decimal = htparam.finteger.

    IF rm-no NE "" THEN
    DO:
        CREATE cl-list. 
        cl-list.zinr = rm-no. 
        FIND FIRST zimmer WHERE zimmer.zinr EQ rm-no NO-LOCK NO-ERROR.
        IF AVAILABLE zimmer THEN cl-list.rmcat = zimmer.kbezeich.

        FOR EACH res-line WHERE (res-line.active-flag LE 1 
            AND res-line.resstatus NE 12
            AND res-line.resstatus LE 13
            AND res-line.resstatus NE 4
            AND NOT (res-line.ankunft GT t-date) 
            AND NOT (res-line.abreise LT f-date))
            AND res-line.l-zuordnung[3] = 0
            AND res-line.zinr EQ rm-no
            AND res-line.zipreis NE 0 NO-LOCK,
            FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK,
            FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK,
            FIRST zimmer WHERE zimmer.zinr EQ res-line.zinr 
            NO-LOCK BY res-line.zinr:
    
            amount-rmrev    = 0.
            amount-rmargt   = 0.

            IF res-line.reserve-dec NE 0 THEN frate = res-line.reserve-dec. 
            ELSE 
            DO: 
                FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                IF AVAILABLE waehrung THEN frate = waehrung.ankauf / waehrung.einheit. 
            END. 

            IF res-line.ankunft GE f-date THEN s-datum = res-line.ankunft. 
            ELSE s-datum = f-date.
            IF res-line.abreise LE t-date THEN e-datum = res-line.abreise - 1.
            ELSE e-datum = t-date.                                   

            /*FDL Nov 08, 2024: Ticket 064FE3*/
            do-it = YES.
            IF excl-compl THEN
            DO:  
                FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode
                     AND (segment.betriebsnr EQ 1 OR segment.betriebsnr EQ 2) NO-LOCK NO-ERROR.
                IF AVAILABLE segment THEN do-it = NO.
            END.

            IF do-it THEN
            DO:
                DO datum = s-datum TO e-datum:
                    amount-rmrev    = res-line.zipreis * frate.
                    amount-rmargt   = ROUND(res-line.zipreis * frate, price-decimal).
                        
                    FOR EACH argt-line WHERE argt-line.argtnr EQ arrangement.argtnr 
                        AND NOT argt-line.kind2 NO-LOCK: 
                        FIND FIRST artikel WHERE artikel.artnr EQ argt-line.argt-artnr 
                            AND artikel.departement EQ argt-line.departement NO-LOCK. 
                        RUN argt-betrag.p(RECID(res-line), RECID(argt-line), 
                            OUTPUT argt-betrag, OUTPUT ex-rate). 
    
                        amount-rmrev = amount-rmrev - argt-betrag * ex-rate. 
                    END. 
                    amount-rmrev = ROUND(amount-rmrev, price-decimal). 
    
                    IF datum EQ e-datum THEN
                    DO:
                        cl-list.anz = cl-list.anz + res-line.zimmeranz.
                        cl-list.pax = cl-list.pax + res-line.erwachs + res-line.gratis +
                                    res-line.kind1 + res-line.kind2.
                        anz         = anz + res-line.zimmeranz. 
                        pax         = pax + res-line.erwachs + res-line.gratis +
                                    res-line.kind1 + res-line.kind2.
    
                        IF lod_rev THEN 
                        DO:
                            cl-list.net = cl-list.net + amount-rmrev.
                            net = net + amount-rmrev.
                        END.
                        ELSE 
                        DO:
                            cl-list.net = cl-list.net + amount-rmargt.
                            net = net + amount-rmargt.
                        END.                    
                    END.
                    cl-list.manz = cl-list.manz + res-line.zimmeranz.
                    cl-list.mpax = cl-list.mpax + res-line.erwachs + res-line.gratis +
                                res-line.kind1 + res-line.kind2.
                    manz         = manz + res-line.zimmeranz. 
                    mpax         = mpax + res-line.erwachs + res-line.gratis +
                                res-line.kind1 + res-line.kind2.
    
                    IF lod_rev THEN 
                    DO:
                        cl-list.mnet = cl-list.mnet + amount-rmrev.
                        mnet = mnet + amount-rmrev.
                    END.
                    ELSE 
                    DO:
                        cl-list.mnet = cl-list.mnet + amount-rmargt.
                        mnet = mnet + amount-rmargt.
                    END. 
                END.
            END.            
        END.
    END.
    ELSE
    DO:
        IF sorttype EQ 1 THEN
        DO:
            FOR EACH res-line WHERE (res-line.active-flag LE 1 
                AND res-line.resstatus NE 12
                AND res-line.resstatus LE 13
                AND res-line.resstatus NE 4
                AND NOT (res-line.ankunft GT t-date) 
                AND NOT (res-line.abreise LT f-date))
                AND res-line.l-zuordnung[3] = 0
                AND res-line.zinr NE ""
                AND res-line.zipreis NE 0 NO-LOCK,
                FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK,
                FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK,
                FIRST zimmer WHERE zimmer.zinr EQ res-line.zinr 
                NO-LOCK BY res-line.zinr:
        
                amount-rmrev    = 0.
                amount-rmargt   = 0.
    
                IF res-line.reserve-dec NE 0 THEN frate = res-line.reserve-dec. 
                ELSE 
                DO: 
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                    IF AVAILABLE waehrung THEN frate = waehrung.ankauf / waehrung.einheit. 
                END. 
    
                IF res-line.ankunft GE f-date THEN s-datum = res-line.ankunft. 
                ELSE s-datum = f-date.
                IF res-line.abreise LE t-date THEN e-datum = res-line.abreise - 1.
                ELSE e-datum = t-date.                                   
    
                FIND FIRST cl-list WHERE cl-list.zinr EQ res-line.zinr
                    AND cl-list.rmcat EQ zimmer.kbezeich NO-LOCK NO-ERROR.
                IF NOT AVAILABLE cl-list THEN
                DO:
                    CREATE cl-list.
                    cl-list.zinr = res-line.zinr.
                    cl-list.rmcat = zimmer.kbezeich.
                END.

                /*FDL Nov 08, 2024: Ticket 064FE3*/
                do-it = YES.
                IF excl-compl THEN
                DO:  
                    FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode
                         AND (segment.betriebsnr EQ 1 OR segment.betriebsnr EQ 2) NO-LOCK NO-ERROR.
                    IF AVAILABLE segment THEN do-it = NO.
                END.

                IF do-it THEN
                DO:
                    DO datum = s-datum TO e-datum:
                        amount-rmrev    = res-line.zipreis * frate.
                        amount-rmargt   = ROUND(res-line.zipreis * frate, price-decimal).
                            
                        FOR EACH argt-line WHERE argt-line.argtnr EQ arrangement.argtnr 
                            AND NOT argt-line.kind2 NO-LOCK: 
                            FIND FIRST artikel WHERE artikel.artnr EQ argt-line.argt-artnr 
                                AND artikel.departement EQ argt-line.departement NO-LOCK. 
                            RUN argt-betrag.p(RECID(res-line), RECID(argt-line), 
                                OUTPUT argt-betrag, OUTPUT ex-rate). 
        
                            amount-rmrev = amount-rmrev - argt-betrag * ex-rate. 
                        END. 
                        amount-rmrev = ROUND(amount-rmrev, price-decimal). 
        
                        IF datum EQ e-datum THEN
                        DO:
                            cl-list.anz = cl-list.anz + res-line.zimmeranz.
                            cl-list.pax = cl-list.pax + res-line.erwachs + res-line.gratis +
                                        res-line.kind1 + res-line.kind2.
                            anz         = anz + res-line.zimmeranz. 
                            pax         = pax + res-line.erwachs + res-line.gratis +
                                        res-line.kind1 + res-line.kind2.
        
                            IF lod_rev THEN 
                            DO:
                                cl-list.net = cl-list.net + amount-rmrev.
                                net = net + amount-rmrev.
                            END.
                            ELSE 
                            DO:
                                cl-list.net = cl-list.net + amount-rmargt.
                                net = net + amount-rmargt.
                            END.                    
                        END.
                        cl-list.manz = cl-list.manz + res-line.zimmeranz.
                        cl-list.mpax = cl-list.mpax + res-line.erwachs + res-line.gratis +
                                    res-line.kind1 + res-line.kind2.
                        manz         = manz + res-line.zimmeranz. 
                        mpax         = mpax + res-line.erwachs + res-line.gratis +
                                    res-line.kind1 + res-line.kind2.
        
                        IF lod_rev THEN 
                        DO:
                            cl-list.mnet = cl-list.mnet + amount-rmrev.
                            mnet = mnet + amount-rmrev.
                        END.
                        ELSE 
                        DO:
                            cl-list.mnet = cl-list.mnet + amount-rmargt.
                            mnet = mnet + amount-rmargt.
                        END. 
                    END.
                END.                
            END.
        END.
        ELSE IF sorttype EQ 2 THEN
        DO:
            FOR EACH res-line WHERE (res-line.active-flag LE 1 
                AND res-line.resstatus NE 12
                AND res-line.resstatus LE 13
                AND res-line.resstatus NE 4
                AND NOT (res-line.ankunft GT t-date) 
                AND NOT (res-line.abreise LT f-date))
                AND res-line.l-zuordnung[3] = 0
                AND res-line.zinr NE ""
                AND res-line.zipreis NE 0 NO-LOCK,
                FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK,
                FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK,
                FIRST zimmer WHERE zimmer.zinr EQ res-line.zinr 
                NO-LOCK BY res-line.zikatnr BY res-line.zinr:
        
                amount-rmrev    = 0.
                amount-rmargt   = 0.
    
                IF res-line.reserve-dec NE 0 THEN frate = res-line.reserve-dec. 
                ELSE 
                DO: 
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                    IF AVAILABLE waehrung THEN frate = waehrung.ankauf / waehrung.einheit. 
                END. 
    
                IF res-line.ankunft GE f-date THEN s-datum = res-line.ankunft. 
                ELSE s-datum = f-date.
                IF res-line.abreise LE t-date THEN e-datum = res-line.abreise - 1.
                ELSE e-datum = t-date.                                   
                
                IF last-zikatnr NE res-line.zikatnr OR last-zinr NE res-line.zinr THEN
                DO:
                    count-k = count-k + 1.
                    IF count-k GT 1 AND last-zikatnr NE res-line.zikatnr THEN
                    DO:
                        CREATE cl-list.
                        ASSIGN
                            cl-list.flag  = "*"
                            cl-list.rmcat = "Total"
                            cl-list.anz  = t-anz
                            cl-list.pax  = t-pax
                            cl-list.net  = t-net
                            cl-list.manz = t-manz
                            cl-list.mnet = t-mnet
                            cl-list.mpax = t-mpax
                            cl-list.yanz = t-manz
                            cl-list.ypax = t-mnet
                            cl-list.ynet = t-mpax
                            t-anz  = 0
                            t-pax  = 0
                            t-net  = 0
                            t-manz = 0
                            t-mnet = 0
                            t-mpax = 0
                            t-yanz = 0
                            t-ynet = 0
                            t-ypax = 0
                            .
                    END.

                    CREATE cl-list.
                    cl-list.zinr = res-line.zinr.
                    cl-list.rmcat = zimmer.kbezeich.
                    
                    last-zikatnr = res-line.zikatnr.
                    last-zinr = res-line.zinr.                                     
                END.

                /*FDL Nov 08, 2024: Ticket 064FE3*/
                do-it = YES.
                IF excl-compl THEN
                DO:  
                    FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode
                         AND (segment.betriebsnr EQ 1 OR segment.betriebsnr EQ 2) NO-LOCK NO-ERROR.
                    IF AVAILABLE segment THEN do-it = NO.
                END.

                IF do-it THEN
                DO:
                    DO datum = s-datum TO e-datum:
                        amount-rmrev    = res-line.zipreis * frate.
                        amount-rmargt   = ROUND(res-line.zipreis * frate, price-decimal).
    
                        FOR EACH argt-line WHERE argt-line.argtnr EQ arrangement.argtnr
                            AND NOT argt-line.kind2 NO-LOCK:
                            FIND FIRST artikel WHERE artikel.artnr EQ argt-line.argt-artnr
                                AND artikel.departement EQ argt-line.departement NO-LOCK.
                            RUN argt-betrag.p(RECID(res-line), RECID(argt-line),
                                OUTPUT argt-betrag, OUTPUT ex-rate).
    
                            amount-rmrev = amount-rmrev - argt-betrag * ex-rate.
                        END.
                        amount-rmrev = ROUND(amount-rmrev, price-decimal).
    
                        IF datum EQ e-datum THEN
                        DO:
                            cl-list.anz = cl-list.anz + res-line.zimmeranz.
                            cl-list.pax = cl-list.pax + res-line.erwachs + res-line.gratis +
                                        res-line.kind1 + res-line.kind2.
                            anz         = anz + res-line.zimmeranz.
                            pax         = pax + res-line.erwachs + res-line.gratis +
                                        res-line.kind1 + res-line.kind2.
                            t-anz       = t-anz + res-line.zimmeranz.
                            t-pax       = t-pax + res-line.erwachs + res-line.gratis +
                                        res-line.kind1 + res-line.kind2.
    
                            IF lod_rev THEN
                            DO:
                                cl-list.net = cl-list.net + amount-rmrev.
                                net = net + amount-rmrev.
                                t-net = t-net + amount-rmrev.
                            END.
                            ELSE
                            DO:
                                cl-list.net = cl-list.net + amount-rmargt.
                                net = net + amount-rmargt.
                                t-net = t-net + amount-rmargt.
                            END.
                        END.
                        cl-list.manz = cl-list.manz + res-line.zimmeranz.
                        cl-list.mpax = cl-list.mpax + res-line.erwachs + res-line.gratis +
                                    res-line.kind1 + res-line.kind2.
                        manz      = manz + res-line.zimmeranz.
                        mpax      = mpax + res-line.erwachs + res-line.gratis +
                                    res-line.kind1 + res-line.kind2.
                        t-manz      = t-manz + res-line.zimmeranz.
                        t-mpax      = t-mpax + res-line.erwachs + res-line.gratis +
                                    res-line.kind1 + res-line.kind2.
    
                        IF lod_rev THEN
                        DO:
                            cl-list.mnet = cl-list.mnet + amount-rmrev.
                            mnet = mnet + amount-rmrev.
                            t-mnet = t-mnet + amount-rmrev.
                        END.
                        ELSE
                        DO:
                            cl-list.mnet = cl-list.mnet + amount-rmargt.
                            mnet = mnet + amount-rmargt.
                            t-mnet = t-mnet + amount-rmargt.
                        END.
                    END.
                END.                                               
            END.
        END.
        IF sorttype EQ 2 THEN
        DO:
            CREATE cl-list.
            ASSIGN
                cl-list.flag  = "*"
                cl-list.rmcat = "Total"
                cl-list.anz  = t-anz
                cl-list.pax  = t-pax
                cl-list.net  = t-net
                cl-list.manz = t-manz
                cl-list.mnet = t-mnet
                cl-list.mpax = t-mpax
                cl-list.yanz = t-manz
                cl-list.ypax = t-mnet
                cl-list.ynet = t-mpax
                t-anz  = 0
                t-pax  = 0
                t-net  = 0
                t-manz = 0
                t-mnet = 0
                t-mpax = 0
                t-yanz = 0
                t-ynet = 0
                t-ypax = 0
                .
        END.
    END.
    FOR EACH cl-list:
        IF net  NE 0 THEN cl-list.proz    = cl-list.net / net * 100.
        IF mnet NE 0 THEN cl-list.proz1   = cl-list.mnet / mnet * 100.         
    END.
    
    CREATE cl-list. 
    cl-list.flag  = "*".
    cl-list.zinr  = "".
    CREATE cl-list. 
    cl-list.zinr  = "". 
    cl-list.rmcat = "GTOTAL". 
    cl-list.anz   = anz.
    cl-list.pax   = pax.
    cl-list.net   = net.
    IF net NE 0 THEN cl-list.proz = 100.
    cl-list.manz  = manz. 
    cl-list.mpax  = mpax. 
    cl-list.mnet  = mnet. 
    IF mnet NE 0 THEN cl-list.proz1 = 100. 
    cl-list.yanz  = manz. 
    cl-list.ypax  = mpax. 
    cl-list.ynet  = mnet. 
    IF mnet NE 0 THEN cl-list.proz2 = 100.
    
    FOR EACH cl-list NO-LOCK:
        CREATE output-list.
        output-list.flag = cl-list.flag. 
        output-list.rmNo = cl-list.zinr.                    
        ASSIGN 
            output-list.rmno1     = STRING(cl-list.zinr)
            output-list.rmtype    = STRING(cl-list.rmcat)
            output-list.rm        = cl-list.anz 
            output-list.pax       = cl-list.pax 
            output-list.rm-rev    = cl-list.net 
            output-list.percent   = cl-list.proz
            output-list.mtdrm     = cl-list.manz 
            output-list.pax1      = cl-list.mpax 
            output-list.rm-rev1   = cl-list.mnet 
            output-list.percent1  = cl-list.proz1
            output-list.ftdrm     = cl-list.manz 
            output-list.pax2      = cl-list.mpax 
            output-list.rm-rev2   = cl-list.mnet 
            output-list.percent3  = cl-list.proz1.            
    END.
END PROCEDURE.

PROCEDURE create-zinrstat:
    DEFINE VARIABLE mm                  AS INTEGER. 
    DEFINE VARIABLE yy                  AS INTEGER. 
    DEFINE VARIABLE datum               AS DATE. 
    DEFINE VARIABLE last-zikatnr        AS INTEGER INITIAL 0. 

    anz = 0.
    pax = 0.
    net = 0.
    manz = 0. 
    mpax = 0. 
    mnet = 0. 
    yanz = 0. 
    ypax = 0. 
    ynet = 0. 
    
    t-anz  = 0.
    t-pax  = 0.
    t-manz = 0. 
    t-mpax = 0. 
    t-mnet = 0. 
    t-yanz = 0. 
    t-ypax = 0. 
    t-ynet = 0. 

    IF m-ftd = YES AND m-ytd = NO THEN 
    DO: 
      from-date = f-date. 
      to-date = t-date. 
      mm = month(to-date). 
      yy = year(to-date). 
    END.
    ELSE IF m-ftd = NO AND m-ytd = YES THEN
    DO:
      /*to-date = t-date. */
      mm = month(to-date). 
      yy = year(to-date). 
      from-date = DATE(1,1,yy). 
    END. 
    FOR EACH output-list: 
      delete output-list. 
    END. 
    FOR EACH cl-list: 
      delete cl-list. 
    END.
    
    IF rm-no NE "" THEN
    DO:
        FIND FIRST zimmer WHERE zimmer.zinr = rm-no NO-LOCK NO-ERROR.
        IF AVAILABLE zimmer THEN
        DO:
            CREATE cl-list. 
            cl-list.zinr = rm-no. 
            cl-list.rmcat = zimmer.kbezeich. 
    
            DO datum = from-date TO to-date: 
                FIND FIRST zinrstat WHERE zinrstat.zinr = rm-no 
                    AND zinrstat.datum = datum AND zinrstat.zimmeranz GT 0 USE-INDEX zinrdat_ix NO-LOCK NO-ERROR. 
                IF AVAILABLE zinrstat THEN
                DO:
                    /*FDL Nov 08, 2024: Ticket 064FE3*/
                    do-it = YES.
                    IF excl-compl THEN
                    DO:
                        FIND FIRST genstat WHERE genstat.datum EQ datum
                            AND genstat.zikatnr EQ zimmer.zikatnr
                            AND genstat.zinr EQ zimmer.zinr
                            AND genstat.zipreis EQ 0 
                            AND genstat.gratis NE 0
                            AND genstat.resstatus EQ 6
                            AND genstat.res-logic[2] NO-LOCK NO-ERROR.
                        IF AVAILABLE genstat THEN do-it = NO.
                        ELSE
                        DO:
                            FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
                                AND (segment.betriebsnr = 1 OR segment.betriebsnr = 2) NO-LOCK NO-ERROR.
                            IF AVAILABLE segment THEN do-it = NO.
                        END.
                    END.                    
                
                    IF do-it THEN
                    DO:
                        IF datum = to-date THEN
                        DO:
                            cl-list.anz = cl-list.anz + zinrstat.zimmeranz.
                            cl-list.net = cl-list.net + zinrstat.argtumsatz. 
                            cl-list.pax = cl-list.pax + zinrstat.person. 
                            anz         = anz + zinrstat.zimmeranz. 
                            pax         = pax + zinrstat.person. 
                            net         = net + zinrstat.argtumsatz. 
                        END.
                        IF month(zinrstat.datum) = mm AND YEAR(zinrstat.datum) = yy THEN 
                        DO:
                            cl-list.manz    = cl-list.manz + zinrstat.zimmeranz. 
                            cl-list.mnet    = cl-list.mnet + zinrstat.argtumsatz. 
                            cl-list.mpax    = cl-list.mpax + zinrstat.person. 
                            manz            = manz + zinrstat.zimmeranz. 
                            mpax            = mpax + zinrstat.person. 
                            mnet            = mnet + zinrstat.argtumsatz. 
                        END.
                        cl-list.yanz = cl-list.yanz + zinrstat.zimmeranz. 
                        cl-list.ypax = cl-list.ypax + zinrstat.person. 
                        cl-list.ynet = cl-list.ynet + zinrstat.argtumsatz. 
                        yanz        = yanz + zinrstat.zimmeranz. 
                        ypax        = ypax + zinrstat.person. 
                        ynet        = ynet + zinrstat.argtumsatz. 
                    END.                    
                END.
            END.          
        END.
    END.
    ELSE 
    DO:
        rm-no = "".
        IF sorttype = 1 THEN 
        DO:
            FOR EACH zimmer NO-LOCK,
                FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK BY zimmer.zinr:
                
                CREATE cl-list.
                cl-list.zinr  = zimmer.zinr. 
                cl-list.rmcat = zimkateg.kurzbez.                 
                                
                DO datum = from-date TO to-date:
                    FIND FIRST zinrstat WHERE zinrstat.zinr = zimmer.zinr 
                        AND zinrstat.datum = datum AND zinrstat.zimmeranz GT 0 USE-INDEX zinrdat_ix NO-LOCK NO-ERROR. 
                    IF AVAILABLE zinrstat THEN
                    DO:
                        /*FDL Nov 08, 2024: Ticket 064FE3*/
                        do-it = YES.
                        IF excl-compl THEN
                        DO:
                            FIND FIRST genstat WHERE genstat.datum EQ datum
                                AND genstat.zikatnr EQ zimmer.zikatnr
                                AND genstat.zinr EQ zimmer.zinr
                                AND genstat.zipreis EQ 0 
                                AND genstat.gratis NE 0
                                AND genstat.resstatus EQ 6
                                AND genstat.res-logic[2] NO-LOCK NO-ERROR.
                            IF AVAILABLE genstat THEN do-it = NO.
                            ELSE
                            DO:
                                FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
                                    AND (segment.betriebsnr = 1 OR segment.betriebsnr = 2) NO-LOCK NO-ERROR.
                                IF AVAILABLE segment THEN do-it = NO.
                            END.
                        END. 

                        IF do-it THEN
                        DO:
                            IF datum = to-date THEN
                            DO:
                                cl-list.anz = cl-list.anz + zinrstat.zimmeranz.
                                cl-list.net = cl-list.net + zinrstat.argtumsatz. 
                                cl-list.pax = cl-list.pax + zinrstat.person. 
                                anz         = anz + zinrstat.zimmeranz. 
                                pax         = pax + zinrstat.person. 
                                net         = net + zinrstat.argtumsatz.
                            END.
                            IF month(zinrstat.datum) = mm AND YEAR(zinrstat.datum) = yy THEN 
                            DO:
                                 cl-list.manz = cl-list.manz + zinrstat.zimmeranz. 
                                 cl-list.mnet = cl-list.mnet + zinrstat.argtumsatz. 
                                 cl-list.mpax = cl-list.mpax + zinrstat.person. 
                                 manz         = manz + zinrstat.zimmeranz. 
                                 mpax         = mpax + zinrstat.person. 
                                 mnet         = mnet + zinrstat.argtumsatz.
                            END.
                            cl-list.yanz = cl-list.yanz + zinrstat.zimmeranz. 
                            cl-list.ypax = cl-list.ypax + zinrstat.person. 
                            cl-list.ynet = cl-list.ynet + zinrstat.argtumsatz. 
                            yanz = yanz + zinrstat.zimmeranz. 
                            ypax = ypax + zinrstat.person. 
                            ynet = ynet + zinrstat.argtumsatz.
                        END.                         
                    END.
                END.                             
            END.
        END.
        ELSE IF sorttype = 2 THEN
        DO:
            FOR EACH zimmer /*WHERE zimmer.sleeping = YES*/ NO-LOCK,
                FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr 
                NO-LOCK BY zimkateg.zikatnr BY zimmer.zinr: 
                IF last-zikatnr = 0 THEN last-zikatnr = zimmer.zikatnr. 
                IF last-zikatnr NE zimmer.zikatnr THEN 
                DO:
                    CREATE cl-list.
                    ASSIGN 
                        cl-list.rmcat = "Total" 
                        cl-list.anz  = t-anz
                        cl-list.pax  = t-pax
                        cl-list.net  = t-net
                        cl-list.manz = t-manz 
                        cl-list.mnet = t-mnet 
                        cl-list.mpax = t-mpax 
                        cl-list.yanz = t-yanz 
                        cl-list.ypax = t-ypax 
                        cl-list.ynet = t-ynet 
                        t-anz  = 0
                        t-pax  = 0
                        t-net  = 0
                        t-manz = 0 
                        t-mnet = 0 
                        t-mpax = 0 
                        t-yanz = 0 
                        t-ynet = 0 
                        t-ypax = 0
                        last-zikatnr = zimmer.zikatnr. 
                END. 
                
                CREATE cl-list. 
                cl-list.zinr = zimmer.zinr. 
                cl-list.rmcat = zimkateg.kurzbez.
    
                DO datum = from-date TO to-date: 
                    FIND FIRST zinrstat WHERE zinrstat.zinr = zimmer.zinr 
                        AND zinrstat.datum = datum AND zinrstat.zimmeranz GT 0 USE-INDEX zinrdat_ix NO-LOCK NO-ERROR. 
                    IF AVAILABLE zinrstat THEN
                    DO:
                        /*FDL Nov 08, 2024: Ticket 064FE3*/
                        do-it = YES.
                        IF excl-compl THEN
                        DO:
                            FIND FIRST genstat WHERE genstat.datum EQ datum
                                AND genstat.zikatnr EQ zimmer.zikatnr
                                AND genstat.zinr EQ zimmer.zinr
                                AND genstat.zipreis EQ 0 
                                AND genstat.gratis NE 0
                                AND genstat.resstatus EQ 6
                                AND genstat.res-logic[2] NO-LOCK NO-ERROR.
                            IF AVAILABLE genstat THEN do-it = NO.
                            ELSE
                            DO:
                                FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
                                    AND (segment.betriebsnr = 1 OR segment.betriebsnr = 2) NO-LOCK NO-ERROR.
                                IF AVAILABLE segment THEN do-it = NO.
                            END.
                        END. 

                        IF do-it THEN
                        DO:
                            IF datum = to-date THEN
                            DO:
                                cl-list.anz = cl-list.anz + zinrstat.zimmeranz. 
                                cl-list.net = cl-list.net + zinrstat.argtumsatz. 
                                cl-list.pax = cl-list.pax + zinrstat.person. 
                                anz         = anz + zinrstat.zimmeranz. 
                                pax         = pax + zinrstat.person. 
                                net         = net + zinrstat.argtumsatz. 
                                t-anz       = t-anz + zinrstat.zimmeranz. 
                                t-pax       = t-pax + zinrstat.person. 
                                t-net       = t-net + zinrstat.argtumsatz.
                            END.
                        
                            IF month(zinrstat.datum) = mm THEN
                            DO:
                                cl-list.manz = cl-list.manz + zinrstat.zimmeranz. 
                                cl-list.mnet = cl-list.mnet + zinrstat.argtumsatz. 
                                cl-list.mpax = cl-list.mpax + zinrstat.person. 
                                manz         = manz + zinrstat.zimmeranz. 
                                mpax         = mpax + zinrstat.person. 
                                mnet         = mnet + zinrstat.argtumsatz. 
                                t-manz       = t-manz + zinrstat.zimmeranz. 
                                t-mpax       = t-mpax + zinrstat.person. 
                                t-mnet       = t-mnet + zinrstat.argtumsatz. 
                            END.
                            cl-list.yanz = cl-list.yanz + zinrstat.zimmeranz. 
                            cl-list.ypax = cl-list.ypax + zinrstat.person. 
                            cl-list.ynet = cl-list.ynet + zinrstat.argtumsatz. 
                            yanz         = yanz + zinrstat.zimmeranz. 
                            ypax         = ypax + zinrstat.person. 
                            ynet         = ynet + zinrstat.argtumsatz. 
                            t-yanz       = t-yanz + zinrstat.zimmeranz. 
                            t-ypax       = t-ypax + zinrstat.person. 
                            t-ynet       = t-ynet + zinrstat.argtumsatz. 
                        END.                        
                    END.
                END.
            END.
        END.
        IF sorttype = 2 THEN
        DO:
            CREATE cl-list. 
            ASSIGN 
                cl-list.rmcat = "Total" 
                cl-list.anz  = t-anz
                cl-list.pax  = t-pax
                cl-list.net  = t-net
                cl-list.manz = t-manz 
                cl-list.mnet = t-mnet 
                cl-list.mpax = t-mpax 
                cl-list.yanz = t-yanz 
                cl-list.ypax = t-ypax 
                cl-list.ynet = t-ynet. 
            ASSIGN
                t-anz  = 0
                t-pax  = 0
                t-net  = 0
                t-manz = 0 
                t-mnet = 0 
                t-mpax = 0 
                t-yanz = 0 
                t-ynet = 0 
                t-ypax = 0. 
        END.
    END.
    FOR EACH cl-list:
        IF net  NE 0 THEN cl-list.proz    = cl-list.net / net * 100.
        IF mnet NE 0 THEN cl-list.proz1   = cl-list.mnet / mnet * 100. 
        IF ynet NE 0 THEN cl-list.proz2   = cl-list.ynet / ynet * 100. 
    END.
    CREATE cl-list. 
    cl-list.flag = "*".
    
    CREATE cl-list. 
    cl-list.zinr  = "". 
    cl-list.rmcat = "GTOTAL". 
    cl-list.anz   = anz.
    cl-list.pax   = pax.
    cl-list.net   = net.
    IF net NE 0 THEN cl-list.proz = 100.
    cl-list.manz  = manz. 
    cl-list.mpax  = mpax. 
    cl-list.mnet  = mnet. 
    IF mnet NE 0 THEN cl-list.proz1 = 100. 
    cl-list.yanz  = yanz. 
    cl-list.ypax  = ypax. 
    cl-list.ynet  = ynet. 
    
    IF ynet NE 0 THEN cl-list.proz2 = 100. 
    FOR EACH cl-list NO-LOCK:
        CREATE output-list.
        output-list.flag = cl-list.flag. 
        output-list.rmNo = cl-list.zinr.
        IF cl-list.flag = "*" THEN
        DO:
        END.
    
        ELSE 
        DO:
            IF price-decimal = 0 THEN
            DO:              
                ASSIGN 
                    output-list.rmno1     = STRING(cl-list.zinr)
                    output-list.rmtype    = STRING(cl-list.rmcat)
                    output-list.rm        = cl-list.anz 
                    output-list.pax       = cl-list.pax 
                    output-list.rm-rev    = cl-list.net 
                    output-list.percent   = cl-list.proz
                    output-list.mtdrm     = cl-list.manz 
                    output-list.pax1      = cl-list.mpax 
                    output-list.rm-rev1   = cl-list.mnet 
                    output-list.percent1  = cl-list.proz1
                    output-list.ftdrm     = cl-list.yanz 
                    output-list.pax2      = cl-list.ypax 
                    output-list.rm-rev2   = cl-list.ynet 
                    output-list.percent3  = cl-list.proz2.
            END.
            ELSE
            DO:
                CREATE output-list.
                ASSIGN 
                    output-list.rmno1     = STRING(cl-list.zinr)
                    output-list.rmtype    = STRING(cl-list.rmcat)
                    output-list.rm        = cl-list.anz 
                    output-list.pax       = cl-list.pax 
                    output-list.rm-rev    = cl-list.net 
                    output-list.percent   = cl-list.proz
                    output-list.mtdrm     = cl-list.manz 
                    output-list.pax1      = cl-list.mpax 
                    output-list.rm-rev1   = cl-list.mnet 
                    output-list.percent1  = cl-list.proz1
                    output-list.ftdrm     = cl-list.yanz 
                    output-list.pax2      = cl-list.ypax 
                    output-list.rm-rev2   = cl-list.ynet 
                    output-list.percent3  = cl-list.proz2.
            END.
        END.
    END.
END. 


PROCEDURE create-genstat: 
    DEFINE VARIABLE mm              AS INTEGER. 
    DEFINE VARIABLE yy              AS INTEGER. 
    DEFINE VARIABLE datum           AS DATE. 
    DEFINE VARIABLE last-zikatnr    AS INTEGER INITIAL 0. 

    anz = 0.
    pax = 0.
    net = 0.
    manz = 0. 
    mpax = 0. 
    mnet = 0. 
    yanz = 0. 
    ypax = 0. 
    ynet = 0. 
    
    t-anz  = 0.
    t-pax  = 0.
    t-manz = 0. 
    t-mpax = 0. 
    t-mnet = 0. 
    t-yanz = 0. 
    t-ypax = 0. 
    t-ynet = 0. 

    IF m-ftd = YES THEN
    DO:
        from-date   = f-date. 
        to-date     = t-date. 
        mm          = month(to-date). 
        yy          = year(to-date).
    END.
    ELSE
    DO:
        /*to-date   = t-date.*/
        mm        = month(to-date). 
        yy        = year(to-date). 
        from-date = DATE(1,1,yy). 
    END.
    FOR EACH output-list: 
        delete output-list. 
    END.
    FOR EACH output-list: 
       delete output-list. 
   END.
    
   IF rm-no NE "" THEN
   DO:
       FIND FIRST zimmer WHERE zimmer.zinr = rm-no NO-LOCK NO-ERROR.
       IF AVAILABLE zimmer THEN
       DO:
           create cl-list. 
           cl-list.zinr     = rm-no. 
           cl-list.rmcat    = zimmer.kbezeich.

           DO datum = from-date TO to-date:
               FOR EACH genstat WHERE genstat.zinr = rm-no AND genstat.datum = datum 
                   AND (genstat.resstatus = 6 OR genstat.resstatus = 8) NO-LOCK:

                   /*FDL Nov 08, 2024: Ticket 064FE3*/
                   do-it = YES.
                   IF excl-compl THEN
                   DO:  
                       FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode
                            AND (segment.betriebsnr EQ 1 OR segment.betriebsnr EQ 2) NO-LOCK NO-ERROR.
                       IF AVAILABLE segment THEN do-it = NO.
                       ELSE 
                       DO:
                           IF genstat.zipreis EQ 0 AND genstat.gratis NE 0 
                               AND genstat.resstatus EQ 6
                               AND genstat.res-logic[2] EQ YES THEN do-it = NO.
                       END.  
                   END.

                   IF do-it THEN
                   DO:
                       IF datum = to-date THEN
                       DO:
                           cl-list.anz = cl-list.anz + 1.
                           cl-list.net = cl-list.net + genstat.logis.
                           cl-list.pax = cl-list.pax + genstat.erwachs + genstat.gratis +
                                         genstat.kind1 + genstat.kind2 + genstat.kind3. 
                            anz        = anz + 1. 
                            pax        = pax + genstat.erwachs + genstat.gratis +
                                         genstat.kind1 + genstat.kind2 + genstat.kind3. 
                            net        = net + genstat.logis.
    
                       END.
                       IF MONTH(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN
                       DO:
                           cl-list.manz = cl-list.manz + 1. 
                           cl-list.mnet = cl-list.mnet + genstat.logis.
                           cl-list.mpax = cl-list.mpax + genstat.erwachs + genstat.gratis 
                                          + genstat.kind1 + genstat.kind2 + genstat.kind3. 
                           manz         = manz + 1. 
                           mpax         = mpax + genstat.erwachs + genstat.gratis 
                                          + genstat.kind1 + genstat.kind2 + genstat.kind3. 
                           mnet         = mnet + genstat.logis.
    
                       END.
                       cl-list.yanz = cl-list.yanz + 1. 
                       cl-list.ypax = cl-list.ypax + genstat.erwachs + genstat.gratis 
                                      + genstat.kind1 + genstat.kind2 + genstat.kind3. 
                       cl-list.ynet = cl-list.ynet + genstat.logis.
                       yanz         = yanz + 1.
                       ypax         = ypax + genstat.erwachs + genstat.gratis
                                    + genstat.kind1 + genstat.kind2 + genstat.kind3. 
                       ynet         = ynet + genstat.logis.
                   END.                  
               END.
           END.
       END.
   END.
   ELSE 
   DO:
       rm-no = "".
       IF sorttype = 1 THEN 
       DO:
           FOR EACH zimmer NO-LOCK,
               FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr 
               NO-LOCK BY zimmer.zinr: 

               CREATE cl-list.
               cl-list.zinr     = zimmer.zinr.
               cl-list.rmcat    = zimkateg.kurzbez.

               DO datum = from-date TO to-date:
                   FOR EACH genstat WHERE genstat.zinr = zimmer.zinr 
                       AND genstat.datum = datum
                       AND (genstat.resstatus = 6 OR genstat.resstatus = 8) NO-LOCK:
               
                       /*FDL Nov 08, 2024: Ticket 064FE3*/
                       do-it = YES.
                       IF excl-compl THEN
                       DO:  
                           FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode
                                AND (segment.betriebsnr EQ 1 OR segment.betriebsnr EQ 2) NO-LOCK NO-ERROR.
                           IF AVAILABLE segment THEN do-it = NO.
                           ELSE 
                           DO:
                               IF genstat.zipreis EQ 0 AND genstat.gratis NE 0 
                                   AND genstat.resstatus EQ 6
                                   AND genstat.res-logic[2] EQ YES THEN do-it = NO.
                           END.  
                       END.
                       
                       IF do-it THEN
                       DO:
                           IF datum = to-date THEN
                           DO:
                               ASSIGN 
                                   cl-list.anz = cl-list.anz + 1
                                   cl-list.net = cl-list.net + genstat.logis
                                   cl-list.pax = cl-list.pax + genstat.erwachs + genstat.gratis 
                                                 + genstat.kind1 + genstat.kind2 + genstat.kind3
                                   anz         = anz + 1
                                   pax         = pax + genstat.erwachs + genstat.gratis 
                                               + genstat.kind1 + genstat.kind2 + genstat.kind3.
                                   net         = net + genstat.logis.
                           END.
                           IF month(genstat.datum) = mm AND YEAR(genstat.datum) = yy THEN
                           DO:
                               ASSIGN
                                   cl-list.manz = cl-list.manz + 1
                                   cl-list.mnet = cl-list.mnet + genstat.logis
                                   cl-list.mpax = cl-list.mpax + genstat.erwachs + genstat.gratis 
                                                + genstat.kind1 + genstat.kind2 + genstat.kind3
                                   manz = manz + 1
                                   mpax = mpax + genstat.erwachs + genstat.gratis 
                                        + genstat.kind1 + genstat.kind2 + genstat.kind3
                                   mnet = mnet + genstat.logis. 
                           END.
                           ASSIGN 
                               cl-list.yanz = cl-list.yanz + 1
                               cl-list.ypax = cl-list.ypax + genstat.erwachs + genstat.gratis
                                            + genstat.kind1 + genstat.kind2 + genstat.kind3 
                               cl-list.ynet = cl-list.ynet + genstat.logis
                               yanz         = yanz + 1
                               ypax         = ypax + genstat.erwachs + genstat.gratis 
                                            + genstat.kind1 + genstat.kind2 + genstat.kind3
                               ynet         = ynet + genstat.logis. 
                       END.                       
                   END.
               END.
           END.
       END.
       ELSE IF sorttype = 2 THEN
       DO:
           FOR EACH zimmer /*WHERE zimmer.sleeping = YES*/ NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr 
               NO-LOCK BY zimkateg.zikatnr BY zimmer.zinr: 
               IF last-zikatnr = 0 THEN last-zikatnr = zimmer.zikatnr.
               IF last-zikatnr NE zimmer.zikatnr THEN
               DO:
                    CREATE cl-list. 
                      ASSIGN 
                          cl-list.rmcat = "Total" 
                          cl-list.anz  = t-anz
                          cl-list.pax  = t-pax
                          cl-list.net  = t-net
                          cl-list.manz = t-manz 
                          cl-list.mnet = t-mnet 
                          cl-list.mpax = t-mpax 
                          cl-list.yanz = t-yanz 
                          cl-list.ypax = t-ypax 
                          cl-list.ynet = t-ynet 
                          t-anz  = 0
                          t-pax  = 0
                          t-net  = 0
                          t-manz = 0 
                          t-mnet = 0 
                          t-mpax = 0 
                          t-yanz = 0 
                          t-ynet = 0 
                          t-ypax = 0. 
                          last-zikatnr = zimmer.zikatnr. 
               END.
    
               CREATE cl-list. 
               cl-list.zinr = zimmer.zinr. 
               cl-list.rmcat = zimkateg.kurzbez.
               DO datum = from-date TO to-date:
                   FOR EACH genstat WHERE genstat.zinr = zimmer.zinr 
                       AND genstat.datum = datum
                       AND (genstat.resstatus = 6 OR genstat.resstatus = 8) NO-LOCK:

                       /*FDL Nov 08, 2024: Ticket 064FE3*/
                       do-it = YES.
                       IF excl-compl THEN
                       DO:  
                           FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode
                                AND (segment.betriebsnr EQ 1 OR segment.betriebsnr EQ 2) NO-LOCK NO-ERROR.
                           IF AVAILABLE segment THEN do-it = NO.
                           ELSE 
                           DO:
                               IF genstat.zipreis EQ 0 AND genstat.gratis NE 0 
                                   AND genstat.resstatus EQ 6
                                   AND genstat.res-logic[2] EQ YES THEN do-it = NO.
                           END.  
                       END.

                       IF do-it THEN
                       DO:
                           IF datum = to-date THEN
                           DO:
                               ASSIGN
                                   cl-list.anz = cl-list.anz + 1
                                   cl-list.net = cl-list.net + genstat.logis
                                   cl-list.pax = cl-list.pax + genstat.erwachs + genstat.gratis 
                                                 + genstat.kind1 + genstat.kind2 + genstat.kind3
                                   /**/
                                   anz         = anz + 1
                                   pax         = pax + genstat.erwachs + genstat.gratis
                                               + genstat.kind1 + genstat.kind2 + genstat.kind3
                                   net         = net + genstat.logis
                                   t-anz       = t-anz + 1
                                   t-pax       = t-pax + genstat.erwachs + genstat.gratis
                                               + genstat.kind1 + genstat.kind2 + genstat.kind3
                                   t-net       = t-net + genstat.logis. 
                           END.
                           IF MONTH(genstat.datum) = mm THEN
                           DO:
                               ASSIGN 
                                   cl-list.manz = cl-list.manz + 1 
                                   cl-list.mnet = cl-list.mnet + genstat.logis
                                   cl-list.mpax = cl-list.mpax + genstat.erwachs + genstat.gratis 
                                                  + genstat.kind1 + genstat.kind2 + genstat.kind3
                                   /**/
                                   manz        = manz + 1
                                   mpax        = mpax + genstat.erwachs + genstat.gratis 
                                                   + genstat.kind1 + genstat.kind2 + genstat.kind3
                                   mnet        = mnet + genstat.logis
                                   t-manz      = t-manz + 1
                                   t-mpax      = t-mpax + genstat.erwachs + genstat.gratis 
                                                   + genstat.kind1 + genstat.kind2 + genstat.kind3
                                   t-mnet      = t-mnet + genstat.logis.
                           END.
                           ASSIGN
                               cl-list.yanz = cl-list.yanz + 1 
                               cl-list.ypax = cl-list.ypax + genstat.erwachs + genstat.gratis 
                                               + genstat.kind1 + genstat.kind2 + genstat.kind3
                               /**/
                               cl-list.ynet = cl-list.ynet + genstat.logis
                               yanz         = yanz + 1
                               ypax         = ypax + genstat.erwachs + genstat.gratis 
                                               + genstat.kind1 + genstat.kind2 + genstat.kind3
                               ynet         = ynet + genstat.logis
                               t-yanz       = t-yanz + 1
                               t-ypax       = t-ypax + genstat.erwachs + genstat.gratis 
                                            + genstat.kind1 + genstat.kind2 + genstat.kind3
                               t-ynet       = t-ynet + genstat.logis. 
                       END.                       
                   END.
               END.              
           END.
       END.

       IF sorttype = 2  THEN
       DO:
           CREATE cl-list.
           ASSIGN
               cl-list.rmcat = "Total" 
               cl-list.anz  = t-anz
               cl-list.pax  = t-pax
               cl-list.net  = t-net
               cl-list.manz = t-manz 
               cl-list.mnet = t-mnet 
               cl-list.mpax = t-mpax 
               cl-list.yanz = t-yanz 
               cl-list.ypax = t-ypax 
               cl-list.ynet = t-ynet. 

           ASSIGN
              t-anz  = 0
              t-pax  = 0
              t-net  = 0
              t-manz = 0 
              t-mnet = 0 
              t-mpax = 0 
              t-yanz = 0 
              t-ynet = 0 
              t-ypax = 0. 
       END.
   END.
   FOR EACH cl-list:
       IF net  NE 0 THEN cl-list.proz = cl-list.net / net * 100.
       IF mnet NE 0 THEN cl-list.proz1 = cl-list.mnet / mnet * 100. 
       IF ynet NE 0 THEN cl-list.proz2 = cl-list.ynet / ynet * 100. 
   END.
 
   CREATE cl-list. 
   cl-list.zinr  = "". 
   cl-list.rmcat = "GTOTAL". 
   cl-list.anz   = anz.
   cl-list.pax   = pax.
   cl-list.net   = net.
   IF net NE 0 THEN cl-list.proz = 100.
   cl-list.manz  = manz. 
   cl-list.mpax  = mpax. 
   cl-list.mnet  = mnet. 
   IF mnet NE 0 THEN cl-list.proz1 = 100. 
   cl-list.yanz  = yanz. 
   cl-list.ypax  = ypax. 
   cl-list.ynet  = ynet. 
   IF ynet NE 0 THEN cl-list.proz2 = 100.

   FOR EACH cl-list NO-LOCK:
      CREATE output-list.
      ASSIGN 
          output-list.rmno1     = STRING(cl-list.zinr)
          output-list.rmtype    = STRING(cl-list.rmcat)
          output-list.rm        = cl-list.anz 
          output-list.pax       = cl-list.pax 
          output-list.rm-rev    = cl-list.net 
          output-list.percent   = cl-list.proz
          output-list.mtdrm     = cl-list.manz 
          output-list.pax1      = cl-list.mpax 
          output-list.rm-rev1   = cl-list.mnet 
          output-list.percent1  = cl-list.proz1
          output-list.ftdrm     = cl-list.yanz 
          output-list.pax2      = cl-list.ypax 
          output-list.rm-rev2   = cl-list.ynet 
          output-list.percent3  = cl-list.proz2.             
   END.
END. 
