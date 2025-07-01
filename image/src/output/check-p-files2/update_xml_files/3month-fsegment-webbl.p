DEFINE TEMP-TABLE output-list
    FIELD segmentcode AS INTEGER
    FIELD segment     AS CHAR
    FIELD monthyear   AS DATE
    FIELD room        AS INTEGER FORMAT ">>,>>9"
    FIELD revenue     AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD avrg-rev    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD pax         AS INTEGER FORMAT ">,>>9"
    FIELD occpr       AS DECIMAL FORMAT "->,>>,>>9.99"
    FIELD doccpr      AS DECIMAL FORMAT "->,>>,>>9.99"
.

DEFINE INPUT PARAMETER from-date   AS DATE   NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE to-date        AS DATE    NO-UNDO.
DEFINE VARIABLE fr-date        AS DATE    NO-UNDO.
DEFINE VARIABLE last-tdate     AS DATE    NO-UNDO.
DEFINE VARIABLE last-fdate     AS DATE    NO-UNDO.
 
DEFINE VARIABLE long-digit     AS LOGICAL NO-UNDO.
DEFINE VARIABLE black-list     AS INTEGER NO-UNDO. 
DEFINE VARIABLE ci-date        AS DATE    NO-UNDO.
 
DEFINE VARIABLE tot-rm         AS INTEGER NO-UNDO.
DEFINE VARIABLE tot-rev        AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-arr        AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-pax        AS INTEGER NO-UNDO.
DEFINE VARIABLE tot-occpr      AS INTEGER NO-UNDO.
DEFINE VARIABLE tot-doccpr     AS INTEGER NO-UNDO.

DEFINE VARIABLE all-rm         AS INTEGER NO-UNDO.
DEFINE VARIABLE act-rm         AS INTEGER NO-UNDO.
DEFINE VARIABLE inactive       AS INTEGER NO-UNDO. 
DEFINE VARIABLE tot-room       AS INTEGER NO-UNDO.
 
DEFINE VARIABLE trev1          AS DECIMAL NO-UNDO EXTENT 12.
DEFINE VARIABLE trm1           AS DECIMAL NO-UNDO EXTENT 12.
DEFINE VARIABLE loopi          AS INTEGER NO-UNDO.
DEFINE VARIABLE monthnr        AS INTEGER NO-UNDO.
DEFINE VARIABLE yearnr         AS INTEGER NO-UNDO.
 
DEFINE VARIABLE mtd-act        AS INTEGER.
DEFINE VARIABLE mtd-totrm      AS INTEGER.

DEFINE VARIABLE do-it AS LOGICAL INITIAL NO.

DEFINE BUFFER boutput FOR output-list.
DEFINE BUFFER segmtype-exist FOR segment.
DEFINE BUFFER rline FOR res-line.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN ci-date = htparam.fdate.

FIND FIRST htparam WHERE paramnr = 709 NO-LOCK. 
ASSIGN black-list = htparam.finteger. 

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FOR EACH zimmer WHERE sleeping NO-LOCK: 
    act-rm = act-rm + 1.
END.

FOR EACH zimmer WHERE NOT zimmer.sleeping NO-LOCK: 
    inactive = inactive + 1. 
END.

tot-room = act-rm + inactive.

fr-date = DATE(MONTH(from-date),1,YEAR(from-date)).
IF MONTH(fr-date) GE 10 THEN
    to-date = DATE(3 - (12 - MONTH(from-date)),1,YEAR(from-date) + 1) - 1.
ELSE
    to-date = DATE(MONTH(from-date) + 3,1,YEAR(from-date)) - 1.

