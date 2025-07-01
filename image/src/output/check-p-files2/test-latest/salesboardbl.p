DEFINE TEMP-TABLE month-list
    FIELD gastnr   AS INT
    FIELD NAME     AS CHAR
    FIELD occ      AS INT
    FIELD rmRev    AS DECIMAL
    FIELD fbRev    AS DECIMAL
    FIELD otherRev AS DECIMAL.

DEFINE TEMP-TABLE mtd-list LIKE month-list.

DEFINE TEMP-TABLE tguest
    FIELD gastnr        AS INTEGER   FORMAT "->>>>>>>>>9"
    FIELD name          AS CHARACTER FORMAT "x(32)"
    FIELD adresse1      AS CHARACTER FORMAT "x(24)"
    FIELD adresse2      AS CHARACTER FORMAT "x(24)"
    FIELD wohnort       AS CHARACTER FORMAT "x(32)"
    FIELD plz           AS CHARACTER FORMAT "x(10)"
    FIELD land          AS CHARACTER FORMAT "x(3)"
    FIELD telefon       AS CHARACTER FORMAT "x(24)"
    FIELD segment1      AS CHARACTER FORMAT "x(20)"
.

DEFINE TEMP-TABLE reslist
    FIELD gastnr AS INT
    FIELD NAME AS CHAR
    FIELD rnight AS INT
    FIELD rrev AS DECIMAL
    FIELD datum AS DATE
.

DEFINE TEMP-TABLE year-list
    FIELD gastnr AS INT
    FIELD NAME AS CHAR
    FIELD rnight AS INT
    FIELD rrev AS DECIMAL
    FIELD curr-month AS INT
.

DEFINE INPUT  PARAMETER fdate AS DATE.
DEFINE INPUT  PARAMETER curr-task AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR month-list.
DEFINE OUTPUT PARAMETER TABLE FOR tguest.
DEFINE OUTPUT PARAMETER TABLE FOR mtd-list.
DEFINE OUTPUT PARAMETER TABLE FOR year-list.

/*DEFINE VARIABLE fdate AS DATE INIT 06/01/16.
DEFINE VARIABLE curr-task AS INT INIT 1 .*/

DEFINE VARIABLE fdate1 AS DATE.
DEFINE VARIABLE first-day AS DATE.

DEFINE VARIABLE frdate AS DATE.
DEFINE VARIABLE todate AS DATE.

DEFINE VARIABLE date1 AS DATE.
DEFINE VARIABLE date2 AS DATE.

DEFINE VARIABLE startdate AS DATE.
DEFINE VARIABLE enddate AS DATE.
DEFINE VARIABLE ci-date AS DATE.

DEFINE VARIABLE dummy-indv        AS INTEGER.
DEFINE VARIABLE dummy-walkin      AS INTEGER.
DEFINE VARIABLE bfast-art         AS INT.

DEFINE VARIABLE service AS DECIMAL.
DEFINE VARIABLE vat AS DECIMAL.

FIND FIRST htparam WHERE htparam.paramnr = 109 NO-LOCK. 
dummy-walkin = htparam.fint.

FIND FIRST htparam WHERE htparam.paramnr = 123 NO-LOCK. 
dummy-indv = htparam.fint.

FIND FIRST htparam WHERE paramnr = 125 NO-LOCK. 
bfast-art = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
ci-date = htparam.fdate.

IF curr-task = 0 THEN
    fdate1 = fdate - 1.
ELSE IF curr-task = 1 THEN
    fdate1 = fdate.

FOR EACH guest WHERE (guest.karteityp = 1 OR guest.karteityp = 2) 
    AND guest.anlage-datum = fdate1 NO-LOCK:
    CREATE tguest.
    ASSIGN 
        tguest.gastnr        = guest.gastnr
        tguest.name          = guest.NAME + " " + guest.anredefirma
        tguest.adresse1      = guest.adresse1
        tguest.adresse2      = guest.adresse2 + " " + guest.adresse3
        tguest.wohnort       = guest.wohnort
        tguest.plz           = guest.plz
        tguest.land          = guest.land
        tguest.telefon       = guest.telefon.

    FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr AND 
        guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
    IF AVAILABLE guestseg THEN 
    DO: 
        FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
            NO-LOCK NO-ERROR. 
        IF AVAILABLE segment THEN 
            tguest.segment1 = ENTRY(1, segment.bezeich, "$$0").
    END.
