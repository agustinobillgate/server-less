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

/*Irfan 21/02/18 add countrymapping
DEFINE TEMP-TABLE nation 
    FIELD nr AS INTEGER
    FIELD nation-code AS CHARACTER
    FIELD nation-name AS CHARACTER
    FIELD nation-iso2 AS CHARACTER
    FIELD nation-iso3 AS CHARACTER.
*/
DEFINE INPUT  PARAMETER datum AS DATE.
DEFINE INPUT  PARAMETER propID AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR x-list.
/*
DEFINE VARIABLE datum AS DATE.
FIND FIRST htparam WHERE paramnr = 87.
datum = fdate - 1.
DEFINE VARIABLE propID AS CHAR INIT "A1".*/

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

DEFINE STREAM s1.
/*
/*Irfan 21/02/18 add mappingcountry*/
IF SEARCH("countrymapping.xml") NE ? THEN
    TEMP-TABLE nation:READ-XML("file",SEARCH("countrymapping.xml"),?,?,?).
*/
FOR EACH res-line WHERE 
    (res-line.ankunft LE datum AND res-line.abreise GE datum) OR 
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
                               datum, OUTPUT flodging, 
                               OUTPUT lodging, OUTPUT breakfast,
                               OUTPUT lunch, OUTPUT dinner,
                               OUTPUT others, OUTPUT rmrate,
                               OUTPUT net-vat,OUTPUT net-service,
                               OUTPUT vat, OUTPUT service).
        ASSIGN
            t-rmrev = t-rmrev + lodging
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

/*
DEFINE VARIABLE filenm AS CHARACTER INIT "c:\source10\GHS\x1_future.csv".

OUTPUT STREAM s1 TO Value(filenm) APPEND UNBUFFERED.
PUT STREAM s1 UNFORMATTED 
    "CONF_NO,ARRIVAL_DATE,DEPARTURE_DATE,ROOM_TYPE,RATES,GUEST_NAME,COMPANY_NAME,"
    "SOURCE_NAME,MEMBERSHIP_NO,PROFILE_NO,EMAIL,TOTAL_REV,ROOM_REVENUE,FB_REVENUE,"
    "OTHER_REVENUE,PROPERTY_CODE,BOOKING_DATE,MARKET_CODE,BOOKING_STATUS,"
    "NUM_OF_GUEST,DESCRIPTION" SKIP.
OUTPUT STREAM s1 CLOSE.

OUTPUT STREAM s1 TO Value(filenm) APPEND UNBUFFERED.  
    FOR EACH x-list:
        ASSIGN
            x-list.gname = REPLACE(x-list.gname,","," ")
            x-list.comp = REPLACE(x-list.comp,","," ").

        PUT STREAM s1 UNFORMATTED 
            x-list.confno "," x-list.arrdate "," x-list.depdate "," x-list.roomtype ","
            x-list.roomrate "," x-list.gname "," x-list.comp "," x-list.sourcename "," 
            x-list.memberno "," x-list.profile "," x-list.email "," x-list.totrev "," 
            x-list.rmrev "," x-list.fbrev "," x-list.others "," x-list.propId ","
            x-list.bookdate "," x-list.market "," x-list.bookstatus SKIP.
    END.
OUTPUT STREAM s1 CLOSE.*/



