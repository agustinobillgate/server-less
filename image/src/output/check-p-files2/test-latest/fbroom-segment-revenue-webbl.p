DEFINE TEMP-TABLE t-payload-list
    FIELD from-date     AS DATE
    FIELD to-date       AS DATE
    FIELD sort-type     AS INTEGER
    .

DEFINE TEMP-TABLE revenue-segmlist
    FIELD segment-code          AS INTEGER
    FIELD segmemt-short-desc    AS CHARACTER
    FIELD segment-description   AS CHARACTER
    FIELD segment-group         AS CHARACTER
    FIELD rsv-segmroom-rev      AS DECIMAL
    FIELD rsv-segmfood-rev      AS DECIMAL
    FIELD rsv-segmbev-rev       AS DECIMAL
    FIELD rsv-segmother-rev     AS DECIMAL
    FIELD rsv-segmfcost-rev     AS DECIMAL
    FIELD rsv-segmtotal-rev     AS DECIMAL
    FIELD outlet-segmfood-rev   AS DECIMAL
    FIELD outlet-segmbev-rev    AS DECIMAL
    FIELD outlet-segmother-rev  AS DECIMAL
    FIELD outlet-segmtotal-rev  AS DECIMAL
    FIELD grand-total           AS DECIMAL
    .

DEFINE TEMP-TABLE revenue-room-other
    FIELD segment-code          AS INTEGER
    FIELD segmemt-short-desc    AS CHARACTER
    FIELD segment-room-other    AS DECIMAL
    .

DEFINE INPUT PARAMETER TABLE FOR t-payload-list.
DEFINE OUTPUT PARAMETER TABLE FOR revenue-segmlist.

DEFINE VARIABLE curr-date       AS DATE.
DEFINE VARIABLE bill-date       AS DATE. 
DEFINE VARIABLE ci-date         AS DATE.
DEFINE VARIABLE from-date       AS DATE.
DEFINE VARIABLE to-date         AS DATE.

FIND FIRST htparam WHERE htparam.paramnr EQ 87 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ci-date = htparam.fdate.
FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN bill-date = htparam.fdate.

FIND FIRST t-payload-list.

FOR EACH segment WHERE NOT segment.bezeich MATCHES "*$$0*" NO-LOCK:
    CREATE revenue-segmlist.
    ASSIGN
        revenue-segmlist.segment-code           = segment.segmentcode
        revenue-segmlist.segmemt-short-desc     = segment.bezeich
        revenue-segmlist.segment-description    = segment.bemerkung        
        .

    FIND FIRST queasy WHERE queasy.KEY EQ 26 
        AND queasy.number1 EQ segment.segmentgrup NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN revenue-segmlist.segment-group = queasy.char3.    
END.
CREATE revenue-segmlist.
ASSIGN
    revenue-segmlist.segment-code       = 9999
    revenue-segmlist.segmemt-short-desc = "UNKNOWN"
    .

DO curr-date = t-payload-list.from-date TO t-payload-list.to-date:
    IF curr-date LT ci-date THEN RUN create-history.
    ELSE RUN create-forecast.
END.
RUN create-bill-fo.
RUN create-bill-outlet.