FOR EACH segment WHERE segment.betriebsnr EQ 0 AND segment.segmentcode NE black-list NO-LOCK BY segment.segmentcode:
    DO loopi = MONTH(fr-date) TO MONTH(fr-date) + 2:
        IF loopi GT 12 THEN
            ASSIGN
                monthnr = loopi - 12
                yearnr  = 1.
        ELSE
            ASSIGN
                monthnr = loopi
                yearnr  = 0.
        CREATE output-list.
        ASSIGN
            output-list.segmentcode = segment.segmentcode
            output-list.segment     = ENTRY(1, segment.bezeich, "$$0")
            output-list.monthyear   = DATE(monthnr,1,YEAR(from-date) + yearnr)
        .
        CREATE output-list.
        ASSIGN
            output-list.segmentcode = segment.segmentcode
            output-list.segment     = ENTRY(1, segment.bezeich, "$$0")
            output-list.monthyear   = DATE(monthnr,1,YEAR(from-date) + yearnr - 1)  
        .
    END.
END.

/*************** MAIN LOGIC ***************/
RUN create-list.
tot-rm     = 0.
tot-rev    = 0.
tot-arr    = 0.
tot-pax    = 0.
tot-occpr  = 0.
tot-doccpr = 0.
DO loopi = MONTH(fr-date) TO MONTH(fr-date) + 2:
    IF loopi GT 12 THEN
        ASSIGN
            monthnr = loopi - 12
            yearnr  = 1.
    ELSE
        ASSIGN
            monthnr = loopi
            yearnr  = 0.
    CREATE output-list.
    ASSIGN
        output-list.segmentcode = 99999
        output-list.segment     = "T O T A L"
        output-list.monthyear   = DATE(monthnr,1,YEAR(from-date) + yearnr)
    .
    CREATE output-list.
    ASSIGN
        output-list.segmentcode = 99999
        output-list.segment     = "T O T A L"
        output-list.monthyear   = DATE(monthnr,1,YEAR(from-date) + yearnr - 1)  
    .
END.
FOR EACH output-list BY output-list.segmentcode:
    RUN count-mtd-totrm(output-list.monthyear).
    IF output-list.segmentcode NE 99999 THEN
    DO:
        IF output-list.room EQ 0 THEN NEXT.
        ASSIGN
            output-list.occpr  = output-list.room / mtd-act * 100
            output-list.doccpr = (output-list.pax - output-list.room) / output-list.room * 100
        .
        FIND FIRST boutput WHERE boutput.segmentcode EQ 99999 AND boutput.monthyear EQ output-list.monthyear NO-ERROR.
        IF AVAILABLE boutput THEN
        ASSIGN
            boutput.room    = boutput.room + output-list.room
            boutput.revenue = boutput.revenue + output-list.revenue
            boutput.pax     = boutput.pax + output-list.pax
        .
    END.
    ELSE
    DO:
        IF output-list.room EQ 0 THEN NEXT.
        ASSIGN
            output-list.avrg-rev = output-list.revenue / output-list.room
            output-list.occpr    = output-list.room / mtd-act * 100
            output-list.doccpr   = (output-list.pax - output-list.room) / output-list.room * 100
        .
        IF output-list.avrg-rev  = ? THEN output-list.avrg-rev  = 0.00.
    END.
    /*
    IF output-list.occpr  = ? THEN output-list.occpr  = 0.00.
    IF output-list.doccpr = ? THEN output-list.doccpr = 0.00.
    */
END.


