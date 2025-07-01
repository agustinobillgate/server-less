DEFINE TEMP-TABLE his-res
    FIELD number        AS INTEGER
    FIELD resnr         AS INTEGER
    FIELD reslinnr      AS INTEGER
    FIELD staydate      AS DATE
    FIELD ci-date       AS DATE
    FIELD co-date       AS DATE
    FIELD nbrofroom     AS INTEGER
    FIELD room-type     AS CHARACTER
    FIELD rm-rev        AS DECIMAL
    FIELD fb-rev        AS DECIMAL
    FIELD other-rev     AS DECIMAL
    FIELD resstatus     AS CHARACTER
    FIELD reserveID     AS INTEGER
    FIELD reserveName   AS CHARACTER
    FIELD bookdate      AS DATE
    FIELD rate-code     AS CHARACTER
    FIELD nationality   AS CHARACTER
    FIELD segmentcode   AS CHARACTER
    FIELD cancel-date   AS CHARACTER
    FIELD zinr          AS CHARACTER
.
DEFINE TEMP-TABLE his-inv    
    FIELD datum         AS DATE
    FIELD room-type     AS CHARACTER
    FIELD room-status   AS CHARACTER
    FIELD qty           AS INTEGER
    FIELD zikatnr       AS INTEGER
.

DEFINE TEMP-TABLE temp-res LIKE his-res.
DEFINE TEMP-TABLE future-res LIKE his-res.
DEFINE TEMP-TABLE future-inv LIKE his-inv.

DEFINE TEMP-TABLE non-room
    FIELD postingdate      AS DATE
    FIELD departmentID     AS INTEGER
    FIELD departmentName   AS CHARACTER
    FIELD rm-rev           AS DECIMAL
    FIELD fb-rev           AS DECIMAL
    FIELD other-rev        AS DECIMAL
.

DEF TEMP-TABLE t-list
    FIELD departement   AS INTEGER
    FIELD rechnr        AS INTEGER
    FIELD bill-datum    AS DATE
    FIELD sysdate       AS DATE
    FIELD zeit          AS INTEGER
    FIELD fb            AS DECIMAL INITIAL 0
    FIELD other         AS DECIMAL INITIAL 0
    FIELD fb-service    AS DECIMAL INITIAL 0
    FIELD other-service AS DECIMAL INITIAL 0
    FIELD pay           AS DECIMAL INITIAL 0
    FIELD compli        AS DECIMAL INITIAL 0
.

/*TAMBAH INPUTAN UNTUK RANGE DATE YANG MAU DIAMBIL*/
DEFINE INPUT PARAMETER exclude-article AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR his-res.
DEFINE OUTPUT PARAMETER TABLE FOR his-inv.
DEFINE OUTPUT PARAMETER TABLE FOR future-res.
DEFINE OUTPUT PARAMETER TABLE FOR future-inv.
DEFINE OUTPUT PARAMETER TABLE FOR non-room.


/*DEFINE VARIABLE exclude-article AS CHARACTER INIT "".*/

DEFINE VARIABLE datum   AS DATE             NO-UNDO.
DEFINE VARIABLE datum2  AS DATE             NO-UNDO.
DEFINE VARIABLE ci-date AS DATE             NO-UNDO.
DEFINE VARIABLE i       AS INTEGER INIT 0   NO-UNDO.
DEFINE VARIABLE j       AS INTEGER INIT 0   NO-UNDO.
DEFINE VARIABLE iftask  AS CHARACTER        NO-UNDO.
DEFINE VARIABLE last-rechnr AS INTEGER INIT 0  NO-UNDO.

DEFINE BUFFER gbuff FOR guest.
DEFINE BUFFER bufhis-inv FOR his-inv.
DEFINE BUFFER buffuture-inv FOR future-inv.
DEFINE BUFFER bufres-line FOR res-line.

DEFINE VARIABLE curr-i          AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE curr-date       AS DATE    NO-UNDO.   
DEFINE VARIABLE end-date        AS DATE    NO-UNDO.
DEFINE VARIABLE Fnet-lodg       AS DECIMAL NO-UNDO.
DEFINE VARIABLE net-lodg        AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-breakfast   AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-lunch       AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-dinner      AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-other       AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-rmrev       AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-vat         AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-service     AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-fb          AS DECIMAL NO-UNDO.
DEFINE VARIABLE do-it1          AS LOGICAL INIT NO NO-UNDO.

DEFINE VARIABLE vat-proz                AS DECIMAL    NO-UNDO INIT 10.
DEFINE VARIABLE do-it                   AS LOGICAL    NO-UNDO.
DEFINE VARIABLE serv-taxable            AS LOGICAL    NO-UNDO.
DEFINE VARIABLE serv                    AS DECIMAL    NO-UNDO.
DEFINE VARIABLE vat                     AS DECIMAL    NO-UNDO.
DEFINE VARIABLE netto                   AS DECIMAL    NO-UNDO.
DEFINE VARIABLE serv-betrag             AS DECIMAL    NO-UNDO.
DEFINE VARIABLE outStr                  AS CHAR       NO-UNDO.
DEFINE VARIABLE outStr1                 AS CHAR       NO-UNDO.
DEFINE VARIABLE revCode                 AS CHAR       NO-UNDO.
DEFINE VARIABLE rechnr-notTax           AS INTEGER    NO-UNDO.
DEFINE VARIABLE bill-date               AS DATE       NO-UNDO.
DEFINE VARIABLE pay-amount              AS DECIMAL    NO-UNDO.

DEFINE VARIABLE bill-resnr       AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-reslinnr    AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-parentnr    AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-gastnr      AS INTEGER NO-UNDO.
DEFINE VARIABLE ex-article       AS CHARACTER NO-UNDO.
DEFINE VARIABLE t-reslinnr       AS INTEGER NO-UNDO.

DEFINE VARIABLE lastYear         AS INTEGER NO-UNDO.
DEFINE VARIABLE initDate         AS CHAR NO-UNDO.
DEFINE VARIABLE currDate         AS DATE NO-UNDO INIT TODAY.
DEFINE VARIABLE storage-dur      AS INTEGER NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
ci-date = htparam.fdate.

/*for genarate data 1 yeras ago to be continue current date -> fadly 19/07/19*/
lastYear = YEAR(ci-date) - 1.
initDate = "01/01/" + STRING(lastYear).
/*End*/

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK.  /*Invoicing DATE */ 
bill-date = htparam.fdate - 1.

/*for genarate data range storage duration -> fadly 07/08/19*/
FIND FIRST htparam WHERE htparam.paramnr = 162 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN storage-dur = htparam.finteger.
/*END*/

/*FILE 1*/
/* VAT code*/
FIND FIRST htparam WHERE htparam.paramnr = 1 NO-LOCK.
IF htparam.fdecimal NE 0 THEN vat-proz = htparam.fdecimal.

