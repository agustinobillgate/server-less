DEFINE TEMP-TABLE data-list
    FIELD resstatus AS CHARACTER
    FIELD bookchannel AS CHARACTER
    FIELD bookername AS CHARACTER
    FIELD resnr AS INTEGER
    FIELD reslinnr AS INTEGER
    FIELD totalprice AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD bookdate AS CHARACTER
    FIELD ankunft AS CHARACTER
    FIELD abreise AS CHARACTER
    FIELD staydate AS CHARACTER
    FIELD countryname AS CHARACTER
    FIELD currencycode AS CHARACTER
    FIELD firstname AS CHARACTER
    FIELD lastname AS CHARACTER
    FIELD roomtypename AS CHARACTER
    FIELD roomtypecode AS CHARACTER
    FIELD ratecode AS CHARACTER
    FIELD argt AS CHARACTER
    FIELD countrycode AS CHARACTER
    FIELD segment AS CHARACTER /*Add Segment RVN 06/09/2023*/
    FIELD nationalname AS CHARACTER /*Add Nationality RVN 29/09/2023*/
    FIELD nationalcode AS CHARACTER /*Add Nationality RVN 29/09/2023*/
    FIELD remark AS CHARACTER
.

DEFINE TEMP-TABLE output-list 
  FIELD flag AS INTEGER INITIAL 0 
  FIELD STR AS CHAR FORMAT "x(68)" 
  FIELD str1 AS CHAR.

/**/
DEFINE INPUT  PARAMETER fdate AS DATE.
DEFINE INPUT  PARAMETER tdate AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR data-list.
/**/
/*
DEFINE VARIABLE fdate AS DATE INITIAL 02/24/2024.
DEFINE VARIABLE tdate AS DATE INITIAL 02/28/2024.
*/

DEFINE VARIABLE loop-i      AS INT INIT 0.
DEFINE VARIABLE resv-date   AS DATE.
DEFINE VARIABLE str-rsv     AS CHAR.
DEFINE VARIABLE totalarr    AS INTEGER INIT 0.
DEFINE VARIABLE curr        AS INTEGER INIT 0.
DEFINE VARIABLE datum      AS DATE.
DEFINE VARIABLE datum1      AS DATE.
DEFINE VARIABLE new-status  AS CHAR    INIT "".
DEFINE VARIABLE p-87        AS DATE                NO-UNDO.

DEFINE VARIABLE serv            AS DECIMAL      NO-UNDO.
DEFINE VARIABLE vat             AS DECIMAL      NO-UNDO.
DEFINE VARIABLE flodging        AS DECIMAL.
DEFINE VARIABLE lodging         AS DECIMAL.
DEFINE VARIABLE breakfast       AS DECIMAL.
DEFINE VARIABLE lunch           AS DECIMAL.
DEFINE VARIABLE dinner          AS DECIMAL.
DEFINE VARIABLE others          AS DECIMAL.
DEFINE VARIABLE rmrate          AS DECIMAL.
DEFINE VARIABLE net-vat         AS DECIMAL.
DEFINE VARIABLE net-service     AS DECIMAL.
DEFINE VARIABLE totrevincl      AS DECIMAL.
DEFINE VARIABLE totrevexcl      AS DECIMAL.
DEFINE VARIABLE calrate          AS DECIMAL. /*Add Currency Value RVN 05/12/2023*/

EMPTY TEMP-TABLE data-list.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
p-87 = htparam.fdate.

IF fdate LT p-87 AND tdate LT p-87 THEN
DO:
    RUN process-data-old(fdate, tdate).
END.
ELSE IF fdate LT p-87 AND tdate GE p-87 THEN
DO:
    RUN process-data-old(fdate, p-87 - 1).

    FIND FIRST res-line WHERE res-line.resstatus NE 11 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 13 AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE res-line:
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr AND reservation.resdat GE p-87 AND reservation.resdat LE tdate NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE reservation:
            RUN process-data.

            FIND NEXT reservation WHERE reservation.resnr = res-line.resnr AND reservation.resdat GE p-87 AND reservation.resdat LE tdate NO-LOCK NO-ERROR.
        END.

        FIND NEXT res-line WHERE res-line.resstatus NE 11 AND res-line.resstatus NE 12
            AND res-line.resstatus NE 13 AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
    END.
