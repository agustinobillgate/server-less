DEFINE TEMP-TABLE t-foreign-list
    FIELD resnr         LIKE res-line.resnr
    FIELD reslinnr      LIKE res-line.reslinnr
    FIELD NAME          LIKE res-line.name
    FIELD nation1       LIKE guest.nation1
    FIELD ausweis-nr1   LIKE guest.ausweis-nr1
    FIELD geburtdatum1  LIKE guest.geburtdatum1 
    FIELD zinr          LIKE res-line.zinr
    FIELD ankunft       LIKE res-line.ankunft
    FIELD abreise       LIKE res-line.abreise
    FIELD adresse1      LIKE guest.adresse1
    FIELD wohnort       LIKE guest.wohnort
    FIELD land          LIKE guest.land
    FIELD email-adr     LIKE guest.email-adr
    FIELD ankzeit       LIKE res-line.ankzeit
    FIELD abreisezeit   LIKE res-line.abreisezeit
    FIELD resstatus     LIKE res-line.resstatus
    FIELD erwachs       LIKE res-line.erwachs
    FIELD kind1         LIKE res-line.kind1
    FIELD gratis        LIKE res-line.gratis
    FIELD remark        LIKE guest.bemerkung
    FIELD i-purpose     AS CHARACTER
    FIELD gender        LIKE guest.geschlecht
    FIELD telefon       LIKE guest.telefon. /* Add by Michael @ 18/09/2018 for Ayola First request - ticket no BFA872 */

DEF TEMP-TABLE t-queasy    LIKE queasy.
DEFINE TEMP-TABLE summary-list
    FIELD summ-str  AS CHARACTER
    FIELD nation    AS CHARACTER
    FIELD pax       AS INTEGER
    .

DEFINE INPUT PARAMETER  dtype               AS INTEGER.
DEFINE INPUT PARAMETER  fdate               AS DATE.
DEFINE INPUT PARAMETER  from-date           AS DATE.
DEFINE INPUT PARAMETER  to-date             AS DATE.
DEFINE INPUT PARAMETER  ci-date             AS DATE.
DEFINE INPUT PARAMETER  all-nat             AS LOGICAL.
DEFINE INPUT PARAMETER  sorttype            AS INTEGER.
DEFINE INPUT PARAMETER  def-nat             AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR t-foreign-list.
DEFINE OUTPUT PARAMETER TABLE FOR summary-list.

DEFINE VARIABLE pax AS INTEGER NO-UNDO.

