DEFINE TEMP-TABLE genlist LIKE genstat
    FIELD rsv-name      AS CHAR FORMAT "x(25)" COLUMN-LABEL "Rsv Name"
    FIELD nat-str       AS CHAR FORMAT "x(3)" COLUMN-LABEL "NAT"
    FIELD ctry-str      AS CHAR FORMAT "x(3)" COLUMN-LABEL "Country"
    FIELD source-str    AS CHAR FORMAT "x(20)" COLUMN-LABEL "Source"
    FIELD REC-gen       AS INTEGER
    FIELD arr-date      AS DATE
    FIELD depart-date   AS DATE
    FIELD guest-name    AS CHARACTER.

DEFINE INPUT PARAMETER sob       AS CHARACTER.
DEFINE INPUT PARAMETER YTDFlag   AS INTEGER INITIAL 1.
DEFINE INPUT PARAMETER f-date    AS DATE.
DEFINE INPUT PARAMETER t-date    AS DATE.
DEFINE INPUT PARAMETER to-date   AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR genlist.

DEFINE BUFFER g-member FOR guest.

DEFINE VARIABLE from-date        AS DATE NO-UNDO.
DEFINE VARIABLE mm               AS INTEGER. 
DEFINE VARIABLE yy               AS INTEGER. 

IF YTDFlag = 2 THEN
DO:
    from-date = f-date.
    to-date = t-date.
END.
ELSE 
DO:
    /*mm = month(to-date). 
    yy = year(to-date). */
    from-date = f-date.
END.

FOR EACH genlist:
    DELETE genlist.
END.

FIND FIRST sourccod WHERE sourccod.bezeich EQ sob NO-LOCK NO-ERROR.

FOR EACH genstat WHERE genstat.datum GE from-date AND genstat.datum LE to-date
    AND genstat.source EQ sourccod.source-code NO-LOCK:
    CREATE genlist.
    BUFFER-COPY genstat TO genlist.
    ASSIGN 
        genlist.rec-gen     = RECID(genstat)
        genlist.source      = sourccod.source-code
        genlist.source-str  = Sourccod.bezeich
        genlist.arr-date    = genstat.res-date[1]
        genlist.depart-date = genstat.res-date[2]
        .

    FIND FIRST nation WHERE nation.nationnr EQ genstat.nationnr NO-LOCK NO-ERROR.
    IF AVAILABLE nation THEN genlist.nat-str = nation.bezeich.

    FIND FIRST nation WHERE nation.nationnr EQ genstat.resident NO-LOCK NO-ERROR.
    IF AVAILABLE nation THEN genlist.ctry-str = nation.bezeich.

    FIND FIRST guest WHERE guest.gastnr EQ genstat.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN genlist.rsv-name = guest.NAME.

    FIND FIRST g-member WHERE g-member.gastnr EQ genstat.gastnrmember NO-LOCK NO-ERROR.
    IF AVAILABLE g-member THEN genlist.guest-name = g-member.NAME + " " + g-member.vorname1 + ", " + g-member.anrede1.
END.