END.
/*
IF DAY(fdate) = 1 THEN
DO:
    ASSIGN
        frdate = DATE(MONTH(fdate1),1,YEAR(fdate1))
        todate = fdate1.

    FOR EACH genstat WHERE genstat.datum GE frdate
        AND genstat.datum LE todate
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES
        AND genstat.resstatus NE 13,
        FIRST guest WHERE guest.gastnr = genstat.gastnr
            AND guest.karteityp NE 0 AND genstat.gastnr NE dummy-walkin 
            AND guest.gastnr NE dummy-indv NO-LOCK:

        FIND FIRST month-list WHERE month-list.gastnr = genstat.gastnr
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE month-list THEN
        DO:
            CREATE month-list.
            ASSIGN
                month-list.gastnr = genstat.gastnr
                month-list.NAME   = guest.NAME + " " + guest.anredefirma.
        END.
        ASSIGN
            month-list.occ = month-list.occ + 1
            month-list.rmrev = month-list.rmrev + genstat.logis.

        FIND FIRST artikel WHERE artikel.zwkum = bfast-art NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN
            RUN calc-servvat.p(artikel.departement, artikel.artnr, genstat.datum, 
                artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).
        ASSIGN
            month-list.fbrev = month-list.fbrev + ((genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4]) / (1 + vat + service)) .
            month-list.otherRev = month-list.otherRev + (genstat.res-deci[5] / (1 + vat + service)) .
    END.                                                                                          
END.
*/
/*mtd*/
DO:
    ASSIGN
        frdate = DATE(MONTH(fdate1),1,YEAR(fdate1))
        enddate = DATE(12,31,YEAR(fdate1))
        todate = fdate1.

    FOR EACH genstat WHERE genstat.datum GE frdate
        AND genstat.datum LE todate
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES
        AND genstat.resstatus NE 13,
        FIRST guest WHERE guest.gastnr = genstat.gastnr
            AND (guest.karteityp = 1 OR guest.karteityp = 2) 
            /*AND genstat.gastnr NE dummy-walkin 
            AND guest.gastnr NE dummy-indv*/ NO-LOCK:

        FIND FIRST mtd-list WHERE mtd-list.gastnr = genstat.gastnr
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE mtd-list THEN
        DO:
            CREATE mtd-list.
            ASSIGN
                mtd-list.gastnr = genstat.gastnr
                mtd-list.NAME   = guest.NAME + " " + guest.anredefirma.
        END.
        ASSIGN
            mtd-list.occ = mtd-list.occ + 1
            mtd-list.rmrev = mtd-list.rmrev + genstat.logis.

        ASSIGN
            mtd-list.fbrev = mtd-list.fbrev + genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4].
            mtd-list.otherRev = mtd-list.otherRev + genstat.res-deci[5] .
    END.
END.

/*IF frdate LE fdate1 THEN
    RUN create-genstat(frdate,fdate1).
ci-date = 09/01/17.
enddate = 09/30/17.*/
RUN create-rline(ci-date, enddate).


PROCEDURE create-genstat:
    DEFINE INPUT PARAMETER date1 AS DATE.
    DEFINE INPUT PARAMETER date2 AS DATE.

    FOR EACH genstat WHERE genstat.datum GE date1 AND genstat.datum LE date2
        AND genstat.gastnr GT 0
        AND genstat.zinr NE ""
        AND genstat.segmentcode NE 0
        AND genstat.nationnr NE 0
        AND genstat.res-logic[2] EQ YES 
        AND genstat.resstatus NE 13 NO-LOCK,
        FIRST guest WHERE guest.gastnr = genstat.gastnr
            AND (guest.karteityp = 1 OR guest.karteityp = 2) NO-LOCK:
        FIND FIRST year-list WHERE year-list.curr-month = MONTH(genstat.datum)
            AND year-list.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE year-list THEN
        DO:
            CREATE year-list.
            ASSIGN
                year-list.curr-month = MONTH(genstat.datum)
                year-list.gastnr     = genstat.gastnr
                year-list.NAME       = guest.NAME + " " + guest.anredefirma
                year-list.rnight     = year-list.rnight + 1.

            IF genstat.gratis = 0 THEN
                year-list.rrev       = year-list.rrev + genstat.logis + genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5].
                                        
        END.
        ELSE
            year-list.rnight     = year-list.rnight + 1.
            IF genstat.gratis = 0 THEN
                year-list.rrev       = year-list.rrev + genstat.logis + genstat.res-deci[2] + genstat.res-deci[3] + genstat.res-deci[4] + genstat.res-deci[5].
    END.
END.

