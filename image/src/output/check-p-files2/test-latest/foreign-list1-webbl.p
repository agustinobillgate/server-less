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
    FIELD telefon       LIKE guest.telefon  /* Add by Michael @ 18/09/2018 for Ayola First request - ticket no BFA872 */
    FIELD guest-stat    AS INTEGER  /* Naufal Afthar - DC8DD2 -> store guest status*/
    FIELD rm-qty        LIKE res-line.zimmeranz. /* Naufal Afthar - DC8DD2 */

DEF TEMP-TABLE t-queasy    LIKE queasy.
DEFINE TEMP-TABLE summary-list
    FIELD summ-str  AS CHARACTER
    FIELD nation    AS CHARACTER
    FIELD pax       AS INTEGER
    FIELD nation-remark AS CHARACTER
    /* Naufal Afthar - DC8DD2 -> add pax and anz breakdown for all*/
    FIELD pax-inhouse AS INTEGER
    FIELD pax-depart  AS INTEGER
    FIELD pax-arrival AS INTEGER
    /* Naufal Afthar - 6403D8*/
    FIELD pax-arrived AS INTEGER
    FIELD pax-departed AS INTEGER
    FIELD anz-inhouse AS INTEGER
    FIELD anz-depart  AS INTEGER
    FIELD anz-arrival AS INTEGER
    /* Naufal Afthar - 6403D8*/
    FIELD anz-arrived AS INTEGER
    FIELD anz-departed AS INTEGER
    .

/* Naufal Afthar - DC8DD2 -> Count total for ALL case*/
DEFINE VARIABLE tot-pax-inhouse AS INTEGER.
DEFINE VARIABLE tot-pax-depart  AS INTEGER.
DEFINE VARIABLE tot-pax-arrival AS INTEGER.
DEFINE VARIABLE tot-pax-arrived AS INTEGER.
DEFINE VARIABLE tot-pax-departed AS INTEGER.
DEFINE VARIABLE tot-anz-inhouse AS INTEGER.
DEFINE VARIABLE tot-anz-depart  AS INTEGER.
DEFINE VARIABLE tot-anz-arrival AS INTEGER.
DEFINE VARIABLE tot-anz-arrived AS INTEGER.
DEFINE VARIABLE tot-anz-departed AS INTEGER.
DEFINE VARIABLE curr-status AS INTEGER INIT 0.
DEFINE VARIABLE curr-date AS DATE.

DEFINE VARIABLE tot-local AS INTEGER.
DEFINE VARIABLE tot-foreign AS INTEGER.

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
                FOR EACH res-line WHERE (res-line.resstatus = 6 OR res-line.resstatus = 13) 
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
                FOR EACH res-line WHERE res-line.resstatus = 8 
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
                FOR EACH res-line WHERE (res-line.resstatus = 1 OR res-line.resstatus = 11) 
                    AND res-line.active-flag = 0 
                    AND res-line.ankunft = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
                    AND guest.nation1 NE def-nat NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            /* Naufal Afthar - DC8DD2 -> add all case*/
            ELSE IF sorttype EQ 4 THEN
            DO:
                FOR EACH res-line WHERE ((res-line.resstatus = 6 OR res-line.resstatus = 13) 
                    AND res-line.active-flag = 1)
                    OR (res-line.resstatus = 8 
                    AND res-line.active-flag = 2 
                    AND res-line.abreise = fdate)
                    OR ((res-line.resstatus = 1 OR res-line.resstatus = 11) 
                    AND res-line.active-flag = 0 
                    AND res-line.ankunft = fdate) NO-LOCK,
                    FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember
                    AND guest.nation1 NE def-nat NO-LOCK:
                    RUN create-foreign-list.
                END.
            END.
        END. 
        ELSE 
        DO: 
            IF sorttype = 1 THEN 
            DO:
                FOR EACH res-line WHERE (res-line.resstatus = 6 OR res-line.resstatus = 13) 
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
                FOR EACH res-line WHERE res-line.resstatus = 8 
                    AND res-line.active-flag = 2 
                    AND res-line.abreise = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            ELSE IF sorttype = 3 THEN 
            DO:
                FOR EACH res-line WHERE (res-line.resstatus = 1 OR res-line.resstatus = 11) 
                    AND res-line.active-flag = 0 
                    AND res-line.ankunft = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            /* Naufal Afthar - DC8DD2 -> add all case*/
            ELSE IF sorttype EQ 4 THEN
            DO:
                FOR EACH res-line WHERE ((res-line.resstatus = 6 OR res-line.resstatus = 13) 
                    AND res-line.active-flag LE 1 
                    AND res-line.ankunft LE fdate 
                    AND res-line.abreise GT fdate)
                    OR (res-line.resstatus = 8 
                    AND res-line.active-flag = 2 
                    AND res-line.abreise = fdate)
                    OR ((res-line.resstatus = 1 OR res-line.resstatus = 11) 
                    AND res-line.active-flag = 0 
                    AND res-line.ankunft = fdate) NO-LOCK,
                    FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK:
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
                FOR EACH res-line WHERE (res-line.resstatus = 6 OR res-line.resstatus = 13) 
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
                FOR EACH res-line WHERE res-line.resstatus = 8 
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
                FOR EACH res-line WHERE (res-line.resstatus = 1 OR res-line.resstatus = 11 OR res-line.resstatus = 8) 
                    AND res-line.active-flag LE 2 
                    AND res-line.ankunft = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
                    AND guest.nation1 NE def-nat NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            /* Naufal Afthar - DC8DD2 -> add all case*/
            ELSE IF sorttype EQ 4 THEN
            DO:
                FOR EACH res-line WHERE ((res-line.resstatus = 6 OR res-line.resstatus = 13) 
                    AND res-line.active-flag LE 1 
                    AND res-line.ankunft LE fdate 
                    AND res-line.abreise GT fdate)
                    OR (res-line.resstatus = 8 
                    AND res-line.active-flag = 2 
                    AND res-line.abreise = fdate)
                    OR ((res-line.resstatus = 1 OR res-line.resstatus = 11 OR res-line.resstatus = 8) 
                    AND res-line.active-flag LE 2 
                    AND res-line.ankunft = fdate) NO-LOCK,
                    FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember 
                    AND guest.nation1 NE def-nat NO-LOCK:
                    RUN create-foreign-list.
                END.
            END.
        END. 
        ELSE 
        DO: 
            IF sorttype = 1 THEN 
            DO:
                FOR EACH res-line WHERE (res-line.resstatus = 6 OR res-line.resstatus = 13) 
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
                FOR EACH res-line WHERE res-line.resstatus = 8 
                    AND res-line.active-flag = 2 
                    AND res-line.abreise = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            ELSE IF sorttype = 3 THEN 
            DO:
                FOR EACH res-line WHERE (res-line.resstatus = 1 OR res-line.resstatus = 11 OR res-line.resstatus = 8) 
                    AND res-line.active-flag LE 2 
                    AND res-line.ankunft = fdate NO-LOCK, 
                    FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
                    BY guest.nation1 BY res-line.name BY res-line.zinr :
                    RUN create-foreign-list.
                END.
            END.
            /* Naufal Afthar - DC8DD2 -> add all case*/
            ELSE IF sorttype EQ 4 THEN
            DO:
                FOR EACH res-line WHERE ((res-line.resstatus = 6 OR res-line.resstatus = 13) 
                    AND res-line.active-flag LE 1 
                    AND res-line.ankunft LE fdate 
                    AND res-line.abreise GT fdate)
                    OR (res-line.resstatus = 8 
                    AND res-line.active-flag = 2 
                    AND res-line.abreise = fdate)
                    OR ((res-line.resstatus = 1 OR res-line.resstatus = 11 OR res-line.resstatus = 8) 
                    AND res-line.active-flag LE 2 
                    AND res-line.ankunft = fdate) NO-LOCK,
                    FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK:
                    RUN create-foreign-list.
                END.
            END.
        END.
    END.