FOR EACH billjournal NO-LOCK WHERE billjournal.bill-datum GE (ci-date - storage-dur)
    AND billjournal.bill-datum LE bill-date
    AND billjournal.anzahl NE 0 AND billjournal.betrag NE 0 USE-INDEX dateart_ix:
    
    do-it = YES.

    IF last-rechnr NE billjournal.rechnr THEN
    DO:
        FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE bill THEN
        DO:
            /*do-it = NO.*/
            /*for consigment revenue if not have bill, include to NonRoom -> fadly 01/07/2019*/
            ASSIGN
                bill-resnr = 0
                bill-reslinnr = 0
                bill-parentnr = 0
                bill-gastnr   = 0.
            /*END fadly*/
        END.            
        ELSE
        DO:
            ASSIGN
                bill-resnr = bill.resnr
                bill-reslinnr = bill.reslinnr
                bill-parentnr = bill.parent-nr
                bill-gastnr   = bill.gastnr.     
        END.           

        last-rechnr = billjournal.rechnr.
    END.        

    IF do-it THEN 
    DO:
        FIND FIRST artikel WHERE artikel.artnr = billjournal.artnr
            AND artikel.departement = billjournal.departement NO-LOCK NO-ERROR.
            do-it = AVAILABLE artikel /*FTAND 
                (artikel.mwst-code NE 0 OR artikel.service-code NE 0)*/.       
            
        IF do-it THEN
        DO:
            do-it = (artikel.artart = 0 OR artikel.artart = 8).
        END.
        IF do-it THEN
        DO:
            IF exclude-article NE "" THEN
            DO j = 1 TO NUM-ENTRIES(exclude-article,";"):
                ex-article = ENTRY(j, exclude-article, ";").
                IF artikel.artnr = INT(ENTRY(1, ex-article, "-"))
                    AND artikel.departement = INT(ENTRY(2, ex-article, "-")) THEN
                    do-it = NO.
            END.
        END.
    END.
    
    IF do-it AND artikel.bezeich MATCHES("*Remain*")
        AND artikel.bezeich MATCHES("*Balance*") THEN do-it = NO.
    
    IF do-it THEN
    DO:
        FIND FIRST hoteldpt WHERE hoteldpt.num = artikel.departement NO-LOCK.
        ASSIGN revCode = "ATZ". /*revCode ATZ = "Other".*/ 
    
        IF artikel.artart = 0 THEN
        DO:
            IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 
                OR artikel.umsatzart = 6 THEN revCode = "ATM". /*revCode = "FB".*/

            IF artikel.departement = 0 AND artikel.umsatzart = 1 THEN revCode = "ATS". /*revCode = "Lodging".*/
        END.
        ELSE IF artikel.artart = 8 THEN revCode = "ATS". /*revCode = "Lodging".*/                
        
        ASSIGN
            serv        = 0
            vat         = 0
            netto       = 0
            serv-betrag = 0
        .
        
        RUN calc-servvat.p (artikel.departement, artikel.artnr, billjournal.bill-datum,
            artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
        
        IF vat = 1 THEN
            ASSIGN netto = billjournal.betrag * 100 / vat-proz.
        ELSE 
        DO:    
            IF serv = 1 THEN ASSIGN serv-betrag = netto.
            ELSE IF vat GT 0 THEN
            ASSIGN 
                netto = billjournal.betrag / (1 + serv + vat)
                serv-betrag = netto * serv
            .
            IF serv = 0 OR vat = 0 THEN
                netto = billjournal.betrag / (1 + serv + vat).
        END.
        
        IF netto NE 0 THEN
        DO:
            DO:
                IF (bill-reslinnr = 0 AND bill-resnr GT 0 AND billjournal.zinr = "")
                    OR (bill-reslinnr = 0 AND bill-resnr GT 0 AND billjournal.comment = "") THEN /* MASTER BILL */
                DO:          
                    FIND FIRST his-res WHERE his-res.staydate = billjournal.bill-datum
                        AND his-res.resnr = bill-resnr
                        AND his-res.reslinnr = 0 NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE his-res THEN
                    DO:
                        CREATE his-res.
                        ASSIGN
                            his-res.staydate = billjournal.bill-datum
                            his-res.resnr = bill-resnr                            
                            his-res.reslinnr = 0
                            his-res.nbrofroom = 0
                            his-res.reserveID = bill-gastnr
                            his-res.resstatus = "CHECKEDOUT".
                        
                        FIND FIRST guest WHERE guest.gastnr = bill-gastnr NO-LOCK NO-ERROR.
                        IF AVAILABLE guest THEN
                        DO:
                            IF guest.vorname1 NE "" THEN
                                his-res.reservename = guest.NAME + " " + guest.vorname1.
                            ELSE
                                his-res.reservename = guest.NAME.
                        END.   

                        FIND FIRST res-line WHERE res-line.resnr = bill-resnr                            
                            AND (res-line.resstatus = 1 OR res-line.resstatus = 2
                                 OR res-line.resstatus = 5 OR res-line.resstatus = 6
                                 OR res-line.resstatus = 8) USE-INDEX ankunf_ix NO-LOCK NO-ERROR.
                        IF AVAILABLE res-line THEN    
                            his-res.ci-date = res-line.ankunft.                              
                        
                        FIND LAST res-line WHERE res-line.resnr = bill-resnr                            
                            AND (res-line.resstatus = 1 OR res-line.resstatus = 2
                                 OR res-line.resstatus = 5 OR res-line.resstatus = 6
                                 OR res-line.resstatus = 8) USE-INDEX abr-resnam_ix NO-LOCK NO-ERROR.
                        IF AVAILABLE res-line THEN
                            his-res.co-date = res-line.abreise.
                                               
                        FIND FIRST reservation WHERE reservation.resnr = bill-resnr NO-LOCK NO-ERROR.
                        IF AVAILABLE reservation THEN
                        DO:
                            IF reservation.resdat NE ? THEN
                                his-res.bookdate    = reservation.resdat.
                            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                            IF AVAILABLE segment THEN
                                his-res.segmentcode = segment.bezeich.
                        END.
                    END.
                     
                    IF revCode = "ATS" THEN
                        his-res.rm-rev = his-res.rm-rev + netto.
                    ELSE IF revCode = "ATM" THEN
                        his-res.fb-rev = his-res.fb-rev + netto.
                    ELSE IF revCode = "ATZ" THEN
                        his-res.other-rev = his-res.other-rev + netto.
                END.
                ELSE IF (bill-reslinnr NE 0 AND bill-resnr GT 0) 
                    OR (bill-reslinnr = 0 AND bill-resnr GT 0 AND billjournal.zinr NE "") THEN /* PERSONAL BILL */
                DO:
                    IF bill-reslinnr NE 0 THEN
                    DO:                    
                        FIND FIRST his-res WHERE his-res.staydate = billjournal.bill-datum
                        AND bill-resnr = his-res.resnr
                        AND bill-reslinnr = his-res.reslinnr NO-LOCK NO-ERROR.
                        t-reslinnr = bill-reslinnr.
                    END.
                    ELSE
                    DO:                    
                        FIND FIRST his-res WHERE his-res.staydate = billjournal.bill-datum
                        AND bill-resnr = his-res.resnr
                        AND INT(ENTRY(2,billjournal.comment,";")) = his-res.reslinnr NO-LOCK NO-ERROR.
                        t-reslinnr = INT(ENTRY(2,billjournal.comment,";")).
                    END.

                    IF NOT AVAILABLE his-res THEN
                    DO:
                        CREATE his-res.
                        ASSIGN
                            his-res.zinr = billjournal.zinr 
                            his-res.resnr = bill-resnr
                            his-res.reslinnr = t-reslinnr.
                            

                        FIND FIRST res-line WHERE res-line.resnr = bill-resnr
                            AND res-line.reslinnr = t-reslinnr NO-LOCK NO-ERROR.                        
                        
                        IF AVAILABLE res-line THEN
                        DO:  
                            his-res.reserveID = res-line.gastnr.

                            FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                            IF AVAILABLE guest THEN
                            DO:
                                IF guest.vorname1 NE "" THEN
                                    his-res.reservename = guest.NAME + " " + guest.vorname1.
                                ELSE
                                    his-res.reservename = guest.NAME.
                            END.  
                            ASSIGN
                                his-res.ci-date   = res-line.ankunft
                                his-res.co-date   = res-line.abreise                                
                                his-res.staydate  = billjournal.bill-datum.
                            
                            IF billjournal.bill-datum LT bill-date AND billjournal.sysdate GT bill-date THEN
                                his-res.nbrofroom = 0. /*BACK DATED ROOM QTY MUST BE 0*/
                            ELSE
                                his-res.nbrofroom = res-line.zimmeranz.

                            IF his-res.staydate = his-res.co-date
                                AND his-res.ci-date NE his-res.co-date THEN
                                    his-res.nbrofroom = 0. /*TRANSACTION ON GUEST'S CHECK OUT DAY, ROOM QTY MUST BE 0*/

                            IF res-line.resstatus EQ 12 THEN /*IF ADD BILL*/
                            DO:                                    
                                FIND FIRST bufres-line WHERE bufres-line.resnr = bill-resnr
                                    AND bufres-line.reslinnr = bill-parentnr NO-LOCK NO-ERROR.
                                IF AVAILABLE bufres-line THEN     
                                DO:    
                                    his-res.nbrofroom = 0.
                                    FIND FIRST genstat WHERE genstat.resnr = bufres-line.resnr AND genstat.res-int[1] = bufres-line.reslinnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE genstat THEN
                                    DO:                                        
                                        IF bufres-line.resstatus = 6 THEN
                                            his-res.resstatus = "INHOUSE".
                                        ELSE IF bufres-line.resstatus = 13 THEN
                                            ASSIGN
                                                his-res.resstatus = "INHOUSE(ROOM SHARER)".
                                                
                                        ELSE IF bufres-line.resstatus = 8 THEN
                                        DO:
                                            IF genstat.resstatus = 13 THEN
                                                ASSIGN
                                                    his-res.resstatus = "CHECKEDOUT(ROOM SHARER)".
                                            ELSE IF genstat.resstatus = 6 THEN
                                                his-res.resstatus = "CHECKEDOUT".
                                            ELSE IF genstat.resstatus = 8 THEN
                                                his-res.resstatus = "CHECKEDOUT". /*DAY-USE*/
                                        END.
                                    END.    
                                END.
                            END.
                            ELSE
                            DO:                            
                                FIND FIRST genstat WHERE genstat.resnr = res-line.resnr AND genstat.res-int[1] = res-line.reslinnr NO-LOCK NO-ERROR.
                                IF AVAILABLE genstat THEN
                                DO:
                                    IF res-line.resstatus = 6 THEN
                                        his-res.resstatus = "INHOUSE".
                                    ELSE IF res-line.resstatus = 13 THEN
                                        ASSIGN
                                            his-res.resstatus = "INHOUSE(ROOM SHARER)"
                                            his-res.nbrofroom = 0.
                                    ELSE IF res-line.resstatus = 8 THEN
                                    DO:
                                        IF genstat.resstatus = 13 THEN
                                            ASSIGN
                                                his-res.resstatus = "CHECKEDOUT(ROOM SHARER)"
                                                his-res.nbrofroom = 0.
                                        ELSE IF genstat.resstatus = 6 THEN
                                            his-res.resstatus = "CHECKEDOUT".
                                        ELSE IF genstat.resstatus = 8 THEN
                                            his-res.resstatus = "CHECKEDOUT". /*DAY-USE*/
                                    END. 
                                END.
                            END.

                            
                            FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                            IF AVAILABLE zimkateg THEN his-res.room-type = zimkateg.kurzbez.

                            IF res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") THEN
                            DO:
                                DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                                    iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
                                    IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
                                        his-res.rate-code  = SUBSTR(iftask,11).
                                END.
                            END.

                            FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.  
                            IF AVAILABLE gbuff THEN
                                his-res.nationality = gbuff.nation1.
                        END.

                        FIND FIRST reservation WHERE reservation.resnr = bill-resnr NO-LOCK NO-ERROR.
                        IF AVAILABLE reservation THEN
                        DO:
                            IF reservation.resdat NE ? THEN
                                his-res.bookdate    = reservation.resdat.
                            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                            IF AVAILABLE segment THEN
                                his-res.segmentcode = segment.bezeich.
                        END.
                    END.
                    
                    IF revCode = "ATS" THEN
                        his-res.rm-rev = his-res.rm-rev + netto.
                    ELSE IF revCode = "ATM" THEN
                        his-res.fb-rev = his-res.fb-rev + netto.
                    ELSE IF revCode = "ATZ" THEN
                        his-res.other-rev = his-res.other-rev + netto.                   
                END.                 

                ELSE IF bill-resnr = 0 THEN /* NON-STAY BILL */ 
                DO: /* 5. yesterday's non-stay revenue data */
                    FIND FIRST non-room WHERE non-room.departmentID = billjournal.departement 
                        AND non-room.postingdate = billjournal.bill-datum NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE non-room THEN
                    DO:                        
                        CREATE non-room.
                        ASSIGN
                            non-room.departmentID = billjournal.departement
                            non-room.postingdate = billjournal.bill-datum.

                        FIND FIRST hoteldpt WHERE hoteldpt.num = billjournal.departement NO-LOCK NO-ERROR.
                        IF AVAILABLE hoteldpt THEN
                            non-room.departmentName = hoteldpt.depart.
                    END.
                    IF revCode = "ATM" THEN
                        non-room.fb-rev = non-room.fb-rev + netto.
                    ELSE IF revCode = "ATZ" THEN
                        non-room.other-rev = non-room.other-rev + netto.
                    ELSE IF revCode = "ATS" THEN
                        non-room.rm-rev = non-room.rm-rev + netto.
                END.                
            END.
        END.
    END.
END.

DEF BUFFER hbill-buff FOR h-bill-line.

DEF TEMP-TABLE hbill-list
    FIELD dept      AS INTEGER
    FIELD rechnr    AS INTEGER
    FIELD i-fact    AS INTEGER INIT 0
    FIELD do-it     AS LOGICAL INIT YES
    FIELD tot-sales AS DECIMAL INIT 0
.

FOR EACH h-bill-line NO-LOCK WHERE h-bill-line.rechnr GT 0 
    AND h-bill-line.bill-datum GE (ci-date - storage-dur)
    AND h-bill-line.bill-datum LE bill-date
    AND h-bill-line.zeit GE 0
    AND h-bill-line.artnr GT 0 
    AND h-bill-line.betrag NE 0 USE-INDEX bildat_index
    BY h-bill-line.departement BY h-bill-line.rechnr
    BY h-bill-line.sysdate DESCENDING
    BY h-bill-line.zeit DESCENDING:
    FIND FIRST hbill-list WHERE hbill-list.dept = h-bill-line.departement
        AND hbill-list.rechnr = h-bill-line.rechnr NO-ERROR.      
        IF NOT AVAILABLE hbill-list THEN
    DO:          
        CREATE hbill-list.
        ASSIGN
            hbill-list.dept   = h-bill-line.departement
            hbill-list.rechnr = h-bill-line.rechnr
            .
        FIND FIRST hbill-buff WHERE hbill-buff.departement = h-bill-line.departement
            AND hbill-buff.rechnr = h-bill-line.rechnr
            AND hbill-buff.bill-datum GT h-bill-line.bill-datum
            NO-LOCK NO-ERROR.
        hbill-list.do-it = NOT AVAILABLE hbill-buff.
    END.
END.

FOR EACH hbill-list WHERE hbill-list.do-it = YES:                                        
    FOR EACH h-bill-line WHERE h-bill-line.departement = hbill-list.dept
        AND h-bill-line.rechnr = hbill-list.rechnr 
        AND h-bill-line.artnr GT 0 NO-LOCK,
        FIRST h-artikel WHERE h-artikel.departement = h-bill-line.departement
            AND h-artikel.artnr = h-bill-line.artnr AND h-artikel.artart = 0  NO-LOCK:
            hbill-list.tot-sales = hbill-list.tot-sales + h-bill-line.betrag.                
    END.
END.

FOR EACH hbill-list WHERE hbill-list.do-it = YES:                                        
    FOR EACH h-bill-line WHERE h-bill-line.departement = hbill-list.dept
        AND h-bill-line.rechnr = hbill-list.rechnr 
        AND h-bill-line.artnr GT 0 NO-LOCK,
        FIRST h-artikel WHERE h-artikel.departement = h-bill-line.departement
            AND h-artikel.artnr = h-bill-line.artnr
            AND (h-artikel.artart = 11 OR h-artikel.artart = 12)  NO-LOCK:
            hbill-list.do-it = NO.
            
    END.
END.

FOR EACH hbill-list WHERE hbill-list.do-it:
    FOR EACH h-bill-line WHERE h-bill-line.departement = hbill-list.dept
        AND h-bill-line.rechnr = hbill-list.rechnr 
        AND h-bill-line.artnr GT 0 NO-LOCK,
        FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr
        AND h-artikel.departement = h-bill-line.departement 
        AND h-artikel.artart = 0 NO-LOCK:
        FIND FIRST t-list WHERE t-list.rechnr = h-bill-line.rechnr
            AND t-list.departement = h-bill-line.departement
            AND t-list.bill-datum = h-bill-line.bill-datum NO-ERROR.
        IF NOT AVAILABLE t-list THEN
        DO:
            CREATE t-list.
            ASSIGN
                t-list.rechnr      = h-bill-line.rechnr
                t-list.departement = h-bill-line.departement
                t-list.bill-datum  = h-bill-line.bill-datum
                t-list.sysdate     = h-bill-line.sysdate
                t-list.zeit        = h-bill-line.zeit
            .
        END.
     
        FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
            AND artikel.departement = h-artikel.departement NO-LOCK.
        IF artikel.artart = 9 THEN .
        ELSE
        DO:
            ASSIGN
                netto       = 0
                serv-betrag = 0
            .
            RUN calc-servvat.p (artikel.departement, artikel.artnr, h-bill-line.bill-datum,
              artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
            IF vat = 1 THEN
            ASSIGN 
                netto       = h-bill-line.betrag * 100 / vat-proz
                serv-betrag = 0
            .
            ELSE 
            DO:
              IF serv = 1 THEN
              ASSIGN
                  serv-betrag = netto
                  netto       = 0
              .
              ELSE IF vat GT 0 THEN
              ASSIGN
                netto       = h-bill-line.betrag / (1 + serv + vat)
                serv-betrag = netto * serv
              .
            END.
    
            IF artikel.umsatzart = 3 OR artikel.umsatzart GE 5 THEN 
            ASSIGN
                t-list.fb         = t-list.fb + netto 
                t-list.fb-service = t-list.fb-service + serv-betrag 
            .
            ELSE 
            ASSIGN
                t-list.other         = t-list.other + netto
                t-list.other-service = t-list.other-service + serv-betrag
            .
        END.
    END.          
END.

FOR EACH t-list NO-LOCK:
    FIND FIRST non-room WHERE non-room.departmentID = t-list.departement 
        AND non-room.postingdate = t-list.bill-datum NO-LOCK NO-ERROR.
    IF NOT AVAILABLE non-room THEN
    DO:
        CREATE non-room.
        ASSIGN
            non-room.departmentID = t-list.departement
            non-room.postingdate = t-list.bill-datum.

        FIND FIRST hoteldpt WHERE hoteldpt.num = t-list.departement NO-LOCK NO-ERROR.
        IF AVAILABLE hoteldpt THEN
            non-room.departmentName = hoteldpt.depart.            
    END.
    non-room.fb-rev = non-room.fb-rev + t-list.fb.
    non-room.other-rev = non-room.other-rev + t-list.other.

    /*DISP non-room.other-rev FORMAT ">>>,>>>,>>>,>>>" non-room.fb-rev FORMAT ">>>,>>>,>>>,>>>" t-list.rechnr t-list.departement.*/
END.
/*MESSAGE non-room.other-rev " | " non-room.fb-rev 
    VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
    
/*generating history cancelled and no-show reservations*/
FIND FIRST res-line WHERE (res-line.resstatus EQ 9 OR res-line.resstatus EQ 10)
    AND res-line.active-flag EQ 2
    AND res-line.l-zuordnung[3] = 0
    AND res-line.ankunft GE (ci-date - storage-dur)
    AND res-line.ankunft LE bill-date NO-LOCK NO-ERROR.

DO WHILE AVAILABLE res-line:
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
    FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.

    CREATE temp-res.
    ASSIGN
        temp-res.resnr       = res-line.resnr
        temp-res.reslinnr    = res-line.reslinnr
        temp-res.ci-date     = res-line.ankunft
        temp-res.co-date     = res-line.abreise.

    IF res-line.betrieb-gastpay = 11 THEN
    DO:
        IF res-line.resstatus = 9 THEN
            temp-res.resstatus = "CANCELLED(ROOM SHARER)".
        ELSE IF res-line.resstatus = 10 THEN
            temp-res.resstatus = "NO-SHOW(ROOM SHARER)".

        temp-res.nbrofroom   = 0.
    END.
    ELSE
    DO:
        IF res-line.resstatus = 9 THEN
            temp-res.resstatus = "CANCELLED".
        ELSE IF res-line.resstatus = 10 THEN
            temp-res.resstatus = "NO-SHOW".

        temp-res.nbrofroom   = res-line.zimmeranz.
    END.

    IF res-line.CANCELLED NE ? THEN
        temp-res.cancel-date = STRING(MONTH(res-line.CANCELLED),"99") + "-" + 
                               STRING(DAY(res-line.CANCELLED),"99") + "-" +
                               STRING(YEAR(res-line.CANCELLED),"9999").

    IF AVAILABLE zimkateg THEN
        temp-res.room-type   = zimkateg.kurzbez.
    IF AVAILABLE guest THEN
    DO:    
        temp-res.reserveID   = guest.gastnr.
        IF guest.vorname1 NE "" THEN
            temp-res.reservename = guest.NAME + " " + guest.vorname1.
        ELSE
            temp-res.reservename = guest.NAME.
    END.
    IF AVAILABLE gbuff THEN
        temp-res.nationality = gbuff.nation1.
    IF AVAILABLE reservation THEN
    DO:   
        IF reservation.resdat NE ? THEN
            temp-res.bookdate    = reservation.resdat.
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN
            temp-res.segmentcode = segment.bezeich.
    END.      

    IF res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") THEN
    DO:
        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
                temp-res.rate-code  = SUBSTR(iftask,11).
        END.
    END.

    IF res-line.ankunft NE res-line.abreise THEN
        datum2 = res-line.abreise - 1.
    ELSE
        datum2 = res-line.abreise.

    DO datum = res-line.ankunft TO datum2: 
        IF datum GE (ci-date - storage-dur) AND datum LE bill-date THEN
        DO:               
            RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, curr-date,
                                     OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                     OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                     OUTPUT tot-dinner, OUTPUT tot-other,
                                     OUTPUT tot-rmrev, OUTPUT tot-vat,
                                     OUTPUT tot-service).
    
            tot-fb = tot-breakfast + tot-lunch + tot-dinner.
    
            CREATE his-res.
            BUFFER-COPY temp-res TO his-res.
            ASSIGN
                his-res.staydate = datum
                his-res.rm-rev = net-lodg
                his-res.fb-rev = tot-fb
                his-res.other-rev = tot-other.
        END.
    END.   

    DELETE temp-res.
    RELEASE temp-res.
    FIND NEXT res-line WHERE (res-line.resstatus EQ 9 OR res-line.resstatus EQ 10)
        AND res-line.active-flag EQ 2
        AND res-line.l-zuordnung[3] = 0
        AND res-line.ankunft GE (ci-date - storage-dur)
        AND res-line.ankunft LE bill-date NO-LOCK NO-ERROR.
END.
/**/
/*FILE 2*/
/*generating history inventory data for Compliment & Occupied status*/
FIND FIRST genstat WHERE genstat.datum GE (ci-date - storage-dur)
    AND genstat.datum LE bill-date   
    AND genstat.resstatus NE 0
    AND genstat.res-logi[2] = YES
    AND genstat.zikatnr NE 0 NO-LOCK NO-ERROR.

DO WHILE AVAILABLE genstat:
    IF genstat.resstatus NE 13 AND genstat.zinr NE "" THEN
    DO:    
        IF genstat.gratis NE 0 OR (genstat.zipreis = 0 AND genstat.erwachs GT 0) THEN
        DO:    
            FIND FIRST his-inv WHERE his-inv.datum = genstat.datum
                AND his-inv.zikatnr = genstat.zikatnr AND his-inv.room-status = "COMPLIMENT" NO-LOCK NO-ERROR.
            IF NOT AVAILABLE his-inv THEN
            DO:
                CREATE his-inv.
                ASSIGN
                    his-inv.datum = genstat.datum
                    his-inv.zikatnr = genstat.zikatnr
                    his-inv.qty = 1
                    his-inv.room-status = "COMPLIMENT".
            END.
            ELSE
            DO:
                his-inv.qty = his-inv.qty + 1.
            END.
        END.
        ELSE IF genstat.gratis = 0 AND genstat.zipreis NE 0 AND genstat.erwachs GT 0 THEN
        DO:
            FIND FIRST his-inv WHERE his-inv.datum = genstat.datum
                AND his-inv.zikatnr = genstat.zikatnr AND his-inv.room-status = "OCCUPIED" NO-LOCK NO-ERROR.
            IF NOT AVAILABLE his-inv THEN
            DO:
                CREATE his-inv.
                ASSIGN
                    his-inv.datum = genstat.datum
                    his-inv.zikatnr = genstat.zikatnr
                    his-inv.qty = 1
                    his-inv.room-status = "OCCUPIED".
            END.
            ELSE
            DO:
                his-inv.qty = his-inv.qty + 1.
            END.
        END.
    END.   

    /* GENERATE RECORDS WITH NO BILLJOURNAL -> if res-line be delete by storage duration
    FIND FIRST his-res WHERE his-res.zinr = genstat.zinr
                        AND his-res.staydate = genstat.datum
                        AND his-res.resnr = genstat.resnr
                        AND his-res.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
    IF NOT AVAILABLE his-res THEN
    DO:
        CREATE his-res.
        ASSIGN
            his-res.zinr = genstat.zinr 
            his-res.resnr = genstat.resnr
            his-res.reslinnr  = genstat.res-int[1]
            his-res.ci-date   = genstat.res-date[1]
            his-res.co-date   = genstat.res-date[2] 
            his-res.staydate  = genstat.datum
            his-res.nbrofroom = 1 /*default room number in case res-line table is
                                     already outside of storage duration*/   
            his-res.segmentcode = STRING(genstat.segmentcode)
            his-res.reserveID = genstat.gastnr
            his-res.rm-rev = genstat.logis 
            his-res.fb-rev = genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]
            /*his-res.beverage-rev = genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4].*/
            his-res.other-rev = genstat.res-deci[5] + genstat.res-deci[6] + genstat.res-deci[1]. /*termasuk additional F/O items*/
        
        FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN
        DO:
            IF guest.vorname1 NE "" THEN
                his-res.reservename = guest.NAME + " " + guest.vorname1.
            ELSE
                his-res.reservename = guest.NAME.
        END.

        FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK NO-ERROR.
            IF AVAILABLE zimkateg THEN his-res.room-type = zimkateg.kurzbez.                         
        
       FIND FIRST nation WHERE nation.natcode EQ 0 AND nation.nationnr = genstat.nation NO-LOCK NO-ERROR.  
       IF AVAILABLE nation THEN
           ASSIGN
               his-res.nationality = nation.kurzbez.

        FIND FIRST res-line WHERE res-line.resnr = genstat.resnr
            AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.                                        
        IF AVAILABLE res-line THEN
        DO:   
            IF res-line.resstatus = 6 THEN
                his-res.resstatus = "INHOUSE".
            ELSE IF res-line.resstatus = 13 THEN
                ASSIGN
                    his-res.resstatus = "INHOUSE(ROOM SHARER)"
                    his-res.nbrofroom = 0.
            ELSE IF res-line.resstatus = 8 THEN
            DO:
                IF genstat.resstatus = 13 THEN
                    ASSIGN
                        his-res.resstatus = "CHECKEDOUT(ROOM SHARER)"
                        his-res.nbrofroom = 0.
                ELSE IF genstat.resstatus = 6 THEN
                    his-res.resstatus = "CHECKEDOUT".
                ELSE IF genstat.resstatus = 8 THEN
                    his-res.resstatus = "CHECKEDOUT". /*DAY-USE*/
            END.

            IF res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") THEN
            DO:
                DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
                        his-res.rate-code  = SUBSTR(iftask,11).
                END.
            END.            
        END.
        ELSE
        DO:
             IF genstat.resstatus = 6 THEN
                his-res.resstatus = "CHECKEDOUT".
             ELSE IF genstat.resstatus = 13 THEN
                ASSIGN
                    his-res.resstatus = "CHECKEDOUT(ROOM SHARER)"
                    his-res.nbrofroom = 0.
             ELSE IF genstat.resstatus = 8 THEN
                    his-res.resstatus = "CHECKEDOUT".
        END.

        FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN
        DO:
            IF reservation.resdat NE ? THEN
                his-res.bookdate    = reservation.resdat.            
        END.            
    END.*/    

    /* GENERATE RECORDS WITH NO BILLJOURNAL */
    FIND FIRST his-res WHERE his-res.zinr = genstat.zinr
                        AND his-res.staydate = genstat.datum
                        AND his-res.resnr = genstat.resnr
                        AND his-res.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
    IF NOT AVAILABLE his-res THEN
    DO:
        CREATE his-res.
        ASSIGN
            his-res.zinr = genstat.zinr 
            his-res.resnr = genstat.resnr
            his-res.reslinnr = genstat.res-int[1].
            
        FIND FIRST res-line WHERE res-line.resnr = genstat.resnr
            AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.                        
        
        IF AVAILABLE res-line THEN
        DO:  
            his-res.reserveID = res-line.gastnr.

            FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN
            DO:
                IF guest.vorname1 NE "" THEN
                    his-res.reservename = guest.NAME + " " + guest.vorname1.
                ELSE
                    his-res.reservename = guest.NAME.
            END.  

            ASSIGN
                his-res.ci-date   = res-line.ankunft
                his-res.co-date   = res-line.abreise                                
                his-res.staydate  = genstat.datum
                his-res.nbrofroom = res-line.zimmeranz.

            
            IF res-line.resstatus = 6 THEN
                his-res.resstatus = "INHOUSE".
            ELSE IF res-line.resstatus = 13 THEN
                ASSIGN
                    his-res.resstatus = "INHOUSE(ROOM SHARER)"
                    his-res.nbrofroom = 0.
            ELSE IF res-line.resstatus = 8 THEN
            DO:
                IF genstat.resstatus = 13 THEN
                    ASSIGN
                        his-res.resstatus = "CHECKEDOUT(ROOM SHARER)"
                        his-res.nbrofroom = 0.
                ELSE IF genstat.resstatus = 6 THEN
                    his-res.resstatus = "CHECKEDOUT".
                ELSE IF genstat.resstatus = 8 THEN
                    his-res.resstatus = "CHECKEDOUT". /*DAY-USE*/
            END.            

            
            FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
            IF AVAILABLE zimkateg THEN his-res.room-type = zimkateg.kurzbez.

            IF res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") THEN
            DO:
                DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
                        his-res.rate-code  = SUBSTR(iftask,11).
                END.
            END.

            FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.  
            IF AVAILABLE gbuff THEN
                his-res.nationality = gbuff.nation1.
        END.

        FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN
        DO:
            IF reservation.resdat NE ? THEN
                his-res.bookdate    = reservation.resdat.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
            IF AVAILABLE segment THEN
                his-res.segmentcode = segment.bezeich.
        END.
    END.
    
    FIND NEXT genstat WHERE genstat.datum GE (ci-date - storage-dur)
       AND genstat.datum LE bill-date
       AND genstat.resstatus NE 0        
       AND genstat.res-logi[2] = YES
       AND genstat.zikatnr NE 0 NO-LOCK NO-ERROR.
