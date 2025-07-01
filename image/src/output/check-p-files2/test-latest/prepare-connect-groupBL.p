DEFINE TEMP-TABLE res-list LIKE res-line
    FIELD kurzbez           LIKE zimkateg.kurzbez
    FIELD groupname         LIKE reservation.groupname
    FIELD join-flag         AS LOGICAL LABEL "JoinGroup" 
    FIELD mbill-flag        AS LOGICAL LABEL "Assign Mbill" 
    FIELD prev-join         AS LOGICAL
    FIELD prev-mbill        AS LOGICAL.


DEFINE TEMP-TABLE mainres-list
    FIELD gastnr    LIKE guest.gastnr
    FIELD resnr     LIKE reservation.resnr
    FIELD actflag   LIKE reservation.activeflag
    FIELD zimanz    LIKE res-line.zimmeranz
    FIELD ankunft   LIKE res-line.ankunft
    FIELD abreise   LIKE res-line.abreise
    FIELD segm      LIKE reservation.segmentcode
    FIELD deposit   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD until     AS DATE
    FIELD paid      AS DECIMAL
    FIELD id1       AS CHAR    FORMAT "x(3)"
    FIELD id2       AS CHAR    FORMAT "x(3)"
    FIELD id2-date  AS DATE
    FIELD groupname LIKE reservation.groupname
    FIELD grpflag   LIKE reservation.grpflag
    FIELD bemerk    LIKE reservation.bemerk
    FIELD arrival   AS LOGICAL
    FIELD resident  AS LOGICAL
    FIELD arr-today AS LOGICAL.


DEFINE TEMP-TABLE guest-list
    FIELD gastnr            LIKE guest.gastnr
    FIELD NAME              LIKE guest.NAME
    FIELD anredefirma       LIKE guest.anredefirma
    FIELD wohnort           LIKE guest.wohnort
    FIELD karteityp         LIKE guest.karteityp.


DEFINE TEMP-TABLE t-reservation LIKE reservation.
DEFINE TEMP-TABLE t-res-line LIKE res-line.
DEFINE TEMP-TABLE t-guest LIKE guest.

DEFINE INPUT PARAMETER resno    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER reslinno AS INTEGER NO-UNDO.

DEFINE OUTPUT PARAMETER TABLE FOR res-list.
DEFINE OUTPUT PARAMETER TABLE FOR mainres-list.
DEFINE OUTPUT PARAMETER TABLE FOR guest-list.
DEFINE OUTPUT PARAMETER TABLE FOR t-reservation.
DEFINE OUTPUT PARAMETER TABLE FOR t-guest.


IF resno NE 0 THEN DO:
    RUN connect-groupbl.p (1, resNo, reslinNo, ?, ?, ?, ?, OUTPUT TABLE res-list,
                   OUTPUT TABLE mainres-list, OUTPUT TABLE guest-list).    

    RUN read-reservationbl.p (1, resNo, ?, "", OUTPUT TABLE t-reservation).
    FIND FIRST t-reservation NO-LOCK NO-ERROR.
    IF AVAILABLE t-reservation THEN 
    DO:
        RUN read-res-linebl.p (1, resNo, reslinNo, 0, 0, "", ?, ?,
                        0, 0, "", OUTPUT TABLE t-res-line).
        FIND FIRST t-res-line NO-LOCK NO-ERROR.
        IF AVAILABLE t-res-line THEN
        DO:
            RUN read-guestbl.p (1, t-reservation.gastnr, "", "",
                            OUTPUT TABLE t-guest).            
        END.
    END.
END.