END.
/* ELSE IF dtype EQ 1 THEN                                                                                             */
/* DO:                                                                                                                 */
/*     IF NOT all-nat THEN                                                                                             */
/*     DO:                                                                                                             */
/*         IF sorttype = 1 THEN                                                                                        */
/*         DO:                                                                                                         */
/*             FOR EACH res-line WHERE (res-line.resstatus = 6 OR res-line.resstatus = 13 OR res-line.resstatus = 8)   */
/*                 AND res-line.active-flag LE 2                                                                       */
/*                 AND NOT (res-line.ankunft GT to-date)                                                               */
/*                 AND NOT (res-line.abreise - 1 LT from-date) NO-LOCK,                                                */
/*                 FIRST guest WHERE guest.gastnr = res-line.gastnrmember                                              */
/*                 AND guest.nation1 NE def-nat NO-LOCK                                                                */
/*                 BY res-line.ankunft BY guest.nation1 BY res-line.NAME                                               */
/*                 BY res-line.zinr :                                                                                  */
/*                 RUN create-foreign-list.                                                                            */
/*             END.                                                                                                    */
/*         END.                                                                                                        */
/*         ELSE IF sorttype = 2 THEN                                                                                   */
/*         DO:                                                                                                         */
/*             FOR EACH res-line WHERE res-line.resstatus = 8                                                          */
/*                 AND res-line.active-flag = 2                                                                        */
/*                 AND res-line.abreise GE from-date                                                                   */
/*                 AND res-line.abreise LE to-date NO-LOCK,                                                            */
/*                 FIRST guest WHERE guest.gastnr = res-line.gastnrmember                                              */
/*                 AND guest.nation1 NE def-nat NO-LOCK                                                                */
/*                 BY guest.nation1 BY res-line.name BY res-line.zinr                                                  */
/*                 BY res-line.abreise :                                                                               */
/*                 RUN create-foreign-list.                                                                            */
/*             END.                                                                                                    */
/*         END.                                                                                                        */
/*         ELSE IF sorttype = 3 THEN                                                                                   */
/*         DO:                                                                                                         */
/*             FOR EACH res-line WHERE (res-line.resstatus = 1 OR res-line.resstatus = 11 OR res-line.resstatus = 8)   */
/*                 AND res-line.active-flag LE 2                                                                       */
/*                 AND res-line.ankunft GE from-date                                                                   */
/*                 AND res-line.ankunft LE to-date NO-LOCK,                                                            */
/*                 FIRST guest WHERE guest.gastnr = res-line.gastnrmember                                              */
/*                 AND guest.nation1 NE def-nat NO-LOCK                                                                */
/*                 BY guest.nation1 BY res-line.name BY res-line.zinr                                                  */
/*                 BY res-line.ankunft :                                                                               */
/*                 RUN create-foreign-list.                                                                            */
/*             END.                                                                                                    */
/*                                                                                                                     */
/*         END.                                                                                                        */
/*         ELSE IF sorttype EQ 4 THEN /* Naufal Afthar - DC8DD2 -> add all case*/                                      */
/*         DO:                                                                                                         */
/*             FOR EACH res-line WHERE ((res-line.resstatus = 6 OR res-line.resstatus = 13 OR res-line.resstatus = 8)  */
/*                 AND res-line.active-flag LE 2                                                                       */
/*                 AND NOT (res-line.ankunft GT to-date)                                                               */
/*                 AND NOT (res-line.abreise - 1 LT from-date))                                                        */
/*                 OR (res-line.resstatus = 8                                                                          */
/*                 AND res-line.active-flag = 2                                                                        */
/*                 AND res-line.abreise GE from-date                                                                   */
/*                 AND res-line.abreise LE to-date)                                                                    */
/*                 OR ((res-line.resstatus = 1 OR res-line.resstatus = 11 OR res-line.resstatus = 8)                   */
/*                 AND res-line.active-flag LE 2                                                                       */
/*                 AND res-line.ankunft GE from-date                                                                   */
/*                 AND res-line.ankunft LE to-date) NO-LOCK,                                                           */
/*                 FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember                                             */
/*                 AND guest.nation1 NE def-nat NO-LOCK:                                                               */
/*                 RUN create-foreign-list.                                                                            */
/*             END.                                                                                                    */
/*         END.                                                                                                        */
/*     END.                                                                                                            */
/*     ELSE                                                                                                            */
/*     DO:                                                                                                             */
/*         IF sorttype = 1 THEN                                                                                        */
/*         DO:                                                                                                         */
/*             FOR EACH res-line WHERE (res-line.resstatus = 6 OR res-line.resstatus = 13 OR res-line.resstatus = 8)   */
/*                 AND res-line.active-flag LE 2                                                                       */
/*                 AND NOT (res-line.ankunft GT to-date)                                                               */
/*                 AND NOT (res-line.abreise - 1 LT from-date) NO-LOCK,                                                */
/*                 FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK                                      */
/*                 BY res-line.ankunft BY guest.nation1 BY res-line.name BY res-line.zinr :                            */
/*                 RUN create-foreign-list.                                                                            */
/*             END.                                                                                                    */
/*         END.                                                                                                        */
/*         ELSE IF sorttype = 2 THEN                                                                                   */
/*         DO:                                                                                                         */
/*             FOR EACH res-line WHERE res-line.resstatus = 8                                                          */
/*                 AND res-line.active-flag = 2                                                                        */
/*                 AND res-line.abreise GE from-date                                                                   */
/*                 AND res-line.abreise LE to-date NO-LOCK,                                                            */
/*                 FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK                                      */
/*                 BY guest.nation1 BY res-line.name BY res-line.zinr                                                  */
/*                 BY res-line.abreise :                                                                               */
/*                 RUN create-foreign-list.                                                                            */
/*             END.                                                                                                    */
/*         END.                                                                                                        */
/*         ELSE IF sorttype = 3 THEN                                                                                   */
/*         DO:                                                                                                         */
/*             FOR EACH res-line WHERE res-line.resstatus NE 3                                                         */
/*                 AND res-line.active-flag EQ 0                                                                       */
/*                 AND res-line.ankunft GE from-date                                                                   */
/*                 AND res-line.ankunft LE to-date NO-LOCK,                                                            */
/*                 FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK                                      */
/*                 BY guest.nation1 BY res-line.name BY res-line.zinr                                                  */
/*                 BY res-line.ankunft :                                                                               */
/*                 RUN create-foreign-list.                                                                            */
/*             END.                                                                                                    */
/*         END.                                                                                                        */
/*         ELSE IF sorttype EQ 4 THEN /* Naufal Afthar - DC8DD2 -> add all case*/                                      */
/*         DO:                                                                                                         */
/*              FOR EACH res-line WHERE ((res-line.resstatus = 6 OR res-line.resstatus = 13 OR res-line.resstatus = 8) */
/*                 AND res-line.active-flag LE 2                                                                       */
/*                 AND NOT (res-line.ankunft GT to-date)                                                               */
/*                 AND NOT (res-line.abreise - 1 LT from-date))                                                        */
/*                 OR (res-line.resstatus = 8                                                                          */
/*                 AND res-line.active-flag = 2                                                                        */
/*                 AND res-line.abreise GE from-date                                                                   */
/*                 AND res-line.abreise LE to-date)                                                                    */
/*                 OR (res-line.resstatus NE 3                                                                         */
/*                 AND res-line.active-flag EQ 0                                                                       */
/*                 AND res-line.ankunft GE from-date                                                                   */
/*                 AND res-line.ankunft LE to-date) NO-LOCK,                                                           */
/*                 FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK:                                    */
/*                 RUN create-foreign-list.                                                                            */
/*             END.                                                                                                    */
/*         END.                                                                                                        */
/*     END.                                                                                                            */
/* END.                                                                                                                */
ELSE IF dtype EQ 1 THEN
DO:
    IF sorttype EQ 1 THEN
    DO:
        IF to-date GE ci-date THEN RUN create-inhouse.
        ELSE RUN create-inhouse2.
    END.
    ELSE IF sorttype EQ 2 THEN RUN create-foreign-departure.
    ELSE IF sorttype EQ 3 THEN RUN create-foreign-arrival.
    ELSE IF sorttype EQ 4 THEN
    DO:
        IF to-date GE ci-date THEN RUN create-inhouse.
        ELSE RUN create-inhouse2.

        RUN create-foreign-departure.
        RUN create-foreign-arrival.
        RUN create-foreign-arrived-today. 
        RUN create-foreign-departed-today.
    END.
    ELSE IF sorttype EQ 5 THEN RUN create-foreign-arrived-today.
    ELSE IF sorttype EQ 6 THEN RUN create-foreign-departed-today.