IF dtype EQ 0 THEN
DO:
    IF fdate = ci-date THEN 
    DO:
        IF NOT all-nat THEN 
        DO: 
            IF sorttype = 1 THEN 
            DO:
                FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
                    AND res-line.active-flag = 1 NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
                    AND guest.nation1 NE def-nat NO-LOCK 
                    BY res-line.ankunft BY guest.nation1 BY res-line.NAME 
                    BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            ELSE IF sorttype = 2 THEN 
            DO:
                FOR EACH res-line WHERE resstatus = 8 
                    AND res-line.active-flag = 2 
                    AND res-line.abreise = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
                    AND guest.nation1 NE def-nat NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            ELSE IF sorttype = 3 THEN 
            DO:
                FOR EACH res-line WHERE (resstatus = 1 OR resstatus = 11) 
                    AND res-line.active-flag = 0 
                    AND res-line.ankunft = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
                    AND guest.nation1 NE def-nat NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
        END. 
        ELSE 
        DO: 
            IF sorttype = 1 THEN 
            DO:
                FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
                    AND res-line.active-flag LE 1 
                    AND res-line.ankunft LE fdate 
                    AND res-line.abreise GT fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
                    BY res-line.ankunft BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            ELSE IF sorttype = 2 THEN 
            DO:
                FOR EACH res-line WHERE resstatus = 8 
                    AND res-line.active-flag = 2 
                    AND res-line.abreise = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            ELSE IF sorttype = 3 THEN 
            DO:
                FOR EACH res-line WHERE (resstatus = 1 OR resstatus = 11) 
                    AND res-line.active-flag = 0 
                    AND res-line.ankunft = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
        END. 
    END. 
    ELSE 
    DO: 
        IF NOT all-nat THEN 
        DO: 
            IF sorttype = 1 THEN 
            DO:
                FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
                    AND res-line.active-flag LE 1 
                    AND res-line.ankunft LE fdate 
                    AND res-line.abreise GT fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
                    AND guest.nation1 NE def-nat NO-LOCK 
                    BY res-line.ankunft BY guest.nation1 BY res-line.NAME 
                    BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            ELSE IF sorttype = 2 THEN
            DO:
                FOR EACH res-line WHERE resstatus = 8 
                    AND res-line.active-flag = 2 
                    AND res-line.abreise = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
                    AND guest.nation1 NE def-nat NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            ELSE IF sorttype = 3 THEN 
            DO:
                FOR EACH res-line WHERE (resstatus = 1 OR resstatus = 11 OR resstatus = 8) 
                    AND res-line.active-flag LE 2 
                    AND res-line.ankunft = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
                    AND guest.nation1 NE def-nat NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
        END. 
        ELSE 
        DO: 
            IF sorttype = 1 THEN 
            DO:
                FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
                    AND res-line.active-flag LE 1 
                    AND res-line.ankunft LE fdate 
                    AND res-line.abreise GT fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
                    BY res-line.ankunft BY guest.nation1 BY res-line.NAME 
                    BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            ELSE IF sorttype = 2 THEN 
            DO:
                FOR EACH res-line WHERE resstatus = 8 
                    AND res-line.active-flag = 2 
                    AND res-line.abreise = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            ELSE IF sorttype = 3 THEN 
            DO:
                FOR EACH res-line WHERE (resstatus = 1 OR resstatus = 11 OR resstatus = 8) 
                    AND res-line.active-flag LE 2 
                    AND res-line.ankunft = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
        END.
    END.
END.
ELSE IF dtype EQ 1 THEN
DO:
    IF NOT all-nat THEN 
    DO: 
        IF sorttype = 1 THEN 
        DO:
            FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13 OR res-line.resstatus = 8) 
                AND res-line.active-flag LE 2 
                AND NOT (res-line.ankunft GT to-date) 
                AND NOT (res-line.abreise - 1 LT from-date) NO-LOCK, 
                FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
                AND guest.nation1 NE def-nat NO-LOCK 
                BY res-line.ankunft BY guest.nation1 BY res-line.NAME 
                BY res-line.zinr :
                RUN create-foreign-list.
            END.
        END.
        ELSE IF sorttype = 2 THEN 
        DO:
            FOR EACH res-line WHERE resstatus = 8 
                AND res-line.active-flag = 2 
                AND res-line.abreise GE from-date
                AND res-line.abreise LE to-date NO-LOCK, 
                FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
                AND guest.nation1 NE def-nat NO-LOCK 
                BY guest.nation1 BY res-line.name BY res-line.zinr 
                BY res-line.abreise :
                RUN create-foreign-list.
            END.
        END.
        ELSE IF sorttype = 3 THEN 
        DO:
            FOR EACH res-line WHERE (resstatus = 1 OR resstatus = 11 OR resstatus = 8) 
                AND res-line.active-flag LE 2 
                AND res-line.ankunft GE from-date
                AND res-line.ankunft LE to-date NO-LOCK, 
                FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
                AND guest.nation1 NE def-nat NO-LOCK 
                BY guest.nation1 BY res-line.name BY res-line.zinr
                BY res-line.ankunft :
                RUN create-foreign-list.
            END.
        END.
    END. 
    ELSE 
    DO: 
        IF sorttype = 1 THEN 
        DO:
            FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13 OR res-line.resstatus = 8) 
                AND res-line.active-flag LE 2
                AND NOT (res-line.ankunft GT to-date) 
                AND NOT (res-line.abreise - 1 LT from-date) NO-LOCK, 
                FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
                BY res-line.ankunft BY guest.nation1 BY res-line.name BY res-line.zinr :
                RUN create-foreign-list.
            END.
        END.
        ELSE IF sorttype = 2 THEN 
        DO:
            FOR EACH res-line WHERE resstatus = 8 
                AND res-line.active-flag = 2 
                AND res-line.abreise GE from-date
                AND res-line.abreise LE to-date NO-LOCK, 
                FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
                BY guest.nation1 BY res-line.name BY res-line.zinr
                BY res-line.abreise :
                RUN create-foreign-list.
            END.
        END.
        ELSE IF sorttype = 3 THEN 
        DO:
            FOR EACH res-line WHERE (resstatus = 1 OR resstatus = 11 OR resstatus = 8) 
                AND res-line.active-flag LE 2 
                AND res-line.ankunft GE from-date
                AND res-line.ankunft LE to-date NO-LOCK, 
                FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
                BY guest.nation1 BY res-line.name BY res-line.zinr
                BY res-line.ankunft :
                RUN create-foreign-list.
            END.
        END.
    END. 
