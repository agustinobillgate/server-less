DEFINE TEMP-TABLE p-list
    FIELD confno        AS CHARACTER
    FIELD arrdate       AS CHARACTER
    FIELD depdate       AS CHARACTER
    FIELD roomtype      AS CHARACTER
    FIELD roomno        AS CHARACTER
    FIELD roomrate      AS DECIMAL
    FIELD gname         AS CHARACTER
    FIELD comp          AS CHARACTER
    FIELD sourcename    AS CHARACTER
    FIELD memberno      AS CHARACTER
    FIELD totrev        AS DECIMAL
    FIELD rmrev         AS DECIMAL
    FIELD fbrev         AS DECIMAL
    FIELD others        AS DECIMAL
    FIELD propID        AS CHARACTER
    FIELD reward        AS CHARACTER
    FIELD bookdate      AS CHARACTER
    FIELD market        AS CHARACTER
    FIELD note          AS CHARACTER
    FIELD profile       AS CHARACTER
    FIELD exportdate    AS CHARACTER
    FIELD ratecode      AS CHARACTER
.

DEFINE TEMP-TABLE x-list
    FIELD confno        AS CHARACTER
    FIELD arrdate       AS CHARACTER
    FIELD depdate       AS CHARACTER
    FIELD roomtype      AS CHARACTER
    FIELD roomrate      AS DECIMAL
    FIELD gname         AS CHARACTER
    FIELD comp          AS CHARACTER
    FIELD sourcename    AS CHARACTER
    FIELD memberno      AS CHARACTER
    FIELD profile       AS CHARACTER
    FIELD email         AS CHARACTER
    FIELD totrev        AS DECIMAL
    FIELD rmrev         AS DECIMAL
    FIELD fbrev         AS DECIMAL
    FIELD others        AS DECIMAL
    FIELD propID        AS CHARACTER
    FIELD bookdate      AS CHARACTER
    FIELD market        AS CHARACTER
    FIELD bookstatus    AS CHARACTER
    FIELD adult         AS INT
    FIELD child         AS INT
    FIELD note          AS CHARACTER
.

DEFINE TEMP-TABLE r-list
    FIELD email         AS CHARACTER
    FIELD g-title       AS CHARACTER
    FIELD firstname     AS CHARACTER
    FIELD lastname      AS CHARACTER
    FIELD cardname      AS CHARACTER
    FIELD mobile        AS CHARACTER
    FIELD phone         AS CHARACTER
    FIELD postcode      AS CHARACTER
    FIELD fax           AS CHARACTER
    FIELD address1      AS CHARACTER
    FIELD address2      AS CHARACTER
    FIELD city          AS CHARACTER
    FIELD state         AS CHARACTER
    FIELD country       AS CHARACTER
    FIELD nationality   AS CHARACTER
    FIELD memberno      AS CHARACTER
    FIELD propID        AS CHARACTER
    FIELD profile       AS CHARACTER
    FIELD confno        AS CHARACTER
    FIELD note          AS CHARACTER
    FIELD passport      AS CHARACTER
    FIELD idcard        AS CHARACTER
    FIELD birthdate     AS CHARACTER
    FIELD gender        AS CHARACTER
    FIELD comp          AS CHARACTER
    FIELD compno        AS CHARACTER
.

DEFINE TEMP-TABLE nation 
    FIELD nr AS INTEGER
    FIELD nation-code AS CHARACTER
    FIELD nation-name AS CHARACTER
    FIELD nation-iso2 AS CHARACTER
    FIELD nation-iso3 AS CHARACTER.

DEFINE INPUT PARAMETER TABLE FOR nation.
DEFINE INPUT PARAMETER currDate AS DATE.
DEFINE INPUT PARAMETER propID   AS CHAR.
DEFINE INPUT PARAMETER tax-incl AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR p-list.
DEFINE OUTPUT PARAMETER TABLE FOR x-list.
DEFINE OUTPUT PARAMETER TABLE FOR r-list.

RUN ghs-p1-checkout.    
RUN ghs-x1-forecast.    

RUN ghs-r1-checkin.

