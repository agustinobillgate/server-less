/***************************************************************************************
**   Business Logic for FCS0 API Interface
**   Descript       : Business Logic program for FCS0 API
**   Created        : BLY
**   Notes          : Menampilkan data interface dengan flag nebenstelle = $FCS0$
***************************************************************************************/

DEFINE TEMP-TABLE tt-data
    FIELD date-if           AS DATE
    FIELD resno             AS INTEGER
    FIELD roomno            AS CHARACTER
    FIELD roomtype          AS CHARACTER
    FIELD roomstatus        AS CHARACTER
    FIELD guestname         AS CHARACTER
    FIELD arrival           AS DATE
    FIELD departure         AS DATE
    FIELD status-send       AS CHARACTER
    FIELD parameters        AS CHARACTER
    FIELD flags             AS CHARACTER
    FIELD irecid            AS INT64
    .

DEFINE VARIABLE v-nebenstelle   AS CHARACTER    NO-UNDO.

/* Staging */
DEFINE INPUT PARAMETER p-type           AS INTEGER. /* 1 = reservation, 2 = housekeeping */
DEFINE INPUT PARAMETER p-status         AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR tt-data.


/* local 
DEFINE VARIABLE p-type      AS INTEGER INIT 1.
DEFINE VARIABLE p-date      AS DATE.
DEFINE VARIABLE p-status    AS CHARACTER INIT "SUCCESS".
*/

CASE p-status:
    WHEN "SUCCESS" THEN
        v-nebenstelle = "*$FCS1$*".
    WHEN "FAILED" THEN
        v-nebenstelle = "*$FCS0$*".
END CASE.

FOR EACH INTERFACE WHERE (INTERFACE.KEY EQ 10 OR INTERFACE.KEY EQ 37) AND
    INTERFACE.nebenstelle MATCHES v-nebenstelle AND
    (INTERFACE.parameters NE "modify" OR
     (INTERFACE.parameters EQ "modify" AND INTERFACE.zinr NE "")) NO-LOCK:

    CREATE tt-data.
    ASSIGN
        tt-data.date-if         = INTERFACE.intdate
        tt-data.roomno          = INTERFACE.zinr
        tt-data.parameters      = INTERFACE.parameters
        tt-data.flags           = INTERFACE.nebenstelle
        tt-data.status-send     = (IF INTERFACE.nebenstelle MATCHES "*$FCS1$*" THEN "SUCCESS" ELSE "FAILED")
        tt-data.irecid          = INTEGER(RECID(INTERFACE))
        .

    /* For Data Reservation */
    IF p-type EQ 1 THEN
    DO:
        ASSIGN
            tt-data.resno = INTERFACE.resnr.

        FIND FIRST res-line WHERE res-line.resnr EQ INTERFACE.resnr AND
            res-line.reslinnr EQ INTERFACE.reslinnr
            NO-LOCK NO-ERROR.

        IF AVAILABLE res-line THEN
        DO:
            FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.

            IF AVAILABLE guest THEN
                ASSIGN
                    tt-data.guestname       = guest.NAME
                    tt-data.arrival         = res-line.ankunft
                    tt-data.departure       = res-line.abreise
                .
        END.
    END.
    /* for Data HouseKeeping */
    IF p-type EQ 2 THEN
    DO:
        FIND FIRST zimmer WHERE zimmer.zinr EQ INTERFACE.zinr
            NO-LOCK NO-ERROR.

        IF AVAILABLE zimmer THEN
        DO:
            ASSIGN
                tt-data.roomtype = zimmer.kbezeich.

            CASE zimmer.zistatus:
                WHEN 0 THEN tt-data.roomstatus = "Vacant Clean Checked".        /* Vacant Clean Checked */
                WHEN 1 THEN tt-data.roomstatus = "Vacant Clean Unchecked".      /* Vacant Clean Unchecked */
                WHEN 2 THEN tt-data.roomstatus = "Vacant Dirty".                /* Vacant Dirty */
                WHEN 3 THEN tt-data.roomstatus = "Expected Departure".          /* Expected Departure */
                WHEN 4 THEN tt-data.roomstatus = "Occupied Dirty".              /* Occupied Dirty */
                WHEN 5 THEN tt-data.roomstatus = "Occupied Cleaned".            /* Occupied Cleaned */
                WHEN 6 THEN tt-data.roomstatus = "Out of Order".                /* Out of Order */
                WHEN 7 THEN tt-data.roomstatus = "Off Market".                  /* Off Market */
                WHEN 8 THEN tt-data.roomstatus = "Do Not Disturb".              /* Do Not Disturb */
                OTHERWISE tt-data.roomstatus = "Unknown".
            END CASE.
        END.
    END.
END.


/* Debug - Display data 
CURRENT-WINDOW:WIDTH = 200.
FOR EACH tt-data WHERE tt-data.irecid EQ 5036841 /*BY tt-data.irecid*/:
    DISPLAY 
        tt-data.date-if FORMAT "99/99/9999" LABEL "Date"
        tt-data.parameters FORMAT "x(15)" LABEL "param"
        tt-data.flags LABEL "flags"
        tt-data.roomno LABEL "Room"
        tt-data.roomtype LABEL "Type"
        tt-data.roomstatus LABEL "Status"
        tt-data.guestname FORMAT "x(30)" LABEL "Guest"
        tt-data.resno LABEL "Res#"
        tt-data.arrival FORMAT "99/99/9999" LABEL "Check-in"
        tt-data.departure FORMAT "99/99/9999" LABEL "Check-out"
        tt-data.status-send
        tt-data.irecid
    WITH WIDTH 190.
END.
*/