END.

/*FDL June 27, 2024 => Ticket 7B9FEC*/
CREATE summary-list.
summary-list.summ-str = "SUMMARY".
FOR EACH t-foreign-list NO-LOCK BY t-foreign-list.nation1:
    IF t-foreign-list.nation1 EQ ? OR t-foreign-list.nation1 EQ "" THEN t-foreign-list.nation1 = "?".

    FIND FIRST summary-list WHERE summary-list.nation EQ t-foreign-list.nation1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE summary-list THEN
    DO:
        CREATE summary-list.
        summary-list.nation = t-foreign-list.nation1.
        /*bernatd 2024 BD82C9*/
        FIND FIRST nation WHERE nation.kurzbez EQ summary-list.nation NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN 
        DO:
            summary-list.nation-remark = nation.bezeich.
        END.

        IF summary-list.nation EQ "N/A" OR summary-list.nation EQ "?" THEN summary-list.nation-remark = "UNKNOWN".
    END.



    IF t-foreign-list.guest-stat EQ 1 THEN
    DO:
        summary-list.anz-inhouse = summary-list.anz-inhouse + t-foreign-list.rm-qty.
        summary-list.pax-inhouse = summary-list.pax-inhouse + t-foreign-list.erwachs.

/*         IF t-foreign-list.resstatus EQ 6 THEN                                                                 */
/*             ASSIGN                                                                                            */
/*             summary-list.anz-inhouse = summary-list.anz-inhouse + t-foreign-list.rm-qty                       */
/*             tot-anz-inhouse          = tot-anz-inhouse + 1.                                                   */
/*                                                                                                               */
/*         summary-list.pax-inhouse = summary-list.pax-inhouse + t-foreign-list.erwachs.                         */
/*         tot-pax-inhouse          = tot-pax-inhouse + t-foreign-list.erwachs.                                  */
/*                                                                                                               */
/*         summary-list.anz-inhouse = summary-list.anz-inhouse + t-foreign-list.rm-qty.                          */
/*         tot-anz-inhouse          = tot-anz-inhouse + t-foreign-list.rm-qty.                                   */
/*         summary-list.pax-inhouse = summary-list.pax-inhouse + t-foreign-list.erwachs * t-foreign-list.rm-qty. */
/*         tot-pax-inhouse          = tot-pax-inhouse + t-foreign-list.erwachs * t-foreign-list.rm-qty.          */

        /* count total local vs foreign*/
        IF t-foreign-list.nation1 EQ def-nat THEN tot-local = tot-local + t-foreign-list.erwachs.
        ELSE tot-foreign = tot-foreign + t-foreign-list.erwachs.
    END.
    ELSE IF t-foreign-list.guest-stat EQ 2 THEN
    DO:
        IF t-foreign-list.resstatus EQ 6 THEN
            ASSIGN 
            summary-list.anz-depart = summary-list.anz-depart + t-foreign-list.rm-qty 
            tot-anz-depart          = tot-anz-depart + 1.

        summary-list.pax-depart = summary-list.pax-depart + t-foreign-list.erwachs.
        tot-pax-depart          = tot-pax-depart + t-foreign-list.erwachs.

        IF t-foreign-list.resstatus EQ 6 THEN
            ASSIGN 
            summary-list.anz-inhouse = summary-list.anz-inhouse + t-foreign-list.rm-qty 
            tot-anz-inhouse          = tot-anz-inhouse + 1.

        summary-list.pax-inhouse = summary-list.pax-inhouse + t-foreign-list.erwachs.
        tot-pax-inhouse          = tot-pax-inhouse + t-foreign-list.erwachs.

        /* count total local vs foreign*/
        IF t-foreign-list.nation1 EQ def-nat THEN tot-local = tot-local + t-foreign-list.erwachs.
        ELSE tot-foreign = tot-foreign + t-foreign-list.erwachs.
    END.
    ELSE IF t-foreign-list.guest-stat EQ 3 THEN
    DO:
        
        summary-list.pax-arrival = summary-list.pax-arrival + t-foreign-list.erwachs * t-foreign-list.rm-qty.


        IF t-foreign-list.resstatus NE 11 AND t-foreign-list.resstatus NE 13 THEN 
            ASSIGN 
            summary-list.anz-arrival = summary-list.anz-arrival + t-foreign-list.rm-qty
            tot-anz-arrival = tot-anz-arrival + t-foreign-list.rm-qty.

        tot-pax-arrival = tot-pax-arrival + t-foreign-list.erwachs * t-foreign-list.rm-qty.

        /* count total local vs foreign*/
        IF t-foreign-list.nation1 EQ def-nat THEN tot-local = tot-local + t-foreign-list.erwachs * t-foreign-list.rm-qty.
        ELSE tot-foreign = tot-foreign + t-foreign-list.erwachs * t-foreign-list.rm-qty.
    END.
    /* Naufal Afthar - 6403D8 - add departed & arrived today */
    ELSE IF t-foreign-list.guest-stat EQ 5 THEN
    DO:
        summary-list.anz-arrived = summary-list.anz-arrived + t-foreign-list.rm-qty.
        summary-list.pax-arrived = summary-list.pax-arrived + t-foreign-list.erwachs * t-foreign-list.rm-qty.

        summary-list.anz-inhouse = summary-list.anz-inhouse + t-foreign-list.rm-qty.
        tot-anz-inhouse          = tot-anz-inhouse + t-foreign-list.rm-qty.
        summary-list.pax-inhouse = summary-list.pax-inhouse + t-foreign-list.erwachs * t-foreign-list.rm-qty.
        tot-pax-inhouse          = tot-pax-inhouse + t-foreign-list.erwachs * t-foreign-list.rm-qty.


        /* count total local vs foreign*/
        IF t-foreign-list.nation1 EQ def-nat THEN tot-local = tot-local + t-foreign-list.erwachs * t-foreign-list.rm-qty.
        ELSE tot-foreign = tot-foreign + t-foreign-list.erwachs * t-foreign-list.rm-qty.
    END.
    ELSE IF t-foreign-list.guest-stat EQ 6 THEN
    DO:
        IF (t-foreign-list.erwachs + t-foreign-list.gratis) GT 0 THEN
            ASSIGN
            summary-list.anz-departed = summary-list.anz-departed + t-foreign-list.rm-qty
            tot-anz-departed = tot-anz-departed + t-foreign-list.rm-qty.

        summary-list.pax-departed = summary-list.pax-departed + t-foreign-list.erwachs.
        tot-pax-departed = tot-pax-departed + t-foreign-list.erwachs.

        /* count total local vs foreign*/
        IF t-foreign-list.nation1 EQ def-nat THEN tot-local = tot-local + t-foreign-list.erwachs.
        ELSE tot-foreign = tot-foreign + t-foreign-list.erwachs.
    END.