/**************************************** PROCEDURE ****************************************/
PROCEDURE ghs-p1-checkout:
    DEFINE VARIABLE birthdate AS CHARACTER.
    DEFINE VARIABLE str-rsv AS CHARACTER.
    DEFINE VARIABLE contcode AS CHARACTER.
    DEFINE VARIABLE loop-i AS INTEGER.
    DEFINE VARIABLE curr-i AS INTEGER.
    
    DEFINE VARIABLE rsv-date AS DATE.
    DEFINE VARIABLE to-date AS DATE.
    DEFINE VARIABLE datum1 AS DATE.
    
    DEFINE VARIABLE flodging AS DECIMAL.
    DEFINE VARIABLE lodging AS DECIMAL.
    DEFINE VARIABLE breakfast AS DECIMAL.
    DEFINE VARIABLE lunch AS DECIMAL.
    DEFINE VARIABLE dinner AS DECIMAL.
    DEFINE VARIABLE others AS DECIMAL.
    DEFINE VARIABLE rmrate AS DECIMAL.
    DEFINE VARIABLE net-vat AS DECIMAL.
    DEFINE VARIABLE net-service AS DECIMAL.
    DEFINE VARIABLE vat AS DECIMAL.
    DEFINE VARIABLE service AS DECIMAL.
    DEFINE VARIABLE t-rmrev AS DECIMAL.
    DEFINE VARIABLE t-fbrev AS DECIMAL.
    DEFINE VARIABLE t-others AS DECIMAL.
    
    DEFINE VARIABLE ci-date AS CHARACTER.
    DEFINE VARIABLE co-date AS CHARACTER.
    
    DEFINE BUFFER gmember FOR guest.
    DEFINE BUFFER gcomp FOR guest.  

    FOR EACH res-line WHERE 
        res-line.resstatus = 8 AND res-line.active-flag = 2 AND res-line.abreise = currDate NO-LOCK,
        FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
        FIRST sourccod WHERE sourccod.source-code = reservation.resart NO-LOCK,
        FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
        FIRST queasy WHERE queasy.KEY EQ 152
            AND queasy.number1 EQ zimkateg.typ NO-LOCK:
        ASSIGN
            t-rmrev = 0
            t-fbrev = 0
            t-others = 0
            curr-i = 0.
        IF AVAILABLE gmember THEN
        DO:
            CREATE p-list.
            ASSIGN
                p-list.confno = propID + "-" + STRING(res-line.resnr) + STRING(res-line.reslinnr,"999")
                /*p-list.roomtype = zimkateg.kurzbez Commented by Irfan on 150518*/
                p-list.roomno = res-line.zinr
                p-list.roomrate = res-line.zipreis
                p-list.sourcename = sourccod.bezeich
                p-list.market = segment.bezeich
                p-list.note = res-line.bemerk
                p-list.memberno = ""
                p-list.reward   = ""
                p-list.profile = propID + "-" + STRING(gmember.gastnr)
                p-list.propID = propID
                p-list.gname = gmember.vorname1 + " " + gmember.NAME + "," + gmember.anrede1
            .    
    
            /*
            Irfan 150518
            add validation for room type requested by Seres Spring
            */
            IF propID MATCHES "*SSRS*" THEN
            DO:
                p-list.roomtype = queasy.char1.
            END.
            ELSE
            DO:
                p-list.roomtype = zimkateg.kurzbez.
            END.
    
            DO loop-i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                str-rsv = ENTRY(loop-i, res-line.zimmer-wunsch, ";").
                IF SUBSTR(str-rsv,1,6)   = "$CODE$"   THEN contcode     = SUBSTR(str-rsv,7).
            END.
    
            p-list.ratecode = contcode.
            IF SESSION:DATE-FORMAT = "dmy" THEN
                rsv-date = 
                    DATE(SUBSTR(res-line.reserve-char,7,2) + "/" +
                    SUBSTR(res-line.reserve-char,4,2) + "/" +
                    SUBSTR(res-line.reserve-char,1,2)).
            ELSE IF SESSION:DATE-FORMAT = "mdy" THEN
                rsv-date = 
                    DATE(SUBSTR(res-line.reserve-char,4,2) + "/" +
                    SUBSTR(res-line.reserve-char,7,2) + "/" +
                    SUBSTR(res-line.reserve-char,1,2)).
            ELSE rsv-date =  DATE(SUBSTR(res-line.reserve-char,1,8)).
    
            IF rsv-date NE ? THEN
                p-list.bookdate = STRING(YEAR(rsv-date),"9999") + "-" +
                                  STRING(MONTH(rsv-date),"99") + "-" +
                                  STRING(DAY(rsv-date),"99").
            ELSE p-list.bookdate = "".
    
            p-list.exportdate = STRING(YEAR(TODAY),"9999") + "-" +
                                  STRING(MONTH(TODAY),"99") + "-" +
                                  STRING(DAY(TODAY),"99").
    
            IF res-line.ankunft = res-line.abreise THEN to-date = res-line.abreise.
                ELSE to-date = res-line.abreise - 1.
            DO datum1 = res-line.ankunft TO to-date:
                curr-i = curr-i + 1.
                RUN ghs-get-room-breakdownbl.p(RECID(res-line),datum1, curr-i, 
                                       currDate, OUTPUT flodging, 
                                       OUTPUT lodging, OUTPUT breakfast,
                                       OUTPUT lunch, OUTPUT dinner,
                                       OUTPUT others, OUTPUT rmrate,
                                       OUTPUT net-vat,OUTPUT net-service,
                                       OUTPUT vat, OUTPUT service).

                IF NOT tax-incl THEN t-rmrev = t-rmrev + lodging - net-vat - net-service. /*this is exclude tax & service*/
                ELSE t-rmrev = t-rmrev + lodging.

                ASSIGN
                    /*t-rmrev = t-rmrev + lodging*/
                    t-fbrev = t-fbrev + breakfast + lunch + dinner
                    t-others = t-others + others.
            END.
    
            ASSIGN
                p-list.rmrev = ROUND(t-rmrev, 2)
                p-list.fbrev = ROUND(t-fbrev, 2)
                p-list.others = ROUND(t-others, 2)
                p-list.totrev = p-list.rmrev + p-list.fbrev + p-list.others.
            
            IF res-line.ankunft NE ? THEN
                ci-date = STRING(YEAR(res-line.ankunft),"9999") + "-" +
                          STRING(MONTH(res-line.ankunft),"99") + "-" +
                          STRING(DAY(res-line.ankunft),"99").
            ELSE ci-date = "".
            
            
    
            IF res-line.abreise NE ? THEN
                co-date = STRING(YEAR(res-line.abreise),"9999") + "-" +
                          STRING(MONTH(res-line.abreise),"99") + "-" +
                          STRING(DAY(res-line.abreise),"99").
            ASSIGN
                p-list.arrdate = ci-date
                p-list.depdate = co-date.
    
            FIND FIRST gcomp WHERE gcomp.gastnr = gmember.master-gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE gcomp THEN
                p-list.comp = gcomp.name + ", " + gcomp.anredefirma.
        END.
    END.

    FOR EACH p-list:
        ASSIGN
            /*IF 271118*/
            p-list.confno       = REPLACE(p-list.confno,","," ")
            p-list.arrdate      = REPLACE(p-list.arrdate,","," ")
            p-list.depdate      = REPLACE(p-list.depdate,","," ")
            p-list.roomno       = REPLACE(p-list.roomno,","," ")            
            p-list.roomtype     = REPLACE(p-list.roomtype,","," ")
            p-list.sourcename   = REPLACE(p-list.sourcename,","," ")
            p-list.memberno     = REPLACE(p-list.memberno,","," ")            
            p-list.propID       = REPLACE(p-list.propID,","," ")
            p-list.reward       = REPLACE(p-list.reward,","," ")            
            p-list.bookdate     = REPLACE(p-list.bookdate,","," ")
            p-list.exportdate   = REPLACE(p-list.exportdate,","," ")            
            p-list.market       = REPLACE(p-list.market,","," ")
            p-list.profil       = REPLACE(p-list.profil,","," ")            
            /*End IF*/
            p-list.gname        = REPLACE(p-list.gname,","," ")
            p-list.ratecode     = REPLACE(p-list.ratecode,CHR(10)," ")
            p-list.comp         = REPLACE(p-list.comp,","," ").        
    END.