END.
/**/
/*generating history inventory data for Available status*/
FIND FIRST zkstat WHERE zkstat.datum GE (ci-date - storage-dur)
    AND zkstat.datum LE bill-date
    AND zkstat.zikatnr NE 0 NO-LOCK NO-ERROR.
 
DO WHILE AVAILABLE zkstat:
    FIND FIRST his-inv WHERE his-inv.datum = zkstat.datum
            AND his-inv.zikatnr = zkstat.zikatnr AND his-inv.room-status = "AVAILABLE" NO-LOCK NO-ERROR.
    IF NOT AVAILABLE his-inv THEN
    DO:
        CREATE his-inv.
        ASSIGN
            his-inv.datum = zkstat.datum
            his-inv.zikatnr = zkstat.zikatnr
            his-inv.qty = zkstat.anz100
            his-inv.room-status = "AVAILABLE".
    END.

    FIND NEXT zkstat WHERE zkstat.datum GE (ci-date - storage-dur)
        AND zkstat.datum LE bill-date
        AND zkstat.zikatnr NE 0 NO-LOCK NO-ERROR.
END.

/*generating history inventory data for Out of Order status*/
FIND FIRST outorder WHERE outorder.gespende GE (ci-date - storage-dur)
    AND outorder.gespstart LE bill-date
    AND outorder.zinr NE ""
    AND outorder.betriebsnr LE 1 NO-LOCK NO-ERROR.