END.

/* Naufal Afthar - DC8DD2 -> cacl total*/
CREATE summary-list.
ASSIGN
    summary-list.nation-remark = "TOTAL"
    summary-list.pax-inhouse   = tot-pax-inhouse
    summary-list.pax-depart    = tot-pax-depart
    summary-list.pax-arrival   = tot-pax-arrival
    summary-list.pax-arrived   = tot-pax-arrived
    summary-list.pax-departed  = tot-pax-departed
    summary-list.anz-inhouse   = tot-anz-inhouse
    summary-list.anz-depart    = tot-anz-depart
    summary-list.anz-arrival   = tot-anz-arrival
    summary-list.anz-arrived   = tot-anz-arrived
    summary-list.anz-departed  = tot-anz-departed
    .

/* count total local vs foreign*/
CREATE summary-list.
ASSIGN
    summary-list.nation-remark = "TOTAL LOCAL"
    summary-list.pax-inhouse = tot-local.
CREATE summary-list.
ASSIGN
    summary-list.nation-remark = "TOTAL FOREIGN"
    summary-list.pax-inhouse = tot-foreign.


/* Naufal Afthar - 6403D8 - add departed & arrived today */
PROCEDURE create-foreign-arrived-today:
    DEFINE VARIABLE curr-date AS DATE.

    DO curr-date = from-date TO to-date:
        curr-status = 5.

        /*IF (curr-date GT ci-date) THEN RUN create-arrival(curr-date).
        ELSE */ IF curr-date LT ci-date THEN RUN create-arrival1(curr-date).
        ELSE IF curr-date EQ ci-date THEN RUN create-actual-arrived(curr-date).
    END.
END.

PROCEDURE create-foreign-departed-today:
    IF NOT all-nat THEN
    DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
            AND res-line.active-flag EQ 2
            AND res-line.abreise GE from-date
            AND res-line.abreise LE to-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember 
            AND guest.nation1 NE def-nat NO-LOCK
            BY guest.nation1 BY res-line.NAME BY res-line.zinr
            BY res-line.abreise:
            curr-status = 6.
            RUN create-foreign-list.
        END.
    END.
    ELSE
    DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8
            AND res-line.active-flag EQ 2
            AND res-line.abreise GE from-date
            AND res-line.abreise LE to-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK
            BY guest.nation1 BY res-line.NAME BY res-line.zinr
            BY res-line.abreise:
            curr-status = 6.
            RUN create-foreign-list.
        END.
    END.
END.