END PROCEDURE.

PROCEDURE ghs-x1-forecast:
DEFINE VARIABLE birthdate AS CHARACTER.
DEFINE VARIABLE str-rsv AS CHARACTER.
DEFINE VARIABLE contcode AS CHARACTER.
DEFINE VARIABLE loop-i AS INTEGER.
DEFINE VARIABLE curr-i AS INTEGER.

DEFINE VARIABLE rsv-date AS DATE.
DEFINE VARIABLE to-date AS DATE.
DEFINE VARIABLE datum1 AS DATE.

DEFINE VARIABLE flodging AS DECIMAL.
DEFINE VARIABLE lodging AS DECIMAL.
DEFINE VARIABLE breakfast AS DECIMAL.
DEFINE VARIABLE lunch AS DECIMAL.
DEFINE VARIABLE dinner AS DECIMAL.
DEFINE VARIABLE others AS DECIMAL.
DEFINE VARIABLE rmrate AS DECIMAL.
DEFINE VARIABLE net-vat AS DECIMAL.
DEFINE VARIABLE net-service AS DECIMAL.
DEFINE VARIABLE vat AS DECIMAL.
DEFINE VARIABLE service AS DECIMAL.
DEFINE VARIABLE t-rmrev AS DECIMAL.
DEFINE VARIABLE t-fbrev AS DECIMAL.
DEFINE VARIABLE t-others AS DECIMAL.