/*************** PROCEDURE  ***************/
PROCEDURE create-list:
    DEFINE VARIABLE datum            AS DATE.
    DEFINE VARIABLE datum1           AS DATE. 
    DEFINE VARIABLE datum2           AS DATE. 
    DEFINE VARIABLE tdate            AS DATE.
    DEFINE VARIABLE fdate            AS DATE.
    DEFINE VARIABLE tot-breakfast    AS DECIMAL.
    DEFINE VARIABLE tot-Lunch        AS DECIMAL.
    DEFINE VARIABLE tot-dinner       AS DECIMAL.
    DEFINE VARIABLE tot-Other        AS DECIMAL.
    DEFINE VARIABLE curr-i           AS INTEGER.
    DEFINE VARIABLE net-lodg         AS DECIMAL.
    DEFINE VARIABLE Fnet-lodg        AS DECIMAL.
    DEFINE VARIABLE tot-rmrev        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-vat          AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-service      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE pax              AS INTEGER NO-UNDO. 
    DEFINE VARIABLE consider-it      AS LOGICAL.
    DEFINE VARIABLE dayuse-flag      AS LOGICAL. 
    
    IF to-date LT (ci-date - 1) THEN tdate = to-date. 
    ELSE tdate = ci-date - 1. 

    FOR EACH genstat WHERE 
        ((genstat.datum GE fr-date AND genstat.datum LE tdate)
        OR (genstat.datum GE DATE(MONTH(fr-date),DAY(fr-date),YEAR(fr-date) - 1) AND genstat.datum LE (DATE(MONTH(to-date) + 1,1,YEAR(to-date) - 1) - 1) ))

        AND genstat.segmentcode NE 0
        AND genstat.segmentcode NE black-list
        AND genstat.nationnr NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES 
        /*AND genstat.res-logic[3] EQ NO */
        AND genstat.resstatus NE 13
        AND NOT (genstat.res-date[1] LT genstat.datum
                 AND genstat.res-date[2] EQ genstat.datum 
                 AND genstat.resstatus = 8) /* Checkout today */
        NO-LOCK USE-INDEX segm_ix :  
        FIND FIRST output-list WHERE output-list.segmentcode EQ genstat.segmentcode
           AND output-list.monthyear EQ DATE(MONTH(genstat.datum),1,YEAR(genstat.datum)) NO-ERROR.
        IF NOT AVAILABLE output-list THEN 
        DO:
            FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-ERROR.
            IF AVAILABLE segment THEN
            DO:
                CREATE output-list.
                ASSIGN output-list.segmentcode = genstat.segmentcode
                       output-list.segment     = segment.bezeich
                       output-list.monthyear   = DATE(MONTH(genstat.datum),1,YEAR(genstat.datum))
                .
            END.
        END.
        
        ASSIGN output-list.room     = output-list.room + 1
               output-list.revenue  = output-list.revenue + genstat.logis
               output-list.avrg-rev = output-list.revenue / output-list.room
               output-list.pax      = output-list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3
        .
    END. 
    IF to-date GE ci-date THEN DO:
        FOR EACH res-line WHERE
            (res-line.active-flag LE 1
             AND res-line.resstatus LE 13
             AND res-line.resstatus NE 4
             AND res-line.resstatus NE 12
             AND NOT (res-line.ankunft GT to-date) 
             AND NOT (res-line.abreise LT fr-date)) 
            OR 
            (res-line.active-flag = 2
             AND res-line.resstatus = 8
             AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
            
            AND res-line.gastnr GT 0 
            AND res-line.l-zuordnung[3] = 0 NO-LOCK 
            USE-INDEX gnrank_ix BY res-line.resnr BY res-line.reslinnr descending: 
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
            do-it         = YES.
            dayuse-flag   = NO.

            IF do-it AND res-line.resstatus = 8 THEN
            DO:
                dayuse-flag = YES.     
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

            /*IF res-line.erwachs = 0 AND res-line.gratis GT 0 AND res-line.zipreis = 0 THEN NEXT.  COMPLIMENT /**/
            ELSE IF res-line.erwachs GT 0 AND res-line.gratis EQ 0 AND res-line.zipreis = 0 THEN NEXT.  BONUS NIGHT */

            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                AND segment.segmentcode NE black-list NO-LOCK NO-ERROR.
            IF AVAILABLE segment AND do-it THEN
            DO:
                IF res-line.ankunft GE ci-date THEN datum1 = res-line.ankunft. 
                ELSE datum1 = ci-date.
                IF res-line.abreise LE to-date THEN datum2 = res-line.abreise - 1.
                ELSE datum2 = to-date.
                
                DO datum = datum1 TO datum2:
                    ASSIGN 
                        net-lodg      = 0
                        curr-i        = curr-i + 1.

                    IF datum = res-line.abreise THEN .
                    ELSE DO:
                        ASSIGN net-lodg      = 0
                               tot-breakfast = 0
                               tot-lunch     = 0
                               tot-dinner    = 0
                               tot-other     = 0
                               tot-rmrev     = 0
                               tot-vat       = 0
                               tot-service   = 0
                               pax           = res-line.erwachs
                        . 
                        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                            AND reslin-queasy.resnr = res-line.resnr 
                            AND reslin-queasy.reslinnr = res-line.reslinnr 
                            AND reslin-queasy.date1 LE datum 
                            AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 

                        IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
                            pax = reslin-queasy.number3. 

                        consider-it = YES. 
                        
                        IF res-line.zimmerfix THEN 
                        DO: 
                            FIND FIRST rline WHERE rline.resnr = res-line.resnr 
                                AND rline.reslinnr NE res-line.reslinnr 
                                AND rline.resstatus EQ 8
                                AND rline.abreise GT datum NO-LOCK NO-ERROR. 
                            IF AVAILABLE rline THEN consider-it = NO. 
                        END. 
                                
                        RUN get-room-breakdown.p(RECID(res-line), datum, 0, fr-date,
                                                 OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                 OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                 OUTPUT tot-dinner, OUTPUT tot-other,
                                                 OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                 OUTPUT tot-service). 
                          
                        IF tot-rmrev = 0 THEN  /*ITA 020117*/
                        ASSIGN 
                            net-lodg            = 0
                            Fnet-lodg           = 0
                            tot-breakfast       = 0
                            tot-lunch           = 0
                            tot-dinner          = 0
                            tot-other           = 0
                        . 
                        
                        FIND FIRST output-list WHERE output-list.segmentcode = reservation.segmentcode 
                            AND output-list.monthyear EQ DATE(MONTH(datum),1,YEAR(datum)) NO-ERROR.
                        IF NOT AVAILABLE output-list THEN DO:
                            CREATE output-list.
                            ASSIGN output-list.segmentcode = reservation.segmentcode
                                   output-list.segment     = segment.bezeich
                                   output-list.monthyear   = DATE(MONTH(datum),1,YEAR(datum))
                            .
                        END.
                        
                        /* WRONG validation
                        ASSIGN output-list.room     = output-list.room + res-line.zimmeranz
                               output-list.revenue  = output-list.revenue + net-lodg /*  res-line.zipreis, CHANGED TO ROOM REVENUE */
                               output-list.avrg-rev = output-list.revenue / output-list.room
                               output-list.pax      = output-list.pax + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                                      + res-line.gratis) * res-line.zimmeranz.
                        .
                        */
                        IF datum = res-line.ankunft AND consider-it THEN
                        DO:                                 
                            IF res-line.ankunft LT res-line.abreise OR dayuse-flag THEN 
                            DO: 
                                IF res-line.resstatus NE 11 AND res-line.resstatus NE 13
                                    AND NOT res-line.zimmerfix THEN
                                DO:      
                                    ASSIGN 
                                        output-list.room     = output-list.room + res-line.zimmeranz
                                        output-list.revenue  = output-list.revenue + net-lodg /*  res-line.zipreis, CHANGED TO ROOM REVENUE */
                                        output-list.avrg-rev = output-list.revenue / output-list.room
                                    .
                                END.
                                IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN
                                DO:
                                    output-list.pax          = output-list.pax + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                                               + res-line.gratis) * res-line.zimmeranz.
                                END.
                            END. 
                        END. /*  Arrival */ 
                        
                        IF res-line.resstatus NE 4 AND consider-it 
                            AND (res-line.abreise GT res-line.ankunft 
                            AND res-line.ankunft NE datum
                            AND res-line.abreise NE datum) THEN 
                        DO: 
                            IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 
                                AND NOT res-line.zimmerfix THEN 
                            DO:
                                ASSIGN 
                                    output-list.room     = output-list.room + res-line.zimmeranz
                                    output-list.revenue  = output-list.revenue + net-lodg /*  res-line.zipreis, CHANGED TO ROOM REVENUE */
                                    output-list.avrg-rev = output-list.revenue / output-list.room
                                .
                            END.
                            
                            IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN
                            DO:
                                output-list.pax          = output-list.pax + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
                                                           + res-line.gratis) * res-line.zimmeranz.
                            END.
                        END. /* Inhouse */ 
                    END.
                END.
            END.            
        END.
    END. 