DO WHILE AVAILABLE outorder:
    FIND FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK NO-ERROR.
    IF AVAILABLE zimmer AND zimmer.sleeping = YES THEN
    DO datum2 = outorder.gespstart TO outorder.gespende:
        IF datum2 GE (ci-date - storage-dur) AND datum2 LE bill-date THEN
        DO:            
            FIND FIRST his-inv WHERE his-inv.datum = datum2
                 AND his-inv.room-type = zimmer.kbezeich
                 AND his-inv.room-status = "OUTOFORDER" NO-LOCK NO-ERROR.
            IF NOT AVAILABLE his-inv THEN
            DO:
                CREATE his-inv.
                ASSIGN
                    his-inv.datum = datum2
                    his-inv.qty = 1
                    his-inv.room-status = "OUTOFORDER"
                    his-inv.room-type = zimmer.kbezeich.
            END.
            ELSE
            DO:
                his-inv.qty = his-inv.qty + 1.
            END.
        END.
    END.
    
    FIND NEXT outorder WHERE outorder.gespende GE (ci-date - storage-dur)
        AND outorder.gespstart LE bill-date
        AND outorder.zinr NE ""
        AND outorder.betriebsnr LE 1 NO-LOCK NO-ERROR.
END.

FOR EACH his-inv:
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = his-inv.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE zimkateg AND his-inv.room-type EQ "" THEN
        his-inv.room-type = zimkateg.kurzbez.