DEFINE VARIABLE ci-date AS CHARACTER.
DEFINE VARIABLE co-date AS CHARACTER.

DEFINE BUFFER gmember FOR guest.
DEFINE BUFFER gcomp FOR guest.

    FOR EACH res-line WHERE 
        (res-line.ankunft LE currDate AND res-line.abreise GE currDate) OR 
        ((res-line.resstatus = 1 OR res-line.resstatus = 2 OR res-line.resstatus = 5 OR
        res-line.resstatus = 11) AND res-line.active-flag = 0)
        NO-LOCK,
        FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK,
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
        FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
        FIRST sourccod WHERE sourccod.source-code = reservation.resart NO-LOCK,
        /*FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr BY res-line.resnr:*/
        FIRST zimkateg WHERE zimkateg.zikatnr EQ res-line.zikatnr NO-LOCK,
        FIRST queasy WHERE queasy.KEY EQ 152
            AND queasy.number1 EQ zimkateg.typ NO-LOCK:
        ASSIGN
            t-rmrev = 0
            t-fbrev = 0
            t-others = 0
            curr-i = 0  .
        CREATE x-list.
        ASSIGN
            x-list.confno = propID + "-" + STRING(res-line.resnr) + STRING(res-line.reslinnr,"999")
            /*x-list.roomtype = zimkateg.kurzbez commented by Irfan on 150518*/
            x-list.roomrate = res-line.zipreis
            x-list.sourcename = sourccod.bezeich
            x-list.market = segment.bezeich
            x-list.note = res-line.bemerk
            x-list.memberno = ""
            x-list.profile = propID + "-" + STRING(gmember.gastnr)
            x-list.propID = propID
            x-list.gname = gmember.vorname1 + " " + gmember.NAME + "," + gmember.anrede1
            x-list.adult = res-line.erwachs
            x-list.child = res-line.kind1 + res-line.kind2
        .    
    
        /*
        Irfan 150518
        add validation for room type requested by Seres Spring
        */
    
        IF propID MATCHES "*SSRS*" THEN
        DO:
            x-list.roomtype = queasy.char1.
        END.
        ELSE
        DO:
            x-list.roomtype = zimkateg.kurzbez.
        END.
    
        IF res-line.resstatus NE 9 THEN x-list.bookstatus = "BOOKING".
        ELSE IF res-line.resstatus = 9 OR res-line.resstatus = 10 THEN
            x-list.bookstatus = "CANCEL".
    
        IF SESSION:DATE-FORMAT = "dmy" THEN
            rsv-date = 
                DATE(SUBSTR(res-line.reserve-char,7,2) + "/" +
                SUBSTR(res-line.reserve-char,4,2) + "/" +
                SUBSTR(res-line.reserve-char,1,2)).
        ELSE IF SESSION:DATE-FORMAT = "mdy" THEN
            rsv-date = 
                DATE(SUBSTR(res-line.reserve-char,4,2) + "/" +
                SUBSTR(res-line.reserve-char,7,2) + "/" +
                SUBSTR(res-line.reserve-char,1,2)).
        ELSE rsv-date =  DATE(SUBSTR(res-line.reserve-char,1,8)).
    
        IF rsv-date NE ? THEN
            x-list.bookdate = STRING(YEAR(rsv-date),"9999") + "-" +
                              STRING(MONTH(rsv-date),"99") + "-" +
                              STRING(DAY(rsv-date),"99").
        ELSE x-list.bookdate = "".
    
        IF res-line.ankunft = res-line.abreise THEN to-date = res-line.abreise.
            ELSE to-date = res-line.abreise - 1.
        DO datum1 = res-line.ankunft TO to-date:
            curr-i = curr-i + 1.
            RUN ghs-get-room-breakdownbl.p(RECID(res-line),datum1, curr-i, 
                                   currDate, OUTPUT flodging, 
                                   OUTPUT lodging, OUTPUT breakfast,
                                   OUTPUT lunch, OUTPUT dinner,
                                   OUTPUT others, OUTPUT rmrate,
                                   OUTPUT net-vat,OUTPUT net-service,
                                   OUTPUT vat, OUTPUT service).

            IF NOT tax-incl THEN t-rmrev = t-rmrev + lodging - net-vat - net-service. /*this is exlude tax & service*/
            ELSE t-rmrev = t-rmrev + lodging.
            
            ASSIGN
                /*t-rmrev = t-rmrev + lodging*/
                t-fbrev = t-fbrev + breakfast + lunch 
                t-others = t-others + others.
        END.
    
        ASSIGN
            x-list.rmrev = ROUND(t-rmrev, 2)
            x-list.fbrev = ROUND(t-fbrev, 2)
            x-list.others = ROUND(t-others, 2)
            x-list.totrev = x-list.rmrev + x-list.fbrev + x-list.others.
    
        IF res-line.ankunft NE ? THEN
            ci-date = STRING(YEAR(res-line.ankunft),"9999") + "-" +
                      STRING(MONTH(res-line.ankunft),"99") + "-" +
                      STRING(DAY(res-line.ankunft),"99").
        ELSE ci-date = "".
    
        IF res-line.abreise NE ? THEN
            co-date = STRING(YEAR(res-line.abreise),"9999") + "-" +
                      STRING(MONTH(res-line.abreise),"99") + "-" +
                      STRING(DAY(res-line.abreise),"99").
        ASSIGN
            x-list.arrdate = ci-date
            x-list.depdate = co-date.
    
        FIND FIRST gcomp WHERE gcomp.gastnr = gmember.master-gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE gcomp THEN
            x-list.comp = gcomp.name + ", " + gcomp.anredefirma.
    END.

    FOR EACH x-list:
        ASSIGN
            /*IF 271118*/
            x-list.confno       = REPLACE(x-list.confno,","," ")
            x-list.arrdate      = REPLACE(x-list.arrdate,","," ")
            x-list.depdate      = REPLACE(x-list.depdate,","," ")
            x-list.roomtype     = REPLACE(x-list.roomtype,","," ")
            x-list.sourcename   = REPLACE(x-list.sourcename,","," ")
            x-list.memberno     = REPLACE(x-list.memberno,","," ")
            x-list.profile      = REPLACE(x-list.profile,","," ")
            x-list.email        = REPLACE(x-list.email,","," ")
            x-list.propId       = REPLACE(x-list.propId,","," ")
            x-list.bookdate     = REPLACE(x-list.bookdate,","," ")
            x-list.market       = REPLACE(x-list.market,","," ")
            x-list.bookstatus   = REPLACE(x-list.bookstatus,","," ")
            /*End IF*/
            x-list.gname        = REPLACE(x-list.gname,","," ")
            x-list.comp         = REPLACE(x-list.comp,","," ").                    
    END.
