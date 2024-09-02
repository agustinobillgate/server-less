DEFINE TEMP-TABLE rmlist
    FIELD flag      AS INTEGER  FORMAT ">>>" 
    FIELD code      AS CHAR     FORMAT "x(3)"     COLUMN-LABEL "Location"
    FIELD zinr      LIKE zimmer.zinr              COLUMN-LABEL "RmNo"
    FIELD credit    AS INTEGER  FORMAT ">>>"      COLUMN-LABEL "CP"
    FIELD floor     AS INTEGER  FORMAT ">>"       COLUMN-LABEL "FL"
    FIELD gname     AS CHAR     FORMAT "x(32)"    COLUMN-LABEL "Main GuestName" 
    FIELD pic       AS CHAR     FORMAT "x(12)"    COLUMN-LABEL "Person"
    FIELD bemerk    AS CHAR     FORMAT "x(50)"    COLUMN-LABEL "Reservation Comments"
    FIELD rstat     AS CHAR     FORMAT "x(20)"    COLUMN-LABEL "Room Status" 
    FIELD ankunft   AS DATE     FORMAT "99/99/99" COLUMN-LABEL "Arrival" 
    FIELD abreise   AS DATE     FORMAT "99/99/99" COLUMN-LABEL "Departure" 
    FIELD kbezeich  AS CHAR     FORMAT "x(12)"    COLUMN-LABEL "Description" 
    FIELD nation    AS CHAR     FORMAT "x(3)"     COLUMN-LABEL "Nation" 
    FIELD paxnr     AS INTEGER  FORMAT ">>>"      COLUMN-LABEL "No"
    .

DEF INPUT PARAMETER loc-combo AS CHAR    NO-UNDO.
DEF INPUT PARAMETER stat1     AS CHAR    NO-UNDO.
DEF INPUT PARAMETER stat2     AS CHAR    NO-UNDO.
DEF INPUT PARAMETER stat3     AS CHAR    NO-UNDO.
DEF INPUT PARAMETER stat4     AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER credit   AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR rmlist.

DEFINE VARIABLE ci-date   AS DATE NO-UNDO.
DEFINE VARIABLE stat-list AS CHAR EXTENT 4 FORMAT "x(20)" NO-UNDO. 
ASSIGN
    stat-list[1] = stat1
    stat-list[2] = stat2
    stat-list[3] = stat3
    stat-list[4] = stat4
.

RUN htpdate.p(87, OUTPUT ci-date).
RUN create-rmlist.

PROCEDURE create-rmlist:
    DEFINE VARIABLE last-code AS CHARACTER FORMAT "x(3)" INITIAL "1"    NO-UNDO.
    DEFINE VARIABLE do-it     AS LOGICAL                                NO-UNDO.
    
    DEFINE BUFFER room FOR zimmer.
    
    FOR EACH rmlist:
        DELETE rmlist.
    END.
    
    credit = 0.
    
    FOR EACH room WHERE room.zistatus GE 2 AND room.zistatus LE 4 NO-LOCK:
        IF loc-combo = "ALL" THEN do-it = YES.
        ELSE do-it = room.CODE = loc-combo.
        IF do-it THEN
        DO:
            CREATE rmlist.
            ASSIGN 
                rmlist.code     = room.code
                rmlist.zinr     = room.zinr
                rmlist.credit   = room.reihenfolge
                rmlist.floor    = room.etage
                rmlist.rstat    = stat-list[room.zistatus]
                rmlist.kbezeich = room.kbezeich
            .
            IF rmlist.credit = 0 THEN rmlist.credit = 1.
            IF room.zistatus = 3 OR room.zistatus = 4 THEN
            DO:
                FIND FIRST res-line WHERE res-line.active-flag = 1 
                    AND res-line.zinr = room.zinr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    ASSIGN
                      rmlist.bemerk  = res-line.bemerk
                      rmlist.ankunft = res-line.ankunft
                      rmlist.abreise = res-line.abreise
                    .
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
                        NO-LOCK NO-ERROR. 
                    IF AVAILABLE guest THEN
                    ASSIGN
                        rmlist.gname = guest.name + ", " + guest.vorname1 
                                     + " " + guest.anrede1 
                        rmlist.nation = guest.nation1
                    .
                END.
            END.
            IF room.reihenfolge = 0 THEN credit = credit + 1.
            ELSE credit = credit + room.reihenfolge.
        END.   
    END.
    
    FOR EACH res-line WHERE res-line.resstatus = 6
      AND res-line.abreise = ci-date NO-LOCK BY res-line.zinr:
      FIND FIRST room WHERE room.zinr = res-line.zinr NO-LOCK.
      IF loc-combo = "ALL" THEN do-it = YES.
      ELSE do-it = room.CODE = loc-combo.
      IF do-it THEN
      DO:
        FIND FIRST rmlist WHERE rmlist.zinr = res-line.zinr
            NO-ERROR.
        IF NOT AVAILABLE rmlist THEN
        DO:
            CREATE rmlist.
            ASSIGN 
                rmlist.code     = room.code
                rmlist.zinr     = room.zinr
                rmlist.credit   = room.reihenfolge
                rmlist.floor    = room.etage
                rmlist.rstat    = stat-list[3]
                rmlist.kbezeich = room.kbezeich
            .
            IF rmlist.credit = 0 THEN rmlist.credit = 1.
            ASSIGN
                rmlist.bemerk  = res-line.bemerk
                rmlist.ankunft = res-line.ankunft
                rmlist.abreise = res-line.abreise
            .
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
                NO-LOCK NO-ERROR. 
            IF AVAILABLE guest THEN
            ASSIGN
                rmlist.gname = guest.name + ", " + guest.vorname1 
                             + " " + guest.anrede1 
                rmlist.nation = guest.nation1
            .
            IF room.reihenfolge = 0 THEN credit = credit + 1.
            ELSE credit = credit + room.reihenfolge.
        END.
      END.
    END.
END.