END.

FOR EACH his-inv WHERE his-inv.room-status = "AVAILABLE":
    FIND FIRST bufhis-inv WHERE bufhis-inv.room-status = "OCCUPIED"       
        AND bufhis-inv.datum = his-inv.datum
        AND bufhis-inv.room-type = his-inv.room-type NO-LOCK NO-ERROR.
    IF AVAILABLE bufhis-inv THEN
        his-inv.qty = his-inv.qty - bufhis-inv.qty.

    FIND FIRST bufhis-inv WHERE bufhis-inv.room-status = "OUTOFORDER"       
        AND bufhis-inv.datum = his-inv.datum
        AND bufhis-inv.room-type = his-inv.room-type NO-LOCK NO-ERROR.
    IF AVAILABLE bufhis-inv THEN
        his-inv.qty = his-inv.qty - bufhis-inv.qty.

    FIND FIRST bufhis-inv WHERE bufhis-inv.room-status = "COMPLIMENT"       
        AND bufhis-inv.datum = his-inv.datum
        AND bufhis-inv.room-type = his-inv.room-type NO-LOCK NO-ERROR.
    IF AVAILABLE bufhis-inv THEN
        his-inv.qty = his-inv.qty - bufhis-inv.qty.
END.

/*FILE 3*/
/*generating future inventory data for Compliment status*/
FOR EACH res-line WHERE res-line.active-flag LE 1 
    AND res-line.resstatus LE 6 AND res-line.resstatus NE 3
    AND res-line.resstatus NE 4
    AND res-line.kontignr GE 0 AND res-line.l-zuordnung[3] = 0
    AND res-line.ankunft LE ci-date + 90
    AND res-line.abreise GE ci-date NO-LOCK:
    do-it1 = YES. 
    IF res-line.zinr NE "" THEN 
    DO: 
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
        do-it1 = zimmer.sleeping. 
    END. 

    IF do-it1 THEN
    DO:
        IF res-line.ankunft = res-line.abreise THEN 
            end-date = res-line.abreise.
        ELSE 
            end-date = res-line.abreise - 1.

        DO datum2 = res-line.ankunft TO end-date:
            IF datum2 GE ci-date AND datum2 LE ci-date + 90 THEN
            DO:                
                IF res-line.gratis NE 0 OR (res-line.zipreis = 0 AND res-line.erwachs GT 0) THEN
                DO:    
                    FIND FIRST future-inv WHERE future-inv.datum = datum2
                        AND future-inv.zikatnr = res-line.zikatnr 
                        AND future-inv.room-status = "COMPLIMENT" NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE future-inv THEN
                    DO:
                        CREATE future-inv.
                        ASSIGN
                            future-inv.datum = datum2
                            future-inv.zikatnr = res-line.zikatnr
                            future-inv.qty = res-line.zimmeranz
                            future-inv.room-status = "COMPLIMENT".
                    END.
                    ELSE
                    DO:
                        future-inv.qty = future-inv.qty + res-line.zimmeranz.
                    END.
                END.
                ELSE
                DO:
                     FIND FIRST future-inv WHERE future-inv.datum = datum2
                        AND future-inv.zikatnr = res-line.zikatnr 
                        AND future-inv.room-status = "OCCUPIED" NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE future-inv THEN
                    DO:
                        CREATE future-inv.
                        ASSIGN
                            future-inv.datum = datum2
                            future-inv.zikatnr = res-line.zikatnr
                            future-inv.qty = res-line.zimmeranz
                            future-inv.room-status = "OCCUPIED".
                    END.
                    ELSE
                    DO:
                        future-inv.qty = future-inv.qty + res-line.zimmeranz.
                    END.
                END.
            END.
        END.
    END.