END.

/*FDL June 27, 2024 => Ticket 7B9FEC*/
CREATE summary-list.
summary-list.summ-str = "SUMMARY".
FOR EACH t-foreign-list NO-LOCK BY t-foreign-list.nation1:
    FIND FIRST summary-list WHERE summary-list.nation EQ t-foreign-list.nation1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE summary-list THEN
    DO:
        CREATE summary-list.
        summary-list.nation = t-foreign-list.nation1.
    END.
    summary-list.pax = summary-list.pax + 1.
END.

PROCEDURE create-foreign-list :
    DEFINE VARIABLE i       AS INTEGER.
    DEFINE VARIABLE str     AS CHARACTER.
    DEFINE VARIABLE purpose AS INT.

    CREATE t-foreign-list.
    ASSIGN
        t-foreign-list.resnr         = res-line.resnr
        t-foreign-list.reslinnr      = res-line.reslinnr
        t-foreign-list.NAME          = res-line.name
        t-foreign-list.nation1       = guest.nation1
        t-foreign-list.ausweis-nr1   = guest.ausweis-nr1 
        t-foreign-list.geburtdatum1  = guest.geburtdatum1
        t-foreign-list.zinr          = res-line.zinr
        t-foreign-list.ankunft       = res-line.ankunft
        t-foreign-list.abreise       = res-line.abreise
        t-foreign-list.adresse1      = guest.adresse1
        t-foreign-list.wohnort       = guest.wohnort
        t-foreign-list.land          = guest.land 
        t-foreign-list.email-adr     = guest.email-adr
        t-foreign-list.ankzeit       = res-line.ankzeit
        t-foreign-list.abreisezeit   = res-line.abreisezeit
        t-foreign-list.resstatus     = res-line.resstatus
        t-foreign-list.erwachs       = res-line.erwachs
        t-foreign-list.kind1         = res-line.kind1
        t-foreign-list.gratis        = res-line.gratis
        t-foreign-list.remark        = guest.bemerkung
        t-foreign-list.telefon       = guest.telefon. /* Add by Michael @ 18/09/2018 for Ayola First request - ticket no BFA872 */
        
    /*wen 160517 purpose for LnL*/
    DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        str = ENTRY(i, res-line.zimmer-wunsch, ";").
        IF SUBSTR(str,1,8) = "SEGM_PUR" THEN
            purpose        = INTEGER(SUBSTR(str,9)).
        IF purpose NE 0 THEN
        DO:
            RUN read-queasybl.p (1, 143, purpose, ?, OUTPUT TABLE t-queasy).
            FIND FIRST t-queasy NO-ERROR.
            IF AVAILABLE t-queasy THEN 
                t-foreign-list.i-purpose = t-queasy.char3.
        END.
       /*end*/
    END.    
END.