PROCEDURE create-actual-arrived:
    DEFINE INPUT PARAMETER curr-date AS DATE.

    IF NOT all-nat THEN
    DO:
        FOR EACH res-line WHERE (res-line.resstatus EQ 6 OR res-line.resstatus EQ 13)
            AND res-line.active-flag EQ 1
            AND res-line.ankunft EQ curr-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember
            AND guest.nation1 NE def-nat NO-LOCK
            BY guest.nation1 BY res-line.NAME BY res-line.zinr
            BY res-line.ankunft:
            RUN create-foreign-list.

            IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN tot-anz-arrived = tot-anz-arrived + res-line.zimmeranz.

            tot-pax-arrived = tot-pax-arrived + (res-line.erwachs + res-line.gratis) * res-line.zimmeranz.
        END.
    END.
    ELSE
    DO:
        FOR EACH res-line WHERE (res-line.resstatus EQ 6 OR res-line.resstatus EQ 13)
            AND res-line.active-flag EQ 1
            AND res-line.ankunft EQ curr-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK
            BY guest.nation1 BY res-line.NAME BY res-line.zinr
            BY res-line.ankunft:
            RUN create-foreign-list.

            IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN tot-anz-arrived = tot-anz-arrived + res-line.zimmeranz.

            tot-pax-arrived = tot-pax-arrived + (res-line.erwachs + res-line.gratis) * res-line.zimmeranz.
        END.
    END.
END.
/* end Naufal Afthar*/

PROCEDURE create-foreign-departure:
    DEFINE VARIABLE do-it AS LOGICAL.

    IF NOT all-nat THEN
    DO:
        FOR EACH res-line WHERE res-line.active-flag EQ 1
            AND (res-line.resstatus EQ 6 OR res-line.resstatus = 13 OR res-line.resstatus EQ 11)
            AND res-line.abreise EQ to-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember
            AND guest.nation1 NE def-nat NO-LOCK:
            curr-status = 2.
            RUN create-foreign-list.
        END.
    END.
    ELSE 
    DO:
        FOR EACH res-line WHERE res-line.active-flag EQ 1
            AND (res-line.resstatus EQ 6 OR res-line.resstatus = 13 OR res-line.resstatus EQ 11)
            AND res-line.abreise EQ to-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK:
            curr-status = 2.
            RUN create-foreign-list.
        END.
    END.
END.

PROCEDURE create-foreign-arrival:
    DEFINE VARIABLE curr-date AS DATE.

    DO curr-date = from-date TO to-date:
        curr-status = 3.

        IF (curr-date GT ci-date) THEN RUN create-arrival(curr-date).
        /*ELSE IF curr-date LT ci-date THEN RUN create-arrival1(curr-date). */
        ELSE IF curr-date EQ ci-date THEN RUN create-expected(curr-date).
    END.
END.

PROCEDURE create-inhouse:
    DEFINE VARIABLE actflag1 AS INTEGER.
    DEFINE VARIABLE actflag2 AS INTEGER.
    DEFINE BUFFER rm-sharer FOR res-line.

    IF to-date = ci-date THEN 
    DO: 
      actflag1 = 1. 
      actflag2 = 1. 
    END. 
    ELSE 
    DO: 
      actflag1 = 1. 
      actflag2 = 2. 
    END. 

    IF NOT all-nat THEN
    DO:
        FOR EACH res-line WHERE res-line.active-flag GE actflag1
            AND res-line.active-flag LE actflag2
            AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
            AND res-line.resstatus NE 12 AND res-line.ankunft LE to-date
            AND res-line.abreise GE to-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember
            AND guest.nation1 NE def-nat NO-LOCK
            BY guest.nation1 BY res-line.NAME BY res-line.zinr:

/*             FIND FIRST rm-sharer WHERE rm-sharer.zinr EQ res-line.zinr          */
/*                 AND rm-sharer.resnr EQ res-line.resnr                           */
/*                 AND rm-sharer.ankunft EQ res-line.ankunft                       */
/*                 AND rm-sharer.zipreis EQ 0                                      */
/*                 AND (rm-sharer.erwachs + rm-sharer.kind1 + res-line.kind2) LT 1 */
/*                 AND rm-sharer.gratis LT 1 NO-LOCK NO-ERROR.                     */
/*             IF NOT AVAILABLE rm-sharer THEN                                     */
/*             DO:                                                                 */
/*                 curr-status = 1.                                                */
/*                 RUN create-foreign-list.                                        */
/*                                                                                 */
/*                 ASSIGN                                                          */
/*                     t-foreign-list.rm-qty = res-line.zimmeranz                  */
/*                     t-foreign-list.erwachs = res-line.erwachs                   */
/*                     t-foreign-list.kind1 = res-line.kind1 + res-line.kind2      */
/*                     t-foreign-list.gratis = res-line.gratis.                    */
/*             END.                                                                */
            
            curr-status = 1.
            RUN create-foreign-list.

            ASSIGN
                t-foreign-list.rm-qty = res-line.zimmeranz
                t-foreign-list.erwachs = res-line.erwachs + res-line.gratis
                t-foreign-list.kind1 = res-line.kind1 + res-line.kind2
                t-foreign-list.gratis = res-line.gratis.

            /*FIND FIRST zimmer WHERE zimmer.zinr EQ res-line.zinr NO-LOCK NO-ERROR.
            FIND FIRST queasy WHERE queasy.KEY EQ 14 AND queasy.char1 EQ res-line.zinr
                AND queasy.date1 LE ci-date AND queasy.date2 GE ci-date NO-LOCK NO-ERROR.

           IF AVAILABLE zimmer THEN
           DO:
                IF zimmer.sleeping AND res-line.resstatus NE 13 THEN
                DO:
                    IF NOT AVAILABLE queasy THEN 
                        ASSIGN tot-anz-inhouse = tot-anz-inhouse + res-line.zimmeranz
                                tot-pax-inhouse = tot-pax-inhouse + res-line.erwachs + res-line.gratis.
                    ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
                        ASSIGN tot-anz-inhouse = tot-anz-inhouse + res-line.zimmeranz
                                tot-pax-inhouse = tot-pax-inhouse + res-line.erwachs + res-line.gratis.
                END.
                ELSE IF NOT zimmer.sleeping THEN
                DO:
                    IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr
                        AND res-line.zipreis GT 0 THEN 
                        ASSIGN tot-anz-inhouse = tot-anz-inhouse + res-line.zimmeranz
                                tot-pax-inhouse = tot-pax-inhouse + res-line.erwachs + res-line.gratis.
                END.
           END.*/

            ASSIGN tot-pax-inhouse = tot-pax-inhouse + res-line.erwachs + res-line.gratis
                   tot-anz-inhouse = tot-anz-inhouse + res-line.zimmeranz.
        END.
    END.
    ELSE
    DO:
        FOR EACH res-line WHERE res-line.active-flag GE actflag1
            AND res-line.active-flag LE actflag2
            AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
            AND res-line.resstatus NE 12 AND res-line.ankunft LE to-date
            AND res-line.abreise GE to-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK
            BY guest.nation1 BY res-line.NAME BY res-line.zinr:

/*             FIND FIRST rm-sharer WHERE rm-sharer.zinr EQ res-line.zinr          */
/*                 AND rm-sharer.resnr EQ res-line.resnr                           */
/*                 AND rm-sharer.ankunft EQ res-line.ankunft                       */
/*                 AND rm-sharer.zipreis EQ 0                                      */
/*                 AND (rm-sharer.erwachs + rm-sharer.kind1 + res-line.kind2) LT 1 */
/*                 AND rm-sharer.gratis LT 1 NO-LOCK NO-ERROR.                     */
/*             IF NOT AVAILABLE rm-sharer THEN                                     */
/*             DO:                                                                 */
/*                                                                                 */
/*                 curr-status = 1.                                                */
/*                 RUN create-foreign-list.                                        */
/*                 ASSIGN                                                          */
/*                         t-foreign-list.rm-qty = res-line.zimmeranz              */
/*                         t-foreign-list.erwachs = res-line.erwachs               */
/*                         t-foreign-list.kind1 = res-line.kind1 + res-line.kind2  */
/*                         t-foreign-list.gratis = res-line.gratis.                */
/*                                                                                 */
/*             END.                                                                */
            
            curr-status = 1.
            RUN create-foreign-list.
            ASSIGN
                    t-foreign-list.rm-qty = res-line.zimmeranz
                    t-foreign-list.erwachs = res-line.erwachs + res-line.gratis
                    t-foreign-list.kind1 = res-line.kind1 + res-line.kind2
                    t-foreign-list.gratis = res-line.gratis.
            

            /*FIND FIRST zimmer WHERE zimmer.zinr EQ res-line.zinr NO-LOCK NO-ERROR.
            FIND FIRST queasy WHERE queasy.KEY EQ 14 AND queasy.char1 EQ res-line.zinr
                AND queasy.date1 LE ci-date AND queasy.date2 GE ci-date NO-LOCK NO-ERROR.

           IF AVAILABLE zimmer THEN
           DO:
                IF zimmer.sleeping AND res-line.resstatus NE 13 THEN
                DO:
                    IF NOT AVAILABLE queasy THEN 
                        ASSIGN tot-anz-inhouse = tot-anz-inhouse + res-line.zimmeranz
                                tot-pax-inhouse = tot-pax-inhouse + res-line.erwachs + res-line.gratis.
                    ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
                        ASSIGN tot-anz-inhouse = tot-anz-inhouse + res-line.zimmeranz
                                tot-pax-inhouse = tot-pax-inhouse + res-line.erwachs + res-line.gratis.
                END.
                ELSE IF NOT zimmer.sleeping THEN
                DO:
                    IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr
                        AND res-line.zipreis GT 0 THEN 
                        ASSIGN tot-anz-inhouse = tot-anz-inhouse + res-line.zimmeranz
                                tot-pax-inhouse = tot-pax-inhouse + res-line.erwachs + res-line.gratis.
                END.
           END.*/

            ASSIGN tot-pax-inhouse = tot-pax-inhouse + res-line.erwachs + res-line.gratis
                   tot-anz-inhouse = tot-anz-inhouse + res-line.zimmeranz.
        END.
    END.
END.

PROCEDURE create-inhouse2:
    DEFINE BUFFER rm-sharer FOR res-line.

    IF NOT all-nat THEN
    DO:
        FOR EACH genstat WHERE genstat.datum EQ to-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ genstat.gastnrmember
            AND guest.nation1 NE def-nat NO-LOCK
            BY guest.nation1 BY genstat.zinr:
    
            IF genstat.res-date[1] LT to-date AND genstat.res-date[2] EQ to-date
                AND genstat.resstatus EQ 8 THEN.
            ELSE
            DO:
                FIND FIRST res-line WHERE res-line.resnr EQ genstat.resnr
                    AND res-line.reslinnr EQ genstat.res-int[1] NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    curr-status = 1.
                    RUN create-foreign-list.
                    
                    ASSIGN 
                        t-foreign-list.rm-qty = 1
                        t-foreign-list.erwachs = genstat.erwachs + genstat.gratis
                        t-foreign-list.kind1 = genstat.kind1 + genstat.kind2 + genstat.kind3
                        t-foreign-list.gratis = genstat.gratis.

                    IF res-line.resstatus EQ 13 OR res-line.zimmerfix THEN t-foreign-list.rm-qty = 0.
                END.
            END.

            FIND FIRST zimmer WHERE zimmer.zinr EQ genstat.zinr NO-LOCK NO-ERROR.
            FIND FIRST queasy WHERE queasy.KEY EQ 14 AND queasy.char1 EQ genstat.zinr
                AND queasy.date1 LE ci-date AND queasy.date2 GE ci-date NO-LOCK NO-ERROR.
            
            IF AVAILABLE zimmer THEN
            DO:
                IF zimmer.sleeping AND genstat.resstatus NE 13 THEN
                DO:
                    IF NOT AVAILABLE queasy THEN 
                        ASSIGN tot-anz-inhouse = tot-anz-inhouse + 1.
/*                                 tot-pax-inhouse = tot-pax-inhouse + genstat.erwachs + genstat.gratis.  */
                    ELSE IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr THEN
                        ASSIGN tot-anz-inhouse = tot-anz-inhouse + 1.
/*                                 tot-pax-inhouse = tot-pax-inhouse + genstat.erwachs + genstat.gratis.  */
                END.
                ELSE IF NOT zimmer.sleeping THEN
                DO:
                    IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr AND genstat.zipreis GT 0 THEN 
                        ASSIGN tot-anz-inhouse = tot-anz-inhouse + 1.