/*************************************** PROCEDURES ***************************************/
PROCEDURE create-history:
DEFINE VARIABLE ex-rate         AS DECIMAL INITIAL 1 NO-UNDO. 
DEFINE VARIABLE argt-betrag     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE nett-betrag     AS DECIMAL NO-UNDO.
DEFINE VARIABLE vat-art         AS DECIMAL NO-UNDO.
DEFINE VARIABLE service-art     AS DECIMAL NO-UNDO.
DEFINE VARIABLE vat2-art        AS DECIMAL NO-UNDO.
DEFINE VARIABLE fact-art        AS DECIMAL NO-UNDO.
DEFINE VARIABLE post-it         AS LOGICAL NO-UNDO.

    FOR EACH genstat WHERE genstat.datum EQ curr-date
        AND genstat.resstatus NE 13
        AND genstat.segmentcode NE 0
        AND genstat.nationnr NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] NO-LOCK,
        FIRST arrangement WHERE arrangement.arrangement EQ genstat.argt NO-LOCK
        BY genstat.segmentcode:

        FIND FIRST revenue-segmlist WHERE revenue-segmlist.segment-code EQ genstat.segmentcode NO-LOCK NO-ERROR.
        IF AVAILABLE revenue-segmlist THEN
        DO:
            revenue-segmlist.rsv-segmroom-rev = revenue-segmlist.rsv-segmroom-rev + genstat.logis.
            revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + genstat.logis.
            revenue-segmlist.grand-total = revenue-segmlist.grand-total + genstat.logis.

            FOR EACH argt-line WHERE argt-line.argtnr EQ arrangement.argtnr 
                AND NOT argt-line.kind2 AND argt-line.kind1 NO-LOCK,
                FIRST artikel WHERE artikel.artnr EQ argt-line.argt-artnr 
                AND artikel.departement EQ argt-line.departement NO-LOCK:

                RUN argt-betrag.p(RECID(res-line), RECID(argt-line), OUTPUT argt-betrag, OUTPUT ex-rate).
                RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
                                        genstat.datum, OUTPUT service-art, OUTPUT vat-art, 
                                        OUTPUT vat2-art, OUTPUT fact-art).

                nett-betrag = argt-betrag / fact-art.
                IF (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) THEN
                DO:
                    ASSIGN
                        revenue-segmlist.rsv-segmfood-rev = revenue-segmlist.rsv-segmfood-rev + argt-betrag
                        revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + argt-betrag
                        revenue-segmlist.grand-total = revenue-segmlist.grand-total + argt-betrag 
                        .
                END.
                ELSE IF artikel.umsatzart EQ 6 THEN
                DO:
                    ASSIGN
                        revenue-segmlist.rsv-segmbev-rev = revenue-segmlist.rsv-segmbev-rev + argt-betrag
                        revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + argt-betrag
                        revenue-segmlist.grand-total = revenue-segmlist.grand-total + argt-betrag
                        .
                END.
                ELSE
                DO:
                    ASSIGN
                        revenue-segmlist.rsv-segmother-rev = revenue-segmlist.rsv-segmother-rev + argt-betrag
                        revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + argt-betrag
                        revenue-segmlist.grand-total = revenue-segmlist.grand-total + argt-betrag
                        .
                END.
            END.
            /* Get from bill for fix cost
            FOR EACH fixleist WHERE fixleist.resnr EQ res-line.resnr 
                AND fixleist.reslinnr EQ res-line.reslinnr NO-LOCK: 
                RUN check-fixleist-posted(fixleist.artnr, fixleist.departement, 
                    fixleist.sequenz, fixleist.dekade, 
                    fixleist.lfakt, OUTPUT post-it). 

                IF post-it THEN 
                DO: 
                    FIND FIRST artikel WHERE artikel.artnr EQ fixleist.artnr 
                        AND artikel.departement EQ fixleist.departement NO-LOCK NO-ERROR.
                    IF AVAILABLE artikel THEN
                    DO:
                        RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
                                        genstat.datum, OUTPUT service-art, OUTPUT vat-art, 
                                        OUTPUT vat2-art, OUTPUT fact-art).

                        nett-betrag = fixleist.betrag / fact-art.

                        IF (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) THEN
                        DO:
                            revenue-segmlist.rsv-segmfood-rev = revenue-segmlist.rsv-segmfood-rev + (fixleist.betrag * fixleist.number).
                        END.
                        ELSE IF artikel.umsatzart EQ 6 THEN
                        DO:
                            revenue-segmlist.rsv-segmbev-rev = revenue-segmlist.rsv-segmbev-rev + (fixleist.betrag * fixleist.number).
                        END.
                        ELSE
                        DO:
                            revenue-segmlist.rsv-segmother-rev = revenue-segmlist.rsv-segmother-rev + (fixleist.betrag * fixleist.number).
                        END.
                    END.
                END.
            END.
            */            
        END.        
    END.
END PROCEDURE.

