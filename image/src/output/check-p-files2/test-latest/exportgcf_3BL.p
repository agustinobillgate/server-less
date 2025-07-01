    
DEFINE TEMP-TABLE tguest
    FIELD karteityp     LIKE guest.karteityp
    FIELD gastnr        LIKE guest.gastnr
    FIELD anlage-datum  LIKE guest.anlage-datum
    FIELD NAME          LIKE guest.NAME
    FIELD vorname1      LIKE guest.vorname1
    FIELD anredefirma   LIKE guest.anredefirma
    FIELD anrede1       LIKE guest.anrede1
    FIELD adresse1      LIKE guest.adresse1
    FIELD adresse2      LIKE guest.adresse2    
    FIELD adresse3      LIKE guest.adresse3
    FIELD plz           LIKE guest.plz
    FIELD wohnort       LIKE guest.wohnort
    FIELD land          LIKE guest.land
    FIELD email-adr     LIKE guest.email-adr
    FIELD telefon       LIKE guest.telefon
    FIELD geburtdatum1  LIKE guest.geburtdatum1
    FIELD geschlecht    LIKE guest.geschlecht
    FIELD propID        AS CHAR
    FIELD ankunft       AS DATE
    FIELD abreise       AS DATE
    FIELD zinr          AS CHAR
    FIELD sob           AS CHAR
    FIELD bezeich       AS CHAR
    FIELD tacomp        AS CHAR
    FIELD mobil-telefon   LIKE guest.mobil-telefon
.
DEF INPUT  PARAMETER fdate AS DATE.
DEF INPUT  PARAMETER tdate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR tguest.

DEFINE VARIABLE end-date AS DATE.
DEFINE VARIABLE tmp-date AS DATE.

DEFINE BUFFER b-guest FOR guest.

/*FIND LAST genstat NO-LOCK NO-ERROR.
end-date = genstat.datum.*/

FOR EACH genstat NO-LOCK BY genstat.datum DESC:
    IF genstat.gastnr NE ? THEN DO:
        end-date = genstat.datum.
        IF end-date NE ? THEN LEAVE.    
    END.
END.

IF tdate LT end-date THEN
    end-date = tdate.

IF fdate LT end-date THEN
    RUN create-genstat(fdate,end-date).
IF tdate GT end-date THEN
    tmp-date = end-date + 1.                        /* RULITA 131124 | Fixing for serverless */
    /* RUN create-rline(end-date + 1, tdate). */
    RUN create-rline(tmp-date,tdate).
IF fdate GE end-date THEN
    RUN create-rline(fdate,tdate).

FOR EACH tguest:
    FIND FIRST nation WHERE nation.kurzbez = tguest.land NO-LOCK NO-ERROR.
    IF AVAILABLE nation THEN tguest.bezeich = nation.bezeich.
    FIND FIRST res-line WHERE res-line.gastnrmember = tguest.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN 
            FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart NO-LOCK NO-ERROR.
        IF AVAILABLE sourccod THEN tguest.sob = sourccod.bezeich.
        ELSE tguest.sob = "".
    END.
    IF AVAILABLE res-line THEN
    DO:
        FIND FIRST b-guest WHERE b-guest.gastnr = res-line.gastnr 
            AND b-guest.karteityp NE 0 NO-LOCK NO-ERROR.
        IF AVAILABLE b-guest THEN 
            tguest.tacomp = STRING(b-guest.NAME + ", " + b-guest.anredefirma).
        ELSE tguest.tacomp = "".
    END.
    ELSE 
    DO:
        FIND FIRST history WHERE history.gastnr = tguest.gastnr 
            AND history.zi-wechsel = NO 
            AND history.reslinnr = 999 NO-LOCK NO-ERROR.
        IF AVAILABLE history THEN
        DO:
            FIND FIRST b-guest WHERE b-guest.gastnr = history.gastnr 
                NO-LOCK NO-ERROR.
            IF AVAILABLE b-guest THEN
                tguest.tacomp = STRING(b-guest.NAME + ", " + b-guest.vorname1).
        END.
        ELSE tguest.tacomp = "".
    END.
END.

PROCEDURE create-genstat:
    DEFINE INPUT PARAMETER date1 AS DATE.
    DEFINE INPUT PARAMETER date2 AS DATE.

    FOR EACH genstat WHERE genstat.datum GE date1 AND genstat.datum LE date2
        AND genstat.gastnr GT 0 
        AND genstat.zinr NE "" AND genstat.resstatus NE 11
        AND genstat.resstatus NE 13 AND genstat.resstatus NE 4
        AND genstat.resstatus NE 3
        AND genstat.resstatus NE 9 NO-LOCK BY genstat.gastnrmember:
        FIND FIRST guest WHERE guest.gastnr = genstat.gastnrmember 
            AND guest.karteityp = 0 AND guest.NAME NE ""
            NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN
        DO:
            FIND FIRST tguest WHERE tguest.gastnr = guest.gastnr NO-ERROR.
            IF NOT AVAILABLE tguest THEN
            DO:
                CREATE tguest.
                BUFFER-COPY guest TO tguest.
                ASSIGN
                    /* tguest.propId       = propId */
                    tguest.propId       = ""                                /* Rulita 231124 | Fixing issue 90 */
                    tguest.ankunft      = genstat.res-date[1]
                    tguest.abreise      = genstat.res-date[2]
                    tguest.zinr         = genstat.zinr
                    tguest.telefon      = guest.telefon
                    tguest.mobil-telefon = guest.mobil-telefon.

                /* Penambahan Validasi untuk memprioritaskan mobilenumber: CHIRAG 29Oct18  
                IF guest.mobil-telefon NE "" THEN
                    tguest.telefon = guest.mobil-telefon.
                ELSE
                    tguest.telefon = guest.telefon.*/
            END.
        END. 
    END.
END.

PROCEDURE create-rline:
    DEFINE INPUT PARAMETER date1 AS DATE.
    DEFINE INPUT PARAMETER date2 AS DATE.

    FOR EACH res-line WHERE active-flag = 1 
        AND res-line.resstatus NE 12 AND res-line.resstatus NE 9 
        AND res-line.ankunft LE date2 AND res-line.abreise GE date1 
        AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 
        NO-LOCK BY res-line.gastnrmember:
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
            AND guest.karteityp = 0 AND guest.NAME NE ""
            NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN
        DO:
            FIND FIRST tguest WHERE tguest.gastnr = guest.gastnr NO-ERROR.
            IF NOT AVAILABLE tguest THEN
            DO:
                CREATE tguest.
                BUFFER-COPY guest TO tguest.
                ASSIGN
                    /* tguest.propId       = propId */
                    tguest.propId       = ""                                /* Rulita 231124 | Fixing issue 90 */
                    tguest.ankunft = res-line.ankunft
                    tguest.abreise = res-line.abreise
                    tguest.zinr    = res-line.zinr
                    tguest.telefon      = guest.telefon
                    tguest.mobil-telefon = guest.mobil-telefon.

                /* Penambahan Validasi untuk memprioritaskan mobilenumber: CHIRAG 29Oct18  
                IF guest.mobil-telefon NE "" THEN
                    tguest.telefon = guest.mobil-telefon.
                ELSE
                    tguest.telefon = guest.telefon.*/
            END.
        END. 
    END.
END.