PROCEDURE create-rline:
    DEFINE INPUT PARAMETER date1 AS DATE.
    DEFINE INPUT PARAMETER date2 AS DATE.

    DEFINE VARIABLE dat1 AS DATE.
    DEFINE VARIABLE dat2 AS DATE.
    DEFINE VARIABLE datum AS DATE.
    DEFINE VARIABLE curr-i AS INT.

    DEFINE VARIABLE net-lodg    AS DECIMAL NO-UNDO.
    DEFINE VARIABLE Fnet-lodg   AS DECIMAL NO-UNDO.

    DEFINE VAR tot-breakfast    AS DECIMAL.
    DEFINE VAR tot-Lunch        AS DECIMAL.
    DEFINE VAR tot-dinner       AS DECIMAL.
    DEFINE VAR tot-Other        AS DECIMAL.
    DEFINE VAR tot-rmrev        AS DECIMAL.
    DEFINE VAR tot-vat          AS DECIMAL INITIAL 0.
    DEFINE VAR tot-service      AS DECIMAL INITIAL 0.

    FOR EACH res-line WHERE (res-line.resstatus LE 6 
        AND res-line.resstatus NE 4
        AND res-line.resstatus NE 3
        AND res-line.resstatus NE 11
        AND res-line.resstatus NE 13
        AND res-line.active-flag LE 1 
        AND NOT (res-line.ankunft GT date2) 
        AND NOT (res-line.abreise LT date1))

        OR (res-line.active-flag = 2 AND res-line.resstatus = 8
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)

        AND res-line.gastnr GT 0 
        AND res-line.l-zuordnung[3] = 0  
        USE-INDEX gnrank_ix NO-LOCK,
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
        FIRST guest WHERE guest.gastnr = res-line.gastnr
            AND (guest.karteityp = 1 OR guest.karteityp = 2) NO-LOCK
        BY res-line.resnr BY res-line.reslinnr DESCENDING:

        dat1 = date1. 
        IF res-line.ankunft GT dat1 THEN dat1 = res-line.ankunft. 
        
        IF res-line.abreise = res-line.ankunft THEN
            dat2 = res-line.abreise.
        ELSE dat2 = res-line.abreise - 1.
        IF dat2 GT date2 THEN dat2 = date2. 

        curr-i = 0.

        /*IF res-line.gastnr = 224 THEN
        DO:
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK NO-ERROR.

            FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart
            NO-LOCK NO-ERROR.

            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
            

            DISP dat1 dat2 res-line.ankunft res-line.abreise res-line.resstatus res-line.active-flag res-line.zimmerfix AVAILABLE segment
                AVAILABLE sourccod AVAILABLE zimmer "===" res-line.zinr zimmer.zinr.
        END. */
        
        DO datum = dat1 TO dat2:
            curr-i = curr-i + 1.
            FIND FIRST year-list WHERE year-list.curr-month = MONTH(datum)
                AND year-list.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE year-list THEN
            DO:
                CREATE year-list.
                ASSIGN
                    year-list.curr-month = MONTH(datum)
                    year-list.gastnr     = res-line.gastnr
                    year-list.NAME       = guest.NAME + " " + guest.anredefirma.

                IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND NOT res-line.zimmerfix THEN
                    year-list.rnight     = year-list.rnight + res-line.zimmeranz.
                IF res-line.zipreis NE 0 THEN
                DO:
                    RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, ci-date,
                                     OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                     OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                     OUTPUT tot-dinner, OUTPUT tot-other,
                                     OUTPUT tot-rmrev, OUTPUT tot-vat,
                                     OUTPUT tot-service).
                    year-list.rrev = year-list.rrev + net-lodg + tot-breakfast + tot-lunch + tot-dinner + tot-other.
                END.
            END.
            ELSE
            DO:
                IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND NOT res-line.zimmerfix THEN
                    year-list.rnight     = year-list.rnight + res-line.zimmeranz.
                IF res-line.zipreis NE 0 THEN
                DO:
                    RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, ci-date,
                                     OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                     OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                     OUTPUT tot-dinner, OUTPUT tot-other,
                                     OUTPUT tot-rmrev, OUTPUT tot-vat,
                                     OUTPUT tot-service).
                    year-list.rrev = year-list.rrev + net-lodg + tot-breakfast + tot-lunch + tot-dinner + tot-other.
                END.
            END.                                                             
        END.                                                                 
    END.
END.

/*
DEF VAR a AS INT.
DEF VAR b AS DEC.
FOR EACH year-list BY year-list.NAME :
    a = a + year-list.rnight.
    b = b + year-list.rrev.
    DISP year-list.rnight year-list.NAME  year-list.gastnr year-list.rrev FORMAT ">>>,>>>,>>>,>>9.99".
END.
DISP a B FORMAT ">>>,>>>,>>>,>>9.99".*/