PROCEDURE create-forecast:
DEFINE VARIABLE net-lodg        AS DECIMAL.
DEFINE VARIABLE Fnet-lodg       AS DECIMAL.
DEFINE VARIABLE tot-breakfast   AS DECIMAL.
DEFINE VARIABLE tot-Lunch       AS DECIMAL.
DEFINE VARIABLE tot-dinner      AS DECIMAL.
DEFINE VARIABLE tot-Other       AS DECIMAL.
DEFINE VARIABLE tot-rmrev       AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-vat         AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-service     AS DECIMAL INITIAL 0.
DEFINE VARIABLE ex-rate         AS DECIMAL INITIAL 1 NO-UNDO. 
DEFINE VARIABLE argt-betrag     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE nett-betrag     AS DECIMAL NO-UNDO.
DEFINE VARIABLE vat-art         AS DECIMAL NO-UNDO.
DEFINE VARIABLE service-art     AS DECIMAL NO-UNDO.
DEFINE VARIABLE vat2-art        AS DECIMAL NO-UNDO.
DEFINE VARIABLE fact-art        AS DECIMAL NO-UNDO.
DEFINE VARIABLE post-it         AS LOGICAL NO-UNDO.

    FOR EACH res-line WHERE (res-line.resstatus LE 13 
        AND res-line.resstatus NE 4
        AND res-line.resstatus NE 8
        AND res-line.resstatus NE 9 
        AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 12 
        AND res-line.active-flag LE 1 
        AND res-line.ankunft GE curr-date
        AND res-line.abreise LE curr-date) 
        OR (res-line.resstatus EQ 8 AND res-line.active-flag EQ 2
        AND res-line.ankunft EQ ci-date AND res-line.abreise EQ ci-date)
        AND res-line.l-zuordnung[3] EQ 0
        AND res-line.gastnr GT 0 NO-LOCK,
        FIRST reservation WHERE reservation.resnr EQ res-line.resnr
        AND reservation.segmentcode NE 0 NO-LOCK BY reservation.segmentcode:

        IF curr-date EQ res-line.abreise THEN.
        ELSE
        DO:
            ASSIGN 
                net-lodg      = 0
                tot-breakfast = 0
                tot-lunch     = 0
                tot-dinner    = 0
                tot-other     = 0
                .

            RUN get-room-breakdown.p(RECID(res-line), curr-date, 0, from-date,
                                    OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                    OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                    OUTPUT tot-dinner, OUTPUT tot-other,
                                    OUTPUT tot-rmrev, OUTPUT tot-vat,
                                    OUTPUT tot-service).

            FIND FIRST revenue-segmlist WHERE revenue-segmlist.segment-code EQ reservation.segmentcode NO-LOCK NO-ERROR.
            IF AVAILABLE revenue-segmlist THEN
            DO:
                revenue-segmlist.rsv-segmroom-rev = revenue-segmlist.rsv-segmroom-rev + net-lodg.
                revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + net-lodg.
                revenue-segmlist.grand-total = revenue-segmlist.grand-total + net-lodg.

                FOR EACH argt-line WHERE argt-line.argtnr EQ arrangement.argtnr 
                    AND NOT argt-line.kind2 AND argt-line.kind1 NO-LOCK,
                    FIRST artikel WHERE artikel.artnr EQ argt-line.argt-artnr 
                    AND artikel.departement EQ argt-line.departement NO-LOCK:
    
                    RUN argt-betrag.p(RECID(res-line), RECID(argt-line), OUTPUT argt-betrag, OUTPUT ex-rate).
                    RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
                                            genstat.datum, OUTPUT service-art, OUTPUT vat-art, 
                                            OUTPUT vat2-art, OUTPUT fact-art).
    
                    nett-betrag = argt-betrag / fact-art.
                    IF (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) THEN
                    DO:
                        ASSIGN
                            revenue-segmlist.rsv-segmfood-rev = revenue-segmlist.rsv-segmfood-rev + argt-betrag
                            revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + argt-betrag
                            revenue-segmlist.grand-total = revenue-segmlist.grand-total + argt-betrag 
                            .
                    END.
                    ELSE IF artikel.umsatzart EQ 6 THEN
                    DO:
                        ASSIGN
                            revenue-segmlist.rsv-segmbev-rev = revenue-segmlist.rsv-segmbev-rev + argt-betrag
                            revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + argt-betrag
                            revenue-segmlist.grand-total = revenue-segmlist.grand-total + argt-betrag
                            .
                    END.
                    ELSE
                    DO:
                        ASSIGN
                            revenue-segmlist.rsv-segmother-rev = revenue-segmlist.rsv-segmother-rev + argt-betrag
                            revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + argt-betrag
                            revenue-segmlist.grand-total = revenue-segmlist.grand-total + argt-betrag
                            .
                    END.
                END.                
            END.
        END.
    END.
