/*
*** Program     : notif-availability-webbl.p
*** Description : Program to calculate room availability by type and provide notifications
*** Last Update : 15/04/25
*** Created By  : BLY
*/

DEFINE TEMP-TABLE room-summary
    FIELD room-number       AS INTEGER
    FIELD room-type-name    AS CHARACTER
    FIELD overbook          AS INTEGER FORMAT ">>9"
    FIELD availability      AS INTEGER FORMAT "->>>9"
    FIELD ooo-rooms         AS INTEGER
    FIELD total-rooms       AS INTEGER
    FIELD max-avail         AS INTEGER
    FIELD DATE              AS CHARACTER
    .

DEFINE TEMP-TABLE room-type-list
    FIELD room-number       AS INTEGER
    FIELD room-count        AS INTEGER
    FIELD is-sleeping-room  AS LOGICAL INIT YES
    .

DEFINE TEMP-TABLE room-availability-list
    FIELD avail-flag        AS LOGICAL INIT NO
    FIELD allot-flag        AS LOGICAL INIT NO
    FIELD room-number       AS INTEGER
    FIELD type-index        AS INTEGER
    FIELD is-sleeping-room  AS LOGICAL INIT YES
    FIELD allotment         AS INTEGER EXTENT 30
    FIELD descriptions      AS CHARACTER
    FIELD available-rooms   AS INTEGER EXTENT 30
    FIELD coom              AS CHARACTER EXTENT 30
    FIELD sort-priority     AS INTEGER
    .

DEFINE OUTPUT PARAMETER TABLE FOR room-summary.
DEFINE OUTPUT PARAMETER show-notif AS LOGICAL NO-UNDO INIT NO.

/* Local Variable */
DEFINE VARIABLE start-date          AS DATE         NO-UNDO.
DEFINE VARIABLE end-date            AS DATE         NO-UNDO.
DEFINE VARIABLE i                   AS INTEGER      NO-UNDO.
DEFINE VARIABLE check-date          AS DATE         NO-UNDO.
DEFINE VARIABLE process-room        AS LOGICAL      NO-UNDO.
DEFINE VARIABLE billing-date        AS DATE         NO-UNDO.
DEFINE VARIABLE ooo-count-list      AS INTEGER  EXTENT 30 INITIAL 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0].
DEFINE VARIABLE day-names           AS CHARACTER    NO-UNDO EXTENT 7 INITIAL ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].
DEFINE VARIABLE current-max-avail   AS INTEGER      NO-UNDO INIT -100. /* Ini diperlukan karena untuk membuat validasi jika tidak disetup, 
                                                                            maka harus bernilai false. Karena ada overbook shg tidak 0*/
DEFINE VARIABLE show-all-data       AS LOGICAL      NO-UNDO INIT NO. /* Flag untuk menampilkan semua data availability */
/* DEFINE VARIABLE show-notif          AS LOGICAL      NO-UNDO. /* Local Testing */ */

DEFINE BUFFER avail-config FOR queasy.

/* get billing date */
FIND FIRST htparam WHERE htparam.paramnr EQ 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
    ASSIGN start-date = htparam.fdate.

/* set end date to 1 month */
end-date = ADD-INTERVAL(start-date, 1, "months").

