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
    FIELD nights        AS INTEGER
    FIELD adult         AS INTEGER
    FIELD child         AS INTEGER
    FIELD complimentary AS INTEGER
    FIELD arrangement   AS CHARACTER
    FIELD guest-name    AS CHARACTER
    FIELD banquet-rev   AS DECIMAL
    FIELD commision     AS DECIMAL
    FIELD payable       AS DECIMAL
    FIELD nation2       AS CHARACTER
    FIELD booktime      AS CHARACTER
    FIELD salesid       AS CHARACTER
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

DEFINE INPUT PARAMETER banquet-dept AS CHARACTER.
DEFINE INPUT PARAMETER commision    AS CHARACTER.
DEFINE INPUT PARAMETER payable      AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR his-res.

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
DEFINE VARIABLE tot-banquet     AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-commision   AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-payable     AS DECIMAL NO-UNDO.
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

DEFINE VARIABLE bill-resnr       AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-reslinnr    AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-parentnr    AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-gastnr      AS INTEGER NO-UNDO.
DEFINE VARIABLE ex-article       AS CHARACTER NO-UNDO.
DEFINE VARIABLE t-reslinnr       AS INTEGER NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
ci-date = htparam.fdate.

FOR EACH reservation WHERE reservation.resdat GE 01/01/16 AND
    reservation.resdat LT ci-date NO-LOCK BY reservation.resdat:

    FIND FIRST res-line WHERE res-line.resnr = reservation.resnr
        AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99
        AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.

    DO WHILE AVAILABLE res-line:
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
        FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
    
        CREATE his-res.
        ASSIGN
            his-res.resnr         = res-line.resnr
            his-res.reslinnr      = res-line.reslinnr
            his-res.ci-date       = res-line.ankunft
            his-res.co-date       = res-line.abreise
            his-res.adult         = res-line.erwachs
            his-res.child         = res-line.kind1
            his-res.complimentary = res-line.gratis
            his-res.arrangement   = res-line.arrangement
            his-res.booktime      = SUBSTR(res-line.reserve-char, 9, 5)
            his-res.guest-name    = res-line.NAME.
        IF res-line.resstatus EQ 11 OR res-line.resstatus EQ 13 THEN
            his-res.nbrofroom   = 0.
        ELSE
            his-res.nbrofroom   = res-line.zimmeranz.

        IF res-line.ankunft NE res-line.abreise THEN
            his-res.nights = res-line.abreise - res-line.ankunft.
        ELSE
            his-res.nights = 1.
    
        IF AVAILABLE zimkateg THEN
            his-res.room-type   = zimkateg.kurzbez.
        IF AVAILABLE guest THEN
        DO:    
            IF guest.phonetik3 NE "" THEN
            DO:
                FIND FIRST bediener WHERE bediener.nr = INT(guest.phonetik3) NO-LOCK NO-ERROR.
                IF AVAILABLE bediener THEN
                    his-res.salesid = bediener.username.
            END.
            his-res.reserveID   = guest.gastnr.
            IF guest.vorname1 NE "" THEN
                his-res.reservename = guest.NAME + " " + guest.vorname1.
            ELSE
                his-res.reservename = guest.NAME.
        END.
        IF AVAILABLE gbuff THEN
            ASSIGN
                his-res.nationality = gbuff.nation1
                his-res.nation2 = gbuff.nation2.
        IF AVAILABLE reservation THEN
        DO:                
            his-res.bookdate    = reservation.resdat.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
            IF AVAILABLE segment THEN
                his-res.segmentcode = segment.bezeich.
        END.
        IF res-line.resstatus = 1 THEN
            his-res.resstatus = "Guaranteed".
        ELSE IF res-line.resstatus = 2 THEN
            his-res.resstatus = "6PM".
        ELSE IF res-line.resstatus = 3 THEN
            his-res.resstatus = "Tentative".
        ELSE IF res-line.resstatus = 4 THEN
            his-res.resstatus = "WaitList".
        ELSE IF res-line.resstatus = 5 THEN
            his-res.resstatus = "VerbalConfirm".
        ELSE IF res-line.resstatus = 6 THEN
            his-res.resstatus = "Inhouse".
        ELSE IF res-line.resstatus = 8 THEN
            his-res.resstatus = "Departed".
        ELSE IF res-line.resstatus = 9 THEN
            his-res.resstatus = "Cancelled".
        ELSE IF res-line.resstatus = 10 THEN
            his-res.resstatus = "NoShow".
        ELSE IF res-line.resstatus = 11 THEN
            his-res.resstatus = "ShareRes".
        ELSE IF res-line.resstatus = 13 THEN
            his-res.resstatus = "RmSharer".
    
        IF res-line.zimmer-wunsch MATCHES ("*$OrigCode$*") THEN
        DO:
            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
                IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
                    his-res.rate-code  = SUBSTR(iftask,11).
            END.
        END.
    
        IF res-line.ankunft NE res-line.abreise THEN
            datum2 = res-line.abreise - 1.
        ELSE
            datum2 = res-line.abreise.
    
        DO datum = res-line.ankunft TO datum2:        
            RUN get-room-breakdown-phm.p(RECID(res-line), datum, curr-i, curr-date,
                                         banquet-dept, commision, payable,
                                     OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                     OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                     OUTPUT tot-dinner, OUTPUT tot-other,
                                     OUTPUT tot-rmrev, OUTPUT tot-vat,
                                     OUTPUT tot-service, OUTPUT tot-banquet,
                                     OUTPUT tot-commision, OUTPUT tot-payable).
    
            his-res.fb-rev = his-res.fb-rev + tot-breakfast + tot-lunch + tot-dinner.
            his-res.rm-rev = his-res.rm-rev + net-lodg.
            his-res.other-rev = his-res.other-rev + tot-other.
            his-res.banquet-rev = his-res.banquet-rev + tot-banquet.
            his-res.commision = his-res.commision + tot-commision.
            his-res.payable = his-res.payable + tot-payable.
        END.           

        FIND NEXT res-line WHERE res-line.resnr = reservation.resnr
            AND res-line.resstatus NE 12
            AND res-line.resstatus NE 99
            AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
    END.
END.
   
/*
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
                future-res.rm-rev = tot-rmrev
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

*/