END.
/*generating future inventory data for Available status*/
/******************************************************************************************************/
FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK BY zimmer.zikatnr: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
    IF zimkateg.verfuegbarkeit THEN 
    DO: 
        DO datum = ci-date TO ci-date + 90:
            FIND FIRST future-inv WHERE future-inv.zikatnr = zimkateg.zikatnr
                AND future-inv.room-status = "AVAILABLE"
                AND future-inv.datum = datum NO-LOCK NO-ERROR.
            IF NOT AVAILABLE future-inv THEN
            DO:            
                CREATE future-inv.
                ASSIGN
                    future-inv.zikatnr = zimkateg.zikatnr
                    future-inv.qty = 1
                    future-inv.datum = datum
                    future-inv.room-status = "AVAILABLE". 
            END. 
            ELSE future-inv.qty = future-inv.qty + 1. 
        END.
    END. 
END.

/*generating future inventory data for Out of Order status*/
FIND FIRST outorder WHERE outorder.gespende GE ci-date
    AND outorder.gespstart LE ci-date + 90
    AND outorder.zinr NE ""
    AND outorder.betriebsnr LE 1 NO-LOCK NO-ERROR.

DO WHILE AVAILABLE outorder:
    FIND FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK NO-ERROR.
    IF AVAILABLE zimmer AND zimmer.sleeping = YES THEN
    DO datum2 = outorder.gespstart TO outorder.gespende:
        IF datum2 GE ci-date AND datum2 LE ci-date + 90 THEN
        DO:        
            FIND FIRST future-inv WHERE future-inv.datum = datum2
                 AND future-inv.room-type = zimmer.kbezeich
                 AND future-inv.room-status = "OUTOFORDER" NO-LOCK NO-ERROR.
            IF NOT AVAILABLE future-inv THEN
            DO:
                CREATE future-inv.
                ASSIGN
                    future-inv.datum = datum2
                    future-inv.qty = 1
                    future-inv.room-status = "OUTOFORDER"
                    future-inv.room-type = zimmer.kbezeich.
            END.
            ELSE
            DO:
                future-inv.qty = future-inv.qty + 1.
            END.
        END.
    END.
    
    FIND NEXT outorder WHERE outorder.gespende GE ci-date
        AND outorder.gespstart LE ci-date + 90
        AND outorder.zinr NE ""
        AND outorder.betriebsnr LE 1 NO-LOCK NO-ERROR.