END PROCEDURE.

PROCEDURE ghs-r1-checkin:
DEFINE VARIABLE birthdate AS CHARACTER.
DEFINE BUFFER gmember FOR guest.
DEFINE BUFFER gcomp FOR guest.

    FIND FIRST htparam WHERE htparam.paramnr EQ 87 NO-LOCK NO-ERROR.

    FOR EACH res-line WHERE 
        ((res-line.resstatus = 6 OR res-line.resstatus = 13) AND res-line.ankunft = currDate) OR
        (res-line.resstatus = 8 AND res-line.active-flag = 2
        AND res-line.ankunft = currDate AND res-line.abreise = currDate) OR
        (res-line.resstatus NE 9 AND res-line.resstatus NE 99 AND res-line.resstatus NE 12
         AND res-line.resstatus NE 10 AND res-line.ankunft = currDate AND currDate LT htparam.fdate) NO-LOCK,
        FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK:
        IF AVAILABLE gmember THEN
        DO:
            CREATE r-list.
            ASSIGN
                r-list.email = gmember.email-adr
                r-list.g-title = gmember.anrede1
                r-list.firstname = gmember.vorname1
                r-list.lastname = gmember.NAME
                r-list.cardname = gmember.vorname1 + " " + gmember.NAME
                r-list.mobile = gmember.mobil-telefon
                r-list.phone = gmember.telefon
                r-list.postcode  = gmember.plz
                r-list.fax = gmember.fax
                r-list.address1 = gmember.adresse1
                r-list.address2 = gmember.adresse2
                r-list.city = gmember.wohnort
                r-list.state = gmember.geburt-ort2
                r-list.country = gmember.land
                r-list.nationality = gmember.nation1
                r-list.memberno = ""
                r-list.propID = propID
                r-list.profile = propID + "-" + STRING(gmember.gastnr)
                r-list.confno = propID + "-" + STRING(res-line.resnr) + STRING(res-line.reslinnr,"999")
                r-list.note = gmember.bemerkung.
                
            IF gmember.geburt-ort1 = "Passport" THEN
                r-list.passport = gmember.ausweis-nr1.
            ELSE r-list.idcard = gmember.ausweis-nr1.
            IF gmember.geburtdatum1 EQ ? THEN
              birthdate = "".
            ELSE
              birthdate = STRING(YEAR(gmember.geburtdatum1),"9999") + "-" +
                          STRING(MONTH(gmember.geburtdatum1),"99") + "-" +
                          STRING(DAY(gmember.geburtdatum1),"99").
            r-list.birthdate = birthdate.
            IF gmember.geschlecht = "M" THEN
                r-list.gender = "Male".
            ELSE IF gmember.geschlecht = "F" THEN
                r-list.gender = "Female".
            FIND FIRST gcomp WHERE gcomp.gastnr = gmember.master-gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE gcomp THEN
                ASSIGN
                    r-list.comp = gcomp.name + ", " + gcomp.anredefirma
                    r-list.compno = gcomp.telefon.               
        END.
    END.

    FOR EACH r-list:
        FIND FIRST nation WHERE nation.nation-code EQ r-list.country NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN
        DO:
            ASSIGN
                /*country-code        = nation.nation-iso2*/
                r-list.country      = nation.nation-iso2
                r-list.nationality  = nation.nation-iso2.
        END.

        ASSIGN
            r-list.cardname     = REPLACE(r-list.cardname,","," ")
            r-list.firstname    = REPLACE(r-list.firstname,","," ")
            r-list.lastname     = REPLACE(r-list.lastname,","," ")
            r-list.comp         = REPLACE(r-list.comp,","," ")
            r-list.address1     = REPLACE(r-list.address1,","," ")
            r-list.address2     = REPLACE(r-list.address2,","," ")

            /*IF 221118*/
            r-list.email        = REPLACE(r-list.email, ","," ")
            r-list.g-title      = REPLACE(r-list.g-title,","," ")
            r-list.gender       = REPLACE(r-list.gender,","," ")
            r-list.birthdate    = REPLACE(r-list.birthdate,","," ")
            r-list.mobile       = REPLACE(r-list.mobile,","," ")
            r-list.phone        = REPLACE(r-list.phone,","," ")
            r-list.compno       = REPLACE(r-list.compno,","," ")
            r-list.postcode     = REPLACE(r-list.postcode,","," ")
            r-list.fax          = REPLACE(r-list.fax,","," ")
            r-list.city         = REPLACE(r-list.city,","," ")
            r-list.state        = REPLACE(r-list.state,","," ")
            /*country-code        = REPLACE(country-code,","," ")*/
            r-list.passport     = REPLACE(r-list.passport,","," ")
            r-list.idcard       = REPLACE(r-list.idcard,","," ")
            r-list.memberno     = REPLACE(r-list.memberno,","," ")
            r-list.propId       = REPLACE(r-list.propId,","," ")
            r-list.profile      = REPLACE(r-list.profile,","," ")
            r-list.confno       = REPLACE(r-list.confno,","," ")

            r-list.email        = REPLACE(r-list.email, CHR(10)," ")
            r-list.firstname    = REPLACE(r-list.firstname, CHR(10), " ")
            r-list.lastname     = REPLACE(r-list.lastname, CHR(10), " ")
            r-list.cardname     = REPLACE(r-list.cardname, CHR(10), " ")
            r-list.comp         = REPLACE(r-list.comp, CHR(10), " ")
            r-list.address1     = REPLACE(r-list.address1, CHR(10), " ")
            r-list.address2     = REPLACE(r-list.address2, CHR(10), " ")
            r-list.g-title      = REPLACE(r-list.g-title,CHR(10)," ")
            r-list.gender       = REPLACE(r-list.gender,CHR(10)," ")
            r-list.birthdate    = REPLACE(r-list.birthdate,CHR(10)," ")
            r-list.mobile       = REPLACE(r-list.mobile,CHR(10)," ")
            r-list.phone        = REPLACE(r-list.phone,CHR(10)," ")
            r-list.compno       = REPLACE(r-list.compno,CHR(10)," ")
            r-list.postcode     = REPLACE(r-list.postcode,CHR(10)," ")
            r-list.fax          = REPLACE(r-list.fax,CHR(10)," ")
            r-list.city         = REPLACE(r-list.city,CHR(10)," ")
            r-list.state        = REPLACE(r-list.state,CHR(10)," ")
            /*country-code        = REPLACE(country-code,CHR(10)," ")*/
            r-list.passport     = REPLACE(r-list.passport,CHR(10)," ")
            r-list.idcard       = REPLACE(r-list.idcard,CHR(10)," ")
            r-list.memberno     = REPLACE(r-list.memberno,CHR(10)," ")
            r-list.propId       = REPLACE(r-list.propId,CHR(10)," ")
            r-list.profile      = REPLACE(r-list.profile,CHR(10)," ")
            r-list.confno       = REPLACE(r-list.confno,CHR(10)," ")

            r-list.email        = REPLACE(r-list.email, CHR(13)," ")
            r-list.firstname    = REPLACE(r-list.firstname, CHR(13), " ")
            r-list.lastname     = REPLACE(r-list.lastname, CHR(13), " ")
            r-list.cardname     = REPLACE(r-list.cardname, CHR(13), " ")
            r-list.comp         = REPLACE(r-list.comp, CHR(13), " ")
            r-list.address1     = REPLACE(r-list.address1, CHR(13), " ")
            r-list.address2     = REPLACE(r-list.address2, CHR(13), " ")
            r-list.g-title      = REPLACE(r-list.g-title,CHR(13)," ")
            r-list.gender       = REPLACE(r-list.gender,CHR(13)," ")
            r-list.birthdate    = REPLACE(r-list.birthdate,CHR(13)," ")
            r-list.mobile       = REPLACE(r-list.mobile,CHR(13)," ")
            r-list.phone        = REPLACE(r-list.phone,CHR(13)," ")
            r-list.compno       = REPLACE(r-list.compno,CHR(13)," ")
            r-list.postcode     = REPLACE(r-list.postcode,CHR(13)," ")
            r-list.fax          = REPLACE(r-list.fax,CHR(13)," ")
            r-list.city         = REPLACE(r-list.city,CHR(13)," ")
            r-list.state        = REPLACE(r-list.state,CHR(13)," ")
            /*country-code        = REPLACE(country-code,CHR(13)," ")*/
            r-list.passport     = REPLACE(r-list.passport,CHR(13)," ")
            r-list.idcard       = REPLACE(r-list.idcard,CHR(13)," ")
            r-list.memberno     = REPLACE(r-list.memberno,CHR(13)," ")
            r-list.propId       = REPLACE(r-list.propId,CHR(13)," ")
            r-list.profile      = REPLACE(r-list.profile,CHR(13)," ")
            r-list.confno       = REPLACE(r-list.confno,CHR(13)," ")
            /*End IF*/

            r-list.note         = REPLACE(r-list.note,CHR(10)," ")
            r-list.note         = REPLACE(r-list.note,CHR(13)," ")
            r-list.note         = REPLACE(r-list.note,","," "). 

        r-list.country      = REPLACE(r-list.country,","," ").
        r-list.country      = REPLACE(r-list.country,CHR(10)," ").
        r-list.country      = REPLACE(r-list.country,CHR(13)," ").
        r-list.nationality  = REPLACE(r-list.nationality,","," ").
        r-list.nationality  = REPLACE(r-list.nationality,CHR(10)," ").
        r-list.nationality  = REPLACE(r-list.nationality,CHR(13)," ").
    END.
END PROCEDURE.