END.
ELSE
DO:
    /*
    FIND FIRST reservation WHERE reservation.resdat GE fdate AND reservation.resdat LE tdate NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE reservation:
        FIND FIRST res-line WHERE res-line.resnr = reservation.resnr AND res-line.resstatus NE 11 
            AND res-line.resstatus NE 13 AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE res-line:
            RUN process-data.

            FIND NEXT res-line WHERE res-line.resnr = reservation.resnr AND res-line.resstatus NE 11 
                AND res-line.resstatus NE 13 AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
        END.

        FIND NEXT reservation WHERE reservation.resdat GE fdate AND reservation.resdat LE tdate NO-LOCK NO-ERROR.
    END.
    */

    FIND FIRST res-line WHERE res-line.resstatus NE 11 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 13 AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE res-line:
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr AND reservation.resdat GE fdate AND reservation.resdat LE tdate NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE reservation:
            RUN process-data.

            FIND NEXT reservation WHERE reservation.resnr = res-line.resnr AND reservation.resdat GE fdate AND reservation.resdat LE tdate NO-LOCK NO-ERROR.
        END.

        FIND NEXT res-line WHERE res-line.resstatus NE 11 AND res-line.resstatus NE 12
            AND res-line.resstatus NE 13 AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
    END.
END.

PROCEDURE process-data-old:

    DEFINE INPUT PARAMETER from-old AS DATE.
    DEFINE INPUT PARAMETER to-old AS DATE.

    DO datum = from-old TO to-old:
        FOR EACH genstat WHERE genstat.datum GE datum
          AND genstat.datum LE datum
          AND genstat.resstatus NE 11 
          AND genstat.resstatus NE 12
          AND genstat.resstatus NE 13 
          AND genstat.resnr NE 0 NO-LOCK :

            FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK NO-ERROR.
            FIND FIRST res-line WHERE res-line.resnr = genstat.resnr AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
            FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.
            FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK NO-ERROR.
            
            CREATE data-list.
            ASSIGN
                data-list.resnr         = genstat.resnr
                data-list.reslinnr      = genstat.res-int[1]
                /*data-list.totalprice    = res-line.zipreis*/
                data-list.argt          = res-line.arrangement
            .

            FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN
            DO:
                data-list.bookername = guest.vorname1 + " " + guest.NAME.
                RELEASE guest.

                data-list.bookername = REPLACE(data-list.bookername, CHR(10), " ").
                data-list.bookername = REPLACE(data-list.bookername, CHR(13), " ").
                data-list.bookername = REPLACE(data-list.bookername, CHR(59), " ").

            END.

            FIND FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN
            DO:
                data-list.lastname = guest.NAME.
                data-list.firstname = guest.vorname1.

                data-list.lastname = REPLACE(data-list.lastname, CHR(10), " ").
                data-list.lastname = REPLACE(data-list.lastname, CHR(13), " ").
                data-list.lastname = REPLACE(data-list.lastname, CHR(59), " ").

                data-list.firstname = REPLACE(data-list.firstname, CHR(10), " ").
                data-list.firstname = REPLACE(data-list.firstname, CHR(13), " ").
                data-list.firstname = REPLACE(data-list.firstname, CHR(59), " ").

                FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN 
                    ASSIGN
                        data-list.countryname = nation.bezeich
                        data-list.countrycode = nation.kurzbez.

                /*Add Nationality RVN 29/09/2023*/
                FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN 
                     ASSIGN
                        data-list.nationalname = nation.bezeich
                        data-list.nationalcode = nation.kurzbez.

                RELEASE guest.
            END.

            FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart NO-LOCK NO-ERROR.
            IF AVAILABLE sourccod THEN data-list.bookchannel = sourccod.bezeich.

            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR.
            IF AVAILABLE waehrung THEN 
            DO:

                calrate = 0.

                ASSIGN
                    data-list.currencycode = waehrung.wabkurz
                    calrate = waehrung.ankauf.
            END.

            FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK NO-ERROR.
            IF AVAILABLE zimkateg THEN 
                ASSIGN
                    data-list.roomtypename = zimkateg.bezeichnung
                    data-list.roomtypecode = zimkateg.kurzbez.

            DO loop-i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                str-rsv = ENTRY(loop-i, res-line.zimmer-wunsch, ";").
                IF SUBSTR(str-rsv,1,6) = "$CODE$" THEN data-list.ratecode = SUBSTR(str-rsv,7).
            END.
            /*
            IF SESSION:DATE-FORMAT = "dmy" THEN
                resv-date = 
                    DATE(SUBSTR(res-line.reserve-char,7,2) + "/" +
                    SUBSTR(res-line.reserve-char,4,2) + "/" +
                    SUBSTR(res-line.reserve-char,1,2)).
            ELSE IF SESSION:DATE-FORMAT = "mdy" THEN
                resv-date = 
                    DATE(SUBSTR(res-line.reserve-char,4,2) + "/" +
                    SUBSTR(res-line.reserve-char,7,2) + "/" +
                    SUBSTR(res-line.reserve-char,1,2)).
            ELSE resv-date =  DATE(SUBSTR(res-line.reserve-char,1,8)).

            data-list.bookdate = STRING(YEAR(resv-date),"9999") + "-" + 
                STRING(MONTH(resv-date),"99") + "-" + STRING(DAY(resv-date),"99").
            */
            data-list.bookdate = STRING(YEAR(reservation.resdat),"9999") + "-" + 
                STRING(MONTH(reservation.resdat),"99") + "-" + STRING(DAY(reservation.resdat),"99").
            data-list.ankunft = STRING(YEAR(res-line.ankunft),"9999") + "-" + 
                STRING(MONTH(res-line.ankunft),"99") + "-" + STRING(DAY(res-line.ankunft),"99").
            data-list.abreise = STRING(YEAR(res-line.abreise),"9999") + "-" + 
                STRING(MONTH(res-line.abreise),"99") + "-" + STRING(DAY(res-line.abreise),"99").

            /*Add Stay Date RVN 03/06/2024*/
            data-list.staydate = STRING(YEAR(datum),"9999") + "-" + 
                STRING(MONTH(datum),"99") + "-" + STRING(DAY(datum),"99").

            IF res-line.resstatus LE 5 THEN
                ASSIGN
                    data-list.resstatus = "new"
                    new-status = "new|init".
            IF res-line.resstatus = 6 OR res-line.resstatus = 8 THEN
                ASSIGN
                    data-list.resstatus = "modified"
                    new-status = "modify|init".
            IF res-line.resstatus = 9 OR res-line.resstatus = 99 OR res-line.resstatus = 10 THEN
                ASSIGN
                    data-list.resstatus = "cancelled"
                    new-status = "cancel|init".

            /*Add Segment RVN 06/09/2023*/
            FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK NO-ERROR.
            IF AVAILABLE segment THEN data-list.segment = segment.bemerk.

            ASSIGN 
                data-list.remark        = reservation.bemerk.

            data-list.remark = REPLACE(data-list.remark, CHR(10), " ").
            data-list.remark = REPLACE(data-list.remark, CHR(13), " ").
            data-list.remark = REPLACE(data-list.remark, CHR(59), " ").
        
            /*Add Lodging RVN 13/09/2023
            data-list.totalprice = data-list.totalprice + genstat.logis.
            */

            /*Update Lodging Calculation RVN 03/06/2024*/
            ASSIGN
                data-list.totalprice = genstat.logis.

            IF data-list.totalprice LT 0 THEN
                data-list.totalprice = 0.

            /* generate trigger as daily XML file */
            DO TRANSACTION.
                CREATE interface.
                ASSIGN
                    interface.key         = 10
                    interface.zinr        = res-line.zinr
                    interface.nebenstelle = ""
                    interface.intfield    = 0
                    interface.decfield    = 1
                    interface.int-time    = TIME
                    interface.intdate     = TODAY
                    interface.parameters  = new-status
                    interface.resnr       = res-line.resnr
                    interface.reslinnr    = res-line.reslinnr
                .
                FIND CURRENT interface NO-LOCK.
                RELEASE interface.
            END.
        END. /*END FOR EACH*/
    END. /*END DATUM*/