END.

FOR EACH future-inv:
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = future-inv.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE zimkateg AND future-inv.room-type EQ "" THEN
        future-inv.room-type = zimkateg.kurzbez.
END.

FOR EACH future-inv WHERE future-inv.room-status = "AVAILABLE":
    FIND FIRST buffuture-inv WHERE buffuture-inv.room-status = "OCCUPIED"       
        AND buffuture-inv.datum = future-inv.datum
        AND buffuture-inv.room-type = future-inv.room-type NO-LOCK NO-ERROR.
    IF AVAILABLE buffuture-inv THEN
        future-inv.qty = future-inv.qty - buffuture-inv.qty.

    FIND FIRST buffuture-inv WHERE buffuture-inv.room-status = "OUTOFORDER"       
        AND buffuture-inv.datum = future-inv.datum
        AND buffuture-inv.room-type = future-inv.room-type NO-LOCK NO-ERROR.
    IF AVAILABLE buffuture-inv THEN
        future-inv.qty = future-inv.qty - buffuture-inv.qty.

    FIND FIRST buffuture-inv WHERE buffuture-inv.room-status = "COMPLIMENT"       
        AND buffuture-inv.datum = future-inv.datum
        AND buffuture-inv.room-type = future-inv.room-type NO-LOCK NO-ERROR.
    IF AVAILABLE buffuture-inv THEN
        future-inv.qty = future-inv.qty - buffuture-inv.qty.