/* First pass: check if any room type has availability < max-avail at any point during the month */
check-date = start-date.
DO WHILE check-date < end-date AND NOT show-all-data:
    FOR EACH room-type-list:
        DELETE room-type-list.
    END.

    FOR EACH room-availability-list:
        DELETE room-availability-list.
    END.

    /* reset OOO count array for new date */
    DO i = 1 TO 30:
        ooo-count-list[i] = 0.
    END.

    /* count total rooms per room-type */
    DEFINE VARIABLE total-room-count        AS INTEGER      NO-UNDO.
    DEFINE VARIABLE current-type-number     AS INTEGER  INITIAL 0.

    total-room-count = 0.
    FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK BY zimmer.zikatnr:
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK.
        IF zimkateg.verfuegbarkeit THEN
        DO:
            total-room-count = total-room-count + 1.

            IF current-type-number NE zimkateg.zikatnr THEN
            DO:
                CREATE room-type-list.

                room-type-list.room-number = zimkateg.zikatnr.
                room-type-list.room-count = 1.
                current-type-number = zimkateg.zikatnr.
            END.
            ELSE room-type-list.room-count = room-type-list.room-count + 1.
        END.
    END.

    /* init room-avail-list with room count per category */
    FOR EACH zimkateg WHERE zimkateg.verfuegbarkeit = YES NO-LOCK BY zimkateg.typ BY zimkateg.zikatnr:
        FIND FIRST room-type-list WHERE room-type-list.room-number = zimkateg.zikatnr AND room-type-list.is-sleeping-room NO-ERROR.
        IF AVAILABLE room-type-list THEN
        DO:
            CREATE room-availability-list.
            i = 1.
            DO WHILE i LE 30:
                room-availability-list.available-rooms[i] = room-type-list.room-count.
                i = i + 1.
            END.
            ASSIGN
                room-availability-list.room-number = zimkateg.zikatnr
                room-availability-list.type-index = zimkateg.typ
                room-availability-list.descriptions = zimkateg.kurzbez + " - " + STRING(zimkateg.overbooking)
                room-availability-list.sort-priority = 0
                .
        END.
    END.

    /* Count OOO */
    FOR EACH outorder WHERE outorder.betriebsnr LE 1 NO-LOCK,
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr
        AND zimmer.sleeping = YES NO-LOCK:

        FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK.
        IF zimkateg.verfuegbarkeit THEN
        DO:
            FIND FIRST room-availability-list WHERE room-availability-list.room-number = zimmer.zikatnr NO-ERROR.
            IF AVAILABLE room-availability-list AND check-date GE outorder.gespstart AND check-date LE outorder.gespende THEN
            DO:
                ooo-count-list[1] = ooo-count-list[1] + 1.
                room-availability-list.available-rooms[1] = room-availability-list.available-rooms[1] - 1.
            END.
        END.
    END.

    /* Count rooms that are already reserved */
    FOR EACH res-line WHERE res-line.active-flag LE 1
        AND res-line.resstatus LE 6 
        AND res-line.resstatus NE 4
        AND ((res-line.ankunft LE check-date AND res-line.abreise GT check-date)
             OR (res-line.ankunft EQ check-date AND res-line.abreise EQ check-date))
        AND res-line.kontignr GE 0
        AND res-line.l-zuordnung[3] = 0 USE-INDEX res-zinr_ix NO-LOCK:

        FIND FIRST room-availability-list WHERE room-availability-list.is-sleeping-room AND room-availability-list.room-number = res-line.zikatnr NO-LOCK NO-ERROR.

        IF AVAILABLE room-availability-list THEN
        DO:
            process-room = YES.
            IF res-line.zinr NE "" THEN
            DO:
                FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK.
                process-room = zimmer.sleeping.
            END.

            IF process-room THEN
                room-availability-list.available-rooms[1] = room-availability-list.available-rooms[1] - res-line.zimmeranz.
        END.
    END.

    /* Count rooms for contracts */
    FOR EACH kontline WHERE kontline.betriebsnr = 1
        AND kontline.ankunft LE check-date AND kontline.abreise GE check-date
        AND kontline.kontstat = 1 USE-INDEX betr-kontnr_ix NO-LOCK:

        FIND FIRST room-availability-list WHERE room-availability-list.is-sleeping-room AND room-availability-list.room-number = kontline.zikatnr NO-LOCK NO-ERROR.

        IF AVAILABLE room-availability-list THEN
            room-availability-list.available-rooms[1] = room-availability-list.available-rooms[1] - kontline.zimmeranz.
    END.

    /* Check for availability condition */
    FOR EACH room-availability-list WHERE room-availability-list.is-sleeping-room:
        /* Reset current-max-avail */
        ASSIGN
            current-max-avail = -100.
        /* get max avail from queasy.key 325 */
        FIND FIRST avail-config WHERE avail-config.KEY EQ 325 
            AND avail-config.number1 = room-availability-list.room-number NO-LOCK NO-ERROR.
        IF AVAILABLE avail-config AND avail-config.number3 > 0 THEN
            ASSIGN current-max-avail = avail-config.number3.

        IF room-availability-list.available-rooms[1] < current-max-avail THEN 
            ASSIGN show-notif = YES.

        CREATE room-summary.
        ASSIGN
            room-summary.room-number    = room-availability-list.room-number
            room-summary.room-type-name = SUBSTRING(room-availability-list.descriptions, 1, INDEX(room-availability-list.descriptions, " - ") - 1)
            room-summary.overbook       = INTEGER(SUBSTRING(room-availability-list.descriptions, INDEX(room-availability-list.descriptions, " - ") + 3))
            room-summary.availability   = room-availability-list.available-rooms[1]
            room-summary.max-avail      = (IF current-max-avail = -100 THEN 0 ELSE current-max-avail)
            room-summary.total-rooms    = total-room-count
            room-summary.ooo-rooms      = ooo-count-list[1]
            room-summary.DATE           = day-names[WEEKDAY(check-date)] + " " + 
                                            STRING(DAY(check-date), "99") + "/" +
                                            STRING(MONTH(check-date), "99") + "/" +
                                            STRING(YEAR(check-date))
            .

        room-summary.ooo-rooms = 0.

        FOR EACH outorder WHERE outorder.betriebsnr LE 1 NO-LOCK,
            FIRST zimmer WHERE zimmer.zinr = outorder.zinr
            AND zimmer.zikatnr = room-summary.room-number
            AND zimmer.sleeping = YES NO-LOCK:

            IF check-date GE outorder.gespstart AND check-date LE outorder.gespende THEN
                room-summary.ooo-rooms = room-summary.ooo-rooms + 1.
        END.
    END.

    check-date = check-date + 1.
END.

/* Display results Testing 
CURRENT-WINDOW:WIDTH = 200.

FOR EACH room-summary:
    DISP room-summary WITH WIDTH 190.
END.

DISP show-notif.
*/