/*                                 tot-pax-inhouse = tot-pax-inhouse + genstat.erwachs + genstat.gratis.  */
                END.
            END.

            ASSIGN tot-pax-inhouse = tot-pax-inhouse + genstat.erwachs + genstat.gratis.
        END.
    END.
    ELSE
    DO:
        FOR EACH genstat WHERE genstat.datum EQ to-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ genstat.gastnrmember NO-LOCK
            BY guest.nation1 BY genstat.zinr:
    
            IF genstat.res-date[1] LT to-date AND genstat.res-date[2] EQ to-date
                AND genstat.resstatus EQ 8 THEN.
            ELSE
            DO:
                FIND FIRST res-line WHERE res-line.resnr EQ genstat.resnr
                    AND res-line.reslinnr EQ genstat.res-int[1] NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    curr-status = 1.
                    RUN create-foreign-list.

                    ASSIGN 
                        t-foreign-list.rm-qty = 1
                        t-foreign-list.erwachs = genstat.erwachs + genstat.gratis
                        t-foreign-list.kind1 = genstat.kind1 + genstat.kind2 + genstat.kind3
                        t-foreign-list.gratis = genstat.gratis.

                    IF res-line.resstatus EQ 13 OR res-line.zimmerfix THEN t-foreign-list.rm-qty = 0.
                END.
            END.

            FIND FIRST zimmer WHERE zimmer.zinr EQ genstat.zinr NO-LOCK NO-ERROR.
            FIND FIRST queasy WHERE queasy.KEY EQ 14 AND queasy.char1 EQ genstat.zinr
                AND queasy.date1 LE ci-date AND queasy.date2 GE ci-date NO-LOCK NO-ERROR.
            
            IF AVAILABLE zimmer THEN
            DO:
                IF zimmer.sleeping AND genstat.resstatus NE 13 THEN
                DO:
                    IF NOT AVAILABLE queasy THEN 
                        ASSIGN tot-anz-inhouse = tot-anz-inhouse + 1.
/*                                 tot-pax-inhouse = tot-pax-inhouse + genstat.erwachs + genstat.gratis.  */
                    ELSE IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr THEN
                        ASSIGN tot-anz-inhouse = tot-anz-inhouse + 1.
/*                                 tot-pax-inhouse = tot-pax-inhouse + genstat.erwachs + genstat.gratis.  */
                END.
                ELSE IF NOT zimmer.sleeping THEN
                DO:
                    IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr AND genstat.zipreis GT 0 THEN 
                        ASSIGN tot-anz-inhouse = tot-anz-inhouse + 1.
/*                                 tot-pax-inhouse = tot-pax-inhouse + genstat.erwachs + genstat.gratis.  */
                END.
            END.

            ASSIGN tot-pax-inhouse = tot-pax-inhouse + genstat.erwachs + genstat.gratis.
        END.
    END.
END.

PROCEDURE create-arrival :
    DEFINE INPUT PARAMETER curr-date AS DATE.
    DEFINE BUFFER rm-sharer FOR res-line.

    IF NOT all-nat THEN
    DO:
        FOR EACH res-line WHERE res-line.active-flag LE 1
            AND res-line.resstatus NE 12 AND res-line.resstatus NE 3
            AND res-line.ankunft EQ curr-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember 
            AND guest.nation1 NE def-nat NO-LOCK
            BY guest.nation1 BY res-line.NAME BY res-line.zinr:
            FIND FIRST rm-sharer WHERE rm-sharer.zinr EQ res-line.zinr
                AND rm-sharer.resnr EQ res-line.resnr
                AND rm-sharer.ankunft EQ res-line.ankunft
                AND rm-sharer.zipreis EQ 0
                AND rm-sharer.erwachs EQ 0
                AND (rm-sharer.resstatus EQ 11 OR rm-sharer.resstatus EQ 13) 
                AND rm-sharer.gratis LT 1 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE rm-sharer THEN
            DO:
                RUN create-foreign-list.
            END.

            IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN 
            DO:
                IF curr-status EQ 3 THEN tot-anz-arrival = tot-anz-arrival + res-line.zimmeranz.
                ELSE IF curr-status EQ 5 THEN tot-anz-arrived = tot-anz-arrived + res-line.zimmeranz.

            END.
                
            IF curr-status EQ 3 THEN tot-pax-arrival = tot-pax-arrival + ((res-line.erwachs + res-line.gratis) * res-line.zimmeranz).
            ELSE IF curr-status EQ 5 THEN tot-pax-arrived = tot-pax-arrived + ((res-line.erwachs + res-line.gratis) * res-line.zimmeranz).
        END.
    END.
    ELSE 
    DO:
        FOR EACH res-line WHERE res-line.active-flag LE 1
            AND res-line.resstatus NE 12 AND res-line.resstatus NE 3
            AND res-line.ankunft EQ curr-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK
            BY guest.nation1 BY res-line.NAME BY res-line.zinr:
            FIND FIRST rm-sharer WHERE rm-sharer.zinr EQ res-line.zinr
                AND rm-sharer.resnr EQ res-line.resnr
                AND rm-sharer.ankunft EQ res-line.ankunft
                AND rm-sharer.zipreis EQ 0
                AND rm-sharer.erwachs EQ 0
                AND (rm-sharer.resstatus EQ 11 OR rm-sharer.resstatus EQ 13) 
                AND rm-sharer.gratis LT 1 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE rm-sharer THEN
            DO:
                RUN create-foreign-list.
            END.
            
            IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN 
            DO:
                IF curr-status EQ 3 THEN tot-anz-arrival = tot-anz-arrival + res-line.zimmeranz.
                ELSE IF curr-status EQ 5 THEN tot-anz-arrived = tot-anz-arrived + res-line.zimmeranz.

            END.
                
            IF curr-status EQ 3 THEN tot-pax-arrival = tot-pax-arrival + ((res-line.erwachs + res-line.gratis) * res-line.zimmeranz).
            ELSE IF curr-status EQ 5 THEN tot-pax-arrived = tot-pax-arrived + ((res-line.erwachs + res-line.gratis) * res-line.zimmeranz).
        END.
    END.
END.