END.

PROCEDURE count-mtd-totrm:
    DEFINE INPUT PARAMETER in-date AS DATE.
    DEFINE VARIABLE datum AS DATE.
    DEFINE VARIABLE ldatum AS DATE.
    DEFINE VARIABLE OOO  AS INTEGER INIT 0.
    ASSIGN mtd-totrm = 0 mtd-act = 0 all-rm = 0.

    IF MONTH(in-date) EQ 12 THEN
        datum = DATE(1,1,YEAR(in-date) + 1) - 1.
    ELSE
        datum = DATE(MONTH(in-date) + 1,1,YEAR(in-date)) - 1.

    IF (MONTH(in-date) LT MONTH(ci-date) AND YEAR(in-date) EQ YEAR(ci-date))
        OR (YEAR(in-date) LT YEAR(ci-date)) THEN 
    DO:
        FOR EACH zkstat WHERE MONTH(zkstat.datum) EQ MONTH(in-date) AND YEAR(zkstat.datum) EQ YEAR(in-date) NO-LOCK:
            all-rm = all-rm + zkstat.anz100.
        END.
        FOR EACH zinrstat WHERE zinrstat.zinr =  "tot-rm" AND 
            MONTH(zinrstat.datum) EQ MONTH(in-date) AND YEAR(zinrstat.datum) EQ YEAR(in-date) NO-LOCK:
            mtd-totrm = mtd-totrm + zinrstat.zimmeranz.
        END.
        FOR EACH zinrstat WHERE zinrstat.zinr = "ooo" AND 
            MONTH(zinrstat.datum) EQ MONTH(in-date) AND YEAR(zinrstat.datum) EQ YEAR(in-date) NO-LOCK:
            OOO = OOO + zinrstat.zimmeranz.
        END.
    END.
    ELSE IF MONTH(in-date) EQ MONTH(ci-date) AND YEAR(in-date) EQ YEAR(ci-date) THEN 
    DO:
        FOR EACH zkstat WHERE zkstat.datum GE in-date AND zkstat.datum LE ci-date NO-LOCK:
            all-rm = all-rm + zkstat.anz100.
        END.
        FOR EACH zinrstat WHERE zinrstat.zinr =  "tot-rm" AND 
            zinrstat.datum GE in-date AND zinrstat.datum LE ci-date NO-LOCK:
            mtd-totrm = mtd-totrm + zinrstat.zimmeranz.
        END. 
        FOR EACH zinrstat WHERE zinrstat.zinr = "ooo" AND 
            zinrstat.datum GE in-date AND zinrstat.datum LE ci-date NO-LOCK:
            OOO = OOO + zinrstat.zimmeranz.
        END.
        /* rest of the date in month */
        all-rm    = all-rm + (act-rm * (datum - ci-date)).
        mtd-totrm = mtd-totrm + (tot-room * (datum - ci-date)).
        
        DO ldatum = ci-date + 1 TO datum:
            FOR EACH outorder WHERE outorder.gespstart LE ldatum 
            AND outorder.gespende GE ldatum AND outorder.betriebsnr LE 1 
            NO-LOCK, 
            FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping 
            NO-LOCK: 
                OOO = OOO + 1. 
            END.
        END.
    END.
    ELSE 
    DO:
        all-rm = act-rm * (datum - in-date + 1).
        mtd-totrm = mtd-totrm + (tot-room * (datum - in-date + 1)).
        DO ldatum = in-date TO datum:
            FOR EACH outorder WHERE outorder.gespstart LE ldatum 
            AND outorder.gespende GE ldatum AND outorder.betriebsnr LE 1 
            NO-LOCK, 
            FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping 
            NO-LOCK: 
                OOO = OOO + 1. 
            END.
        END.
    END.
    mtd-act = all-rm - OOO.
END.


