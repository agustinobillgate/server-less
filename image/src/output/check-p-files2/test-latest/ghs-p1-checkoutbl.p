
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



DEFINE INPUT  PARAMETER datum AS DATE.
DEFINE INPUT  PARAMETER propID AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR p-list.
/*
datum = 02/21/18.
*/

/*
FIND FIRST htparam WHERE paramnr = 87.
datum = fdate - 1.
DEFINE VARIABLE datum AS DATE INITIAL 03/26/18.
DEFINE VARIABLE propID AS CHAR INIT "A1".
*/

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

FOR EACH res-line WHERE 
    res-line.resstatus = 8 AND res-line.active-flag = 2 AND res-line.abreise = datum NO-LOCK,
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
                                   datum, OUTPUT flodging, 
                                   OUTPUT lodging, OUTPUT breakfast,
                                   OUTPUT lunch, OUTPUT dinner,
                                   OUTPUT others, OUTPUT rmrate,
                                   OUTPUT net-vat,OUTPUT net-service,
                                   OUTPUT vat, OUTPUT service).
            ASSIGN
                t-rmrev = t-rmrev + lodging
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


/*
DEFINE VARIABLE filenm AS CHARACTER INIT "c:\e1-vhp\p1_checkout.csv".
DEFINE VARIABLE rc      AS CHARACTER NO-UNDO.

OUTPUT STREAM s1 TO Value(filenm) APPEND UNBUFFERED.
PUT STREAM s1 UNFORMATTED 
    "CONF_NO,ARRIVAL_DATE,DEPARTURE_DATE,ROOM_NO,ROOM_TYPE,RATE_CODE,RATES,GUEST_NAME,"
    "COMPANY_NAME,SOURCE_NAME,MEMBERSHIP_NO,TOTAL_REV,ROOM_REVENUE,FB_REVENUE,"
    "OTHER_REVENUE,PROPERTY_CODE,REWARD_TYPE,BOOKING_DATE,EXPORT_DATE,MARKET_CODE,PROFILE_NO" SKIP.
OUTPUT STREAM s1 CLOSE.

OUTPUT STREAM s1 TO Value(filenm) APPEND UNBUFFERED.  
    FOR EACH p-list:
        ASSIGN
            rc = REPLACE(p-list.ratecode,CHR(10)," ").
           
        p-list.gname = REPLACE(p-list.gname,","," ").
        PUT STREAM s1 UNFORMATTED 
            p-list.confno "," p-list.arrdate "," p-list.depdate "," p-list.roomno "," 
            p-list.roomtype "," rc "," p-list.roomrate "," p-list.gname ","
            p-list.comp "," p-list.sourcename "," p-list.memberno "," p-list.totrev "," 
            p-list.rmrev "," p-list.fbrev "," p-list.others "," p-list.propId ","
            p-list.reward "," p-list.bookdate "," p-list.exportdate "," p-list.market "," p-list.profil SKIP.
  END.
OUTPUT STREAM s1 CLOSE.
*/