PROCEDURE create-arrival1 :
    DEFINE INPUT PARAMETER curr-date AS DATE.
    DEFINE VARIABLE do-it AS LOGICAL.
    DEFINE BUFFER rm-sharer FOR res-line.

    IF NOT all-nat THEN
    DO:
        FOR EACH res-line WHERE (res-line.resstatus EQ 6 OR
            res-line.resstatus EQ 8 OR res-line.resstatus EQ 13)
            AND res-line.ankunft EQ curr-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember
            AND guest.nation1 NE def-nat NO-LOCK
            BY guest.nation1 BY res-line.NAME BY res-line.zinr:
            do-it = YES.
            IF (res-line.ankunft EQ res-line.abreise) AND res-line.resstatus EQ 8 THEN
            DO:
                FIND FIRST history WHERE history.resnr EQ res-line.resnr
                    AND history.reslinnr EQ res-line.reslinnr
                    AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR.
                IF NOT AVAILABLE history THEN do-it = NO.
            END.
            IF do-it THEN
            DO:
                FIND FIRST rm-sharer WHERE rm-sharer.zinr EQ res-line.zinr
                    AND rm-sharer.resnr EQ res-line.resnr 
                    AND rm-sharer.ankunft EQ res-line.ankunft
                    AND rm-sharer.zipreis EQ 0
                    AND rm-sharer.erwachs EQ 0
                    AND (rm-sharer.resstatus EQ 8 OR rm-sharer.resstatus EQ 11 OR rm-sharer.resstatus EQ 13)
                    AND rm-sharer.gratis LT 1 NO-LOCK NO-ERROR.
                IF NOT AVAILABLE rm-sharer THEN
                DO:
                    RUN create-foreign-list.
                END.

                IF curr-status EQ 3 THEN 
                DO: 
                    tot-pax-arrival = tot-pax-arrival + (res-line.erwachs + res-line.gratis) * res-line.zimmeranz.
                    IF res-line.resstatus EQ 6 THEN tot-anz-arrival = tot-anz-arrival + res-line.zimmeranz.
                    ELSE IF res-line.resstatus EQ 8 AND (res-line.erwachs + res-line.gratis) GT 0 THEN tot-anz-arrival = tot-anz-arrival + res-line.zimmeranz.
                END.
                ELSE IF curr-status EQ 5 THEN
                DO: 
                    tot-pax-arrived = tot-pax-arrived + (res-line.erwachs + res-line.gratis) * res-line.zimmeranz.
                    IF res-line.resstatus EQ 6 THEN tot-anz-arrived = tot-anz-arrived + res-line.zimmeranz.
                    ELSE IF res-line.resstatus EQ 8 AND (res-line.erwachs + res-line.gratis) GT 0 THEN tot-anz-arrived = tot-anz-arrived + res-line.zimmeranz.
                END.
            END.
        END.
    END.
    ELSE 
    DO:
        FOR EACH res-line WHERE (res-line.resstatus EQ 6 OR
            res-line.resstatus EQ 8 OR res-line.resstatus EQ 13)
            AND res-line.ankunft EQ curr-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember
            BY guest.nation1 BY res-line.NAME BY res-line.zinr:
            do-it = YES.
            IF (res-line.ankunft EQ res-line.abreise) AND res-line.resstatus EQ 8 THEN
            DO:
                FIND FIRST history WHERE history.resnr EQ res-line.resnr
                    AND history.reslinnr EQ res-line.reslinnr
                    AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR.
                IF NOT AVAILABLE history THEN do-it = NO.
            END.
            IF do-it THEN
            DO:
                FIND FIRST rm-sharer WHERE rm-sharer.zinr EQ res-line.zinr
                    AND rm-sharer.resnr EQ res-line.resnr 
                    AND rm-sharer.ankunft EQ res-line.ankunft
                    AND rm-sharer.zipreis EQ 0
                    AND rm-sharer.erwachs EQ 0
                    AND (rm-sharer.resstatus EQ 8 OR rm-sharer.resstatus EQ 11 OR rm-sharer.resstatus EQ 13)
                    AND rm-sharer.gratis LT 1 NO-LOCK NO-ERROR.
                IF NOT AVAILABLE rm-sharer THEN
                DO:
                    RUN create-foreign-list.
                END.

                IF curr-status EQ 3 THEN 
                DO: 
                    tot-pax-arrival = tot-pax-arrival + (res-line.erwachs + res-line.gratis) * res-line.zimmeranz.
                    IF res-line.resstatus EQ 6 THEN tot-anz-arrival = tot-anz-arrival + res-line.zimmeranz.
                    ELSE IF res-line.resstatus EQ 8 AND (res-line.erwachs + res-line.gratis) GT 0 THEN tot-anz-arrival = tot-anz-arrival + res-line.zimmeranz.
                END.
                ELSE IF curr-status EQ 5 THEN
                DO: 
                    tot-pax-arrived = tot-pax-arrived + (res-line.erwachs + res-line.gratis) * res-line.zimmeranz.
                    IF res-line.resstatus EQ 6 THEN tot-anz-arrived = tot-anz-arrived + res-line.zimmeranz.
                    ELSE IF res-line.resstatus EQ 8 AND (res-line.erwachs + res-line.gratis) GT 0 THEN tot-anz-arrived = tot-anz-arrived + res-line.zimmeranz.
                END.
            END.
        END.
    END.
END.

PROCEDURE create-expected:
    DEFINE INPUT PARAMETER curr-date AS DATE.
    DEFINE BUFFER rm-sharer FOR res-line.

    IF NOT all-nat THEN
    DO:
        FOR EACH res-line WHERE res-line.active-flag EQ 0
            AND res-line.resstatus NE 3
            AND res-line.ankunft EQ curr-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember
            AND guest.nation1 NE def-nat NO-LOCK
            BY guest.nation1 BY res-line.NAME BY res-line.zinr:
            FIND FIRST rm-sharer WHERE rm-sharer.zinr EQ res-line.zinr
                AND rm-sharer.resnr EQ res-line.resnr 
                AND rm-sharer.ankunft EQ res-line.ankunft
                AND rm-sharer.zipreis EQ 0
                AND rm-sharer.erwachs EQ 0
                AND (rm-sharer.resstatus EQ 8 OR rm-sharer.resstatus EQ 11 OR rm-sharer.resstatus EQ 13)
                AND rm-sharer.gratis LT 1 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE rm-sharer THEN
            DO:
                RUN create-foreign-list.
            END.

        END.
    END.
    ELSE
    DO:
        FOR EACH res-line WHERE res-line.active-flag EQ 0
            AND res-line.resstatus NE 3
            AND res-line.ankunft EQ curr-date NO-LOCK,
            FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember
            BY guest.nation1 BY res-line.NAME BY res-line.zinr:
            FIND FIRST rm-sharer WHERE rm-sharer.zinr EQ res-line.zinr
                AND rm-sharer.resnr EQ res-line.resnr 
                AND rm-sharer.ankunft EQ res-line.ankunft
                AND rm-sharer.zipreis EQ 0
                AND rm-sharer.erwachs EQ 0
                AND (rm-sharer.resstatus EQ 8 OR rm-sharer.resstatus EQ 11 OR rm-sharer.resstatus EQ 13)
                AND rm-sharer.gratis LT 1 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE rm-sharer THEN
            DO:
                RUN create-foreign-list.
            END.
        END.
    END.
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
        t-foreign-list.remark        = guest.bemerkung
        t-foreign-list.telefon       = guest.telefon  /* Add by Michael @ 18/09/2018 for Ayola First request - ticket no BFA872 */
        t-foreign-list.guest-stat    = curr-status.

    IF curr-status NE 1 THEN 
        ASSIGN 
        t-foreign-list.rm-qty  = res-line.zimmeranz
        t-foreign-list.erwachs = res-line.erwachs + res-line.gratis
        t-foreign-list.kind1   = res-line.kind1  
        t-foreign-list.gratis  = res-line.gratis.
        


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
