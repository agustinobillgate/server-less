
DEFINE TEMP-TABLE room
    FIELD zinr LIKE zimmer.zinr COLUMN-LABEL "Room"
    FIELD gname AS CHAR FORMAT "x(36)" COLUMN-LABEL "Guest Name".

DEF OUTPUT PARAMETER TABLE FOR room.

DEFINE VARIABLE ci-date AS DATE INITIAL TODAY.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.
IF fdate NE ? THEN ci-date = htparam.fdate.        /* Rulita 211024 | Fixing for serverless */

RUN create-room1.

PROCEDURE create-room1:
    FOR EACH zimmer NO-LOCK:
        CREATE room.
        ASSIGN
            room.zinr = zimmer.zinr.
        FIND FIRST res-line WHERE res-line.zinr = zimmer.zinr AND 
            res-line.active-flag = 1 AND res-line.resstatus NE 12 AND 
            res-line.ankunft LE ci-date AND res-line.abreise GE ci-date
            NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN
        DO:
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember
                USE-INDEX gastnr_index NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN
                room.gname = guest.NAME + " " + guest.vorname1 + ", " + 
                guest.anrede1 + guest.anredefirma.
        END.
    END.
END.
 