END PROCEDURE.


PROCEDURE process-data:

    DO datum1 = res-line.ankunft TO res-line.abreise - 1 :
        CREATE data-list.
        ASSIGN
            data-list.resnr         = res-line.resnr
            data-list.reslinnr      = res-line.reslinnr
            /*data-list.totalprice    = res-line.zipreis*/
            data-list.argt          = res-line.arrangement
        .
    
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN
        DO:
            data-list.bookername = guest.vorname1 + " " + guest.NAME.
            RELEASE guest.
        END.
    
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN
        DO:
            data-list.lastname = guest.NAME.
            data-list.firstname = guest.vorname1.
    
            FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
            IF AVAILABLE nation THEN 
                ASSIGN
                    data-list.countryname = nation.bezeich
                    data-list.countrycode = nation.kurzbez.
    
            /*Add Nationality RVN 29/09/2023*/
            FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR.
            IF AVAILABLE nation THEN 
                ASSIGN
                    data-list.nationalname = nation.bezeich
                    data-list.nationalcode = nation.kurzbez.
    
    
            RELEASE guest.
        END.
    
        FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart NO-LOCK NO-ERROR.
        IF AVAILABLE sourccod THEN data-list.bookchannel = sourccod.bezeich.
    
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN 
        DO:
    
            calrate = 0.
    
            ASSIGN
                data-list.currencycode = waehrung.wabkurz
                calrate = waehrung.ankauf.
        END.
            
    
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN 
            ASSIGN
                data-list.roomtypename = zimkateg.bezeichnung
                data-list.roomtypecode = zimkateg.kurzbez.
    
        DO loop-i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str-rsv = ENTRY(loop-i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str-rsv,1,6) = "$CODE$" THEN data-list.ratecode = SUBSTR(str-rsv,7).
        END.
    /*
        IF SESSION:DATE-FORMAT = "dmy" THEN
            resv-date = 
                DATE(SUBSTR(res-line.reserve-char,7,2) + "/" +
                SUBSTR(res-line.reserve-char,4,2) + "/" +
                SUBSTR(res-line.reserve-char,1,2)).
        ELSE IF SESSION:DATE-FORMAT = "mdy" THEN
            resv-date = 
                DATE(SUBSTR(res-line.reserve-char,4,2) + "/" +
                SUBSTR(res-line.reserve-char,7,2) + "/" +
                SUBSTR(res-line.reserve-char,1,2)).
        ELSE resv-date =  DATE(SUBSTR(res-line.reserve-char,1,8)).
    
        data-list.bookdate = STRING(YEAR(resv-date),"9999") + "-" + 
            STRING(MONTH(resv-date),"99") + "-" + STRING(DAY(resv-date),"99").
    */
        data-list.bookdate = STRING(YEAR(reservation.resdat),"9999") + "-" + 
            STRING(MONTH(reservation.resdat),"99") + "-" + STRING(DAY(reservation.resdat),"99").
        data-list.ankunft = STRING(YEAR(res-line.ankunft),"9999") + "-" + 
            STRING(MONTH(res-line.ankunft),"99") + "-" + STRING(DAY(res-line.ankunft),"99").
        data-list.abreise = STRING(YEAR(res-line.abreise),"9999") + "-" + 
            STRING(MONTH(res-line.abreise),"99") + "-" + STRING(DAY(res-line.abreise),"99").

        /*Add Stay Date RVN 03/06/2024*/
        data-list.staydate = STRING(YEAR(datum1),"9999") + "-" + 
            STRING(MONTH(datum1),"99") + "-" + STRING(DAY(datum1),"99").
    
        IF res-line.resstatus LE 5 THEN
            ASSIGN
                data-list.resstatus = "new"
                new-status = "new|init".
        IF res-line.resstatus = 6 OR res-line.resstatus = 8 THEN
            ASSIGN
                data-list.resstatus = "modified"
                new-status = "modify|init".
        IF res-line.resstatus = 9 OR res-line.resstatus = 99 OR res-line.resstatus = 10 THEN
            ASSIGN
                data-list.resstatus = "cancelled"
                new-status = "cancel|init".
    
        /*Add Segment RVN 06/09/2023*/
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN data-list.segment = segment.bemerk.
    
        ASSIGN 
            data-list.remark        = reservation.bemerk.
    
        data-list.remark = REPLACE(REPLACE(data-list.remark, CHR(10), " "), CHR(13), " ").

        /*Update Lodging Calculation RVN 03/06/2024*/
        ASSIGN
            lodging = 0.
    
        RUN get-room-breakdown.p(RECID(res-line),datum1, 1, 
                                 datum1, OUTPUT flodging, 
                                 OUTPUT lodging, OUTPUT breakfast,
                                 OUTPUT lunch, OUTPUT dinner,
                                 OUTPUT others, OUTPUT rmrate,
                                 OUTPUT net-vat,OUTPUT net-service).
    
        ASSIGN 
            data-list.totalprice = ROUND(lodging / calrate,2).
    
        /*Add Lodging RVN 13/09/2023
        totrevincl = 0.
        totrevexcl = 0.
        IF res-line.ankunft = res-line.abreise THEN
        DO:
            
            DO datum1 = res-line.ankunft TO res-line.abreise :
                ASSIGN
                    lodging = 0.
    
                RUN get-room-breakdown.p(RECID(res-line),datum1, 1, 
                                        datum1, OUTPUT flodging, 
                                        OUTPUT lodging, OUTPUT breakfast,
                                        OUTPUT lunch, OUTPUT dinner,
                                        OUTPUT others, OUTPUT rmrate,
                                        OUTPUT net-vat,OUTPUT net-service).
    
                data-list.staydate = STRING(YEAR(datum1),"9999") + "-" + 
                    STRING(MONTH(datum1),"99") + "-" + STRING(DAY(datum1),"99").
    
                totrevincl = totrevincl + flodging.
                totrevexcl = totrevexcl + lodging.
            END.
        END.
        ELSE
        DO:
            DO datum1 = res-line.ankunft TO res-line.abreise - 1 :
                ASSIGN
                    lodging = 0.
    
                RUN get-room-breakdown.p(RECID(res-line),datum1, 1, 
                                        datum1, OUTPUT flodging, 
                                        OUTPUT lodging, OUTPUT breakfast,
                                        OUTPUT lunch, OUTPUT dinner,
                                        OUTPUT others, OUTPUT rmrate,
                                        OUTPUT net-vat,OUTPUT net-service).
    
                totrevincl = totrevincl + flodging.
                totrevexcl = totrevexcl + lodging.
            END.
        END.
                
        IF totrevexcl = 0 THEN
            data-list.totalprice = ROUND(((res-line.zipreis * res-line.anztage) / calrate),2).
        ELSE 
            data-list.totalprice = ROUND(totrevexcl / calrate,2).
        */
    
        /* generate trigger as daily XML file */
        DO TRANSACTION.
            CREATE interface.
            ASSIGN
                interface.key         = 10
                interface.zinr        = res-line.zinr
                interface.nebenstelle = ""
                interface.intfield    = 0
                interface.decfield    = 1
                interface.int-time    = TIME
                interface.intdate     = TODAY
                interface.parameters  = new-status
                interface.resnr       = res-line.resnr
                interface.reslinnr    = res-line.reslinnr
            .
            FIND CURRENT interface NO-LOCK.
            RELEASE interface.
        END.
    END. /*END DO DATUM1*/
   
END PROCEDURE.

/*
FOR EACH data-list :
    DISPLAY data-list WITH WIDTH 260.
END.
*/