END.

/*FILE 4*/
/*generating future reservation data*/
EMPTY TEMP-TABLE temp-res.
FIND FIRST res-line WHERE res-line.abreise GE ci-date 
    AND res-line.ankunft LE ci-date + 90
    AND res-line.resstatus NE 4
    AND res-line.resstatus NE 8
    AND res-line.resstatus NE 9
    AND res-line.resstatus NE 10
    AND res-line.resstatus NE 12
    AND res-line.resstatus NE 99
    AND res-line.active-flag LE 1
    AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.

DO WHILE AVAILABLE res-line:
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
    FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.

    CREATE temp-res.
    ASSIGN
        temp-res.resnr       = res-line.resnr
        temp-res.reslinnr    = res-line.reslinnr
        temp-res.ci-date     = res-line.ankunft
        temp-res.co-date     = res-line.abreise.
    IF res-line.resstatus EQ 11 OR res-line.resstatus EQ 13 THEN
        temp-res.nbrofroom   = 0.
    ELSE
        temp-res.nbrofroom   = res-line.zimmeranz.

    IF AVAILABLE zimkateg THEN
        temp-res.room-type   = zimkateg.kurzbez.
    IF AVAILABLE guest THEN
    DO:    
        temp-res.reserveID   = guest.gastnr.
        IF guest.vorname1 NE "" THEN
            temp-res.reservename = guest.NAME + " " + guest.vorname1.
        ELSE
            temp-res.reservename = guest.NAME.
    END.
    IF AVAILABLE gbuff THEN
        temp-res.nationality = gbuff.nation1.
    IF AVAILABLE reservation THEN
    DO:    
        temp-res.bookdate    = reservation.resdat.
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN
            temp-res.segmentcode = segment.bezeich.
    END.
    IF res-line.resstatus = 1 THEN
        temp-res.resstatus = "GUARANTEED".
    ELSE IF res-line.resstatus = 2 THEN
        temp-res.resstatus = "6PM".
    ELSE IF res-line.resstatus = 3 THEN
        temp-res.resstatus = "TENTATIVE".
    ELSE IF res-line.resstatus = 5 THEN
        temp-res.resstatus = "VERBAL CONFIRM".
    ELSE IF res-line.resstatus = 6 THEN
        temp-res.resstatus = "INHOUSE".
    ELSE IF res-line.resstatus = 11 THEN
        temp-res.resstatus = "ROOM SHARER".
    ELSE IF res-line.resstatus = 13 THEN
        temp-res.resstatus = "INHOUSE(ROOM SHARER)".

    IF res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") THEN
    DO:
        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
                temp-res.rate-code  = SUBSTR(iftask,11).
        END.
    END.

    IF res-line.ankunft NE res-line.abreise THEN
        datum2 = res-line.abreise - 1.
    ELSE
        datum2 = res-line.abreise.

    DO datum = res-line.ankunft TO datum2:  
        IF datum GE ci-date AND datum LE ci-date + 90 THEN
        DO:                
            RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, curr-date,
                                     OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                     OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                     OUTPUT tot-dinner, OUTPUT tot-other,
                                     OUTPUT tot-rmrev, OUTPUT tot-vat,
                                     OUTPUT tot-service).
    
            tot-fb = tot-breakfast + tot-lunch + tot-dinner.
    
            CREATE future-res.
            BUFFER-COPY temp-res TO future-res.
            ASSIGN
                future-res.staydate = datum
                future-res.rm-rev = net-lodg
                future-res.fb-rev = tot-fb
                future-res.other-rev = tot-other.
        END.
    END.   

    DELETE temp-res.
    RELEASE temp-res.

    FIND NEXT res-line WHERE res-line.abreise GE ci-date 
    AND res-line.ankunft LE ci-date + 90
    AND res-line.resstatus NE 4
    AND res-line.resstatus NE 8
    AND res-line.resstatus NE 9
    AND res-line.resstatus NE 10
    AND res-line.resstatus NE 12
    AND res-line.resstatus NE 99
    AND res-line.active-flag LE 1
    AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
END.