END PROCEDURE.

PROCEDURE create-bill-fo:
    FOR EACH bill-line WHERE bill-line.bill-datum GE t-payload-list.from-date 
        AND bill-line.bill-datum LE t-payload-list.to-date NO-LOCK,
        FIRST artikel WHERE artikel.artnr EQ bill-line.artnr
        AND artikel.departement EQ bill-line.departement NO-LOCK,
        FIRST bill WHERE bill.rechnr EQ bill-line.rechnr NO-LOCK:
    
        /*Guest & Master Folio*/
        FIND FIRST res-line WHERE (res-line.resnr EQ bill.resnr 
            AND res-line.reslinnr EQ bill.parent-nr)
            OR (res-line.resnr EQ bill.resnr AND bill.reslinnr EQ 0) NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN
        DO:
            FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr 
                AND reservation.segmentcode NE 0 NO-LOCK NO-ERROR.
            IF AVAILABLE reservation THEN
            DO:
                FIND FIRST revenue-segmlist WHERE revenue-segmlist.segment-code EQ reservation.segmentcode NO-LOCK NO-ERROR.
                IF AVAILABLE revenue-segmlist THEN
                DO:
                    IF (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) THEN
                    DO:
                        ASSIGN
                            revenue-segmlist.rsv-segmfood-rev = revenue-segmlist.rsv-segmfood-rev + bill-line.betrag
                            revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + bill-line.betrag
                            revenue-segmlist.grand-total = revenue-segmlist.grand-total + bill-line.betrag 
                            .                        
                    END.
                    ELSE IF artikel.umsatzart EQ 6 THEN
                    DO:                        
                        ASSIGN
                            revenue-segmlist.rsv-segmbev-rev = revenue-segmlist.rsv-segmbev-rev + bill-line.betrag
                            revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + bill-line.betrag
                            revenue-segmlist.grand-total = revenue-segmlist.grand-total + bill-line.betrag 
                            .
                    END.
                    ELSE IF artikel.umsatzart EQ 4 THEN
                    DO:                        
                        ASSIGN
                            revenue-segmlist.rsv-segmother-rev = revenue-segmlist.rsv-segmother-rev + bill-line.betrag
                            revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + bill-line.betrag
                            revenue-segmlist.grand-total = revenue-segmlist.grand-total + bill-line.betrag 
                            .
                    END.                    
                END.
            END.
        END.
    
        /*NonStay Guest Folio*/
        IF bill.resnr EQ 0 AND bill.reslinnr NE 0 AND bill.gastnr NE 0 THEN
        DO:
            /*Company & TA have main segment*/
            FIND FIRST guest WHERE guest.gastnr EQ bill.gastnr
                AND guest.karteityp GE 1 NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN
            DO:
                FIND FIRST guestseg WHERE guestseg.gastnr EQ guest.gastnr 
                    AND guestseg.reihenfolge EQ 1
                    AND guestseg.segmentcode NE 0 NO-LOCK NO-ERROR.
                IF AVAILABLE guestseg THEN
                DO:
                    FIND FIRST revenue-segmlist WHERE revenue-segmlist.segment-code EQ reservation.segmentcode NO-LOCK NO-ERROR.
                    IF AVAILABLE revenue-segmlist THEN
                    DO:
                        IF (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) THEN
                        DO:
                            ASSIGN
                                revenue-segmlist.rsv-segmfood-rev = revenue-segmlist.rsv-segmfood-rev + bill-line.betrag
                                revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + bill-line.betrag
                                revenue-segmlist.grand-total = revenue-segmlist.grand-total + bill-line.betrag 
                                . 
                        END.
                        ELSE IF artikel.umsatzart EQ 6 THEN
                        DO:
                            ASSIGN
                                revenue-segmlist.rsv-segmbev-rev = revenue-segmlist.rsv-segmbev-rev + bill-line.betrag
                                revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + bill-line.betrag
                                revenue-segmlist.grand-total = revenue-segmlist.grand-total + bill-line.betrag 
                                .
                        END.
                        ELSE IF artikel.umsatzart EQ 4 THEN
                        DO:
                            ASSIGN
                                revenue-segmlist.rsv-segmother-rev = revenue-segmlist.rsv-segmother-rev + bill-line.betrag
                                revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + bill-line.betrag
                                revenue-segmlist.grand-total = revenue-segmlist.grand-total + bill-line.betrag 
                                .
                        END.                               
                    END.
                END.
            END.
            ELSE /*Individual Guest haven't segment*/
            DO:
                FIND FIRST revenue-segmlist WHERE revenue-segmlist.segment-code EQ 9999 NO-LOCK NO-ERROR.
                IF AVAILABLE revenue-segmlist THEN
                DO: 
                    IF (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) THEN
                    DO:
                        ASSIGN
                            revenue-segmlist.rsv-segmfood-rev = revenue-segmlist.rsv-segmfood-rev + bill-line.betrag
                            revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + bill-line.betrag
                            revenue-segmlist.grand-total = revenue-segmlist.grand-total + bill-line.betrag 
                            . 
                    END.
                    ELSE IF artikel.umsatzart EQ 6 THEN
                    DO:
                        ASSIGN
                            revenue-segmlist.rsv-segmbev-rev = revenue-segmlist.rsv-segmbev-rev + bill-line.betrag
                            revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + bill-line.betrag
                            revenue-segmlist.grand-total = revenue-segmlist.grand-total + bill-line.betrag 
                            .
                    END.
                    ELSE IF artikel.umsatzart EQ 4 THEN
                    DO:
                        ASSIGN
                            revenue-segmlist.rsv-segmother-rev = revenue-segmlist.rsv-segmother-rev + bill-line.betrag
                            revenue-segmlist.rsv-segmtotal-rev = revenue-segmlist.rsv-segmtotal-rev + bill-line.betrag
                            revenue-segmlist.grand-total = revenue-segmlist.grand-total + bill-line.betrag 
                            .
                    END.                        
                END.
            END.
        END.
    END.
END PROCEDURE.

PROCEDURE create-bill-outlet:
DEFINE VARIABLE guest-no AS INTEGER.

    FIND FIRST h-journal WHERE h-journal.bill-datum GE t-payload-list.from-date 
        AND h-journal.bill-datum LE t-payload-list.to-date NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE h-journal:
    
        guest-no = 0.
        FIND FIRST h-bill WHERE h-bill.rechnr EQ h-journal.rechnr  
            AND h-bill.departement EQ h-journal.departement 
            AND h-bill.bilname NE "" NO-LOCK NO-ERROR.
        IF AVAILABLE h-bill THEN
        DO:
            FIND FIRST h-artikel WHERE h-artikel.artnr EQ h-journal.artnr 
                AND h-artikel.departement EQ h-journal.departement
                AND h-artikel.artart EQ 0 NO-LOCK NO-ERROR.
            IF AVAILABLE h-artikel THEN
            DO:
                FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                    AND artikel.departement EQ h-artikel.departement NO-LOCK NO-ERROR.
                IF AVAILABLE artikel THEN
                DO:
                    IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN /*Inhouse*/
                    DO:
                        FIND FIRST res-line WHERE res-line.resnr EQ h-bill.resnr
                            AND res-line.reslinnr EQ h-bill.reslinnr NO-LOCK NO-ERROR.
                        IF AVAILABLE res-line THEN guest-no = res-line.gastnrmember.
                    END.
                    ELSE IF h-bill.resnr GT 0 THEN  /*only consume*/
                    DO:
                        guest-no = h-bill.resnr.
                    END.

                    IF guest-no NE 0 AND h-bill.segmentcode NE 0 THEN
                    DO:
                        FIND FIRST revenue-segmlist WHERE revenue-segmlist.segment-code EQ h-bill.segmentcode NO-LOCK NO-ERROR.
                        IF AVAILABLE revenue-segmlist THEN
                        DO:
                            IF (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) THEN
                            DO:
                                ASSIGN
                                    revenue-segmlist.outlet-segmfood-rev = revenue-segmlist.outlet-segmfood-rev + h-journal.betrag
                                    revenue-segmlist.outlet-segmtotal-rev = revenue-segmlist.outlet-segmtotal-rev + h-journal.betrag
                                    revenue-segmlist.grand-total = revenue-segmlist.grand-total + h-journal.betrag
                                    .
                            END.
                            ELSE IF artikel.umsatzart EQ 6 THEN
                            DO:
                                ASSIGN
                                    revenue-segmlist.outlet-segmbev-rev = revenue-segmlist.outlet-segmbev-rev + h-journal.betrag
                                    revenue-segmlist.outlet-segmtotal-rev = revenue-segmlist.outlet-segmtotal-rev + h-journal.betrag
                                    revenue-segmlist.grand-total = revenue-segmlist.grand-total + h-journal.betrag
                                    .
                            END.
                            ELSE IF artikel.umsatzart EQ 4 THEN
                            DO:
                                ASSIGN
                                    revenue-segmlist.outlet-segmother-rev = revenue-segmlist.outlet-segmother-rev + h-journal.betrag
                                    revenue-segmlist.outlet-segmtotal-rev = revenue-segmlist.outlet-segmtotal-rev + h-journal.betrag
                                    revenue-segmlist.grand-total = revenue-segmlist.grand-total + h-journal.betrag
                                    .
                            END.
                        END.                        
                    END.
                    ELSE /**UNKNOWN*/
                    DO:
                        FIND FIRST revenue-segmlist WHERE revenue-segmlist.segment-code EQ 9999 NO-LOCK NO-ERROR.
                        IF AVAILABLE revenue-segmlist THEN
                        DO:
                            IF (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) THEN
                            DO:
                                ASSIGN
                                    revenue-segmlist.outlet-segmfood-rev = revenue-segmlist.outlet-segmfood-rev + h-journal.betrag
                                    revenue-segmlist.outlet-segmtotal-rev = revenue-segmlist.outlet-segmtotal-rev + h-journal.betrag
                                    revenue-segmlist.grand-total = revenue-segmlist.grand-total + h-journal.betrag
                                    .
                            END.
                            ELSE IF artikel.umsatzart EQ 6 THEN
                            DO:
                                ASSIGN
                                    revenue-segmlist.outlet-segmbev-rev = revenue-segmlist.outlet-segmbev-rev + h-journal.betrag
                                    revenue-segmlist.outlet-segmtotal-rev = revenue-segmlist.outlet-segmtotal-rev + h-journal.betrag
                                    revenue-segmlist.grand-total = revenue-segmlist.grand-total + h-journal.betrag
                                    .
                            END.
                            ELSE IF artikel.umsatzart EQ 4 THEN
                            DO:
                                ASSIGN
                                    revenue-segmlist.outlet-segmother-rev = revenue-segmlist.outlet-segmother-rev + h-journal.betrag
                                    revenue-segmlist.outlet-segmtotal-rev = revenue-segmlist.outlet-segmtotal-rev + h-journal.betrag
                                    revenue-segmlist.grand-total = revenue-segmlist.grand-total + h-journal.betrag
                                    .
                            END.
                        END.  
                    END.                    
                END.                
            END.
        END.

        FIND NEXT h-journal WHERE h-journal.bill-datum GE t-payload-list.from-date 
            AND h-journal.bill-datum LE t-payload-list.to-date NO-LOCK NO-ERROR.
    END.
END PROCEDURE.

/*
PROCEDURE check-fixleist-posted: 
DEFINE INPUT PARAMETER artnr        AS INTEGER. 
DEFINE INPUT PARAMETER dept         AS INTEGER. 
DEFINE INPUT PARAMETER fakt-modus   AS INTEGER. 
DEFINE INPUT PARAMETER intervall    AS INTEGER. 
DEFINE INPUT PARAMETER lfakt        AS DATE. 
DEFINE OUTPUT PARAMETER post-it     AS LOGICAL INITIAL NO. 

DEFINE VARIABLE delta       AS INTEGER. 
DEFINE VARIABLE start-date  AS DATE. 
DEFINE VARIABLE curr-date   AS DATE. 
 
    curr-date = bill-date.

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
*/
