DEFINE TEMP-TABLE genlist LIKE genstat
    FIELD rsv-name      AS CHAR FORMAT "x(25)" COLUMN-LABEL "Rsv Name"
    FIELD nat-str       AS CHAR FORMAT "x(3)" COLUMN-LABEL "NAT"
    FIELD ctry-str      AS CHAR FORMAT "x(3)" COLUMN-LABEL "Country"
    FIELD source-str    AS CHAR FORMAT "x(20)" COLUMN-LABEL "Source"
    FIELD segment-str   AS CHAR FORMAT "x(20)" COLUMN-LABEL "Segment"
    FIELD REC-gen AS INTEGER.

DEF INPUT PARAMETER date1 AS DATE.
DEF INPUT PARAMETER resnr AS INT.
DEF INPUT PARAMETER zinr AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR genlist.

RUN check-genstat.

PROCEDURE check-genstat:
    FOR EACH genlist:
        DELETE genlist.
    END.
    IF resnr NE 0 AND zinr NE "" THEN
    DO:
        FOR EACH genstat WHERE genstat.datum = date1 AND genstat.resnr = resnr 
            AND genstat.zinr = zinr NO-LOCK:
            CREATE genlist.
            BUFFER-COPY genstat TO genlist.
            RUN get-details.
        END.
    END.
    ELSE IF resnr = 0 AND zinr NE "" THEN
        FOR EACH genstat WHERE genstat.datum = date1 
            AND genstat.zinr = zinr NO-LOCK:
            CREATE genlist.
            BUFFER-COPY genstat TO genlist.
            RUN get-details.
        END.
   ELSE
       FOR EACH genstat WHERE genstat.datum = date1 AND genstat.resnr = resnr 
            NO-LOCK:
            CREATE genlist.
            BUFFER-COPY genstat TO genlist.
            RUN get-details.
        END.
END.

PROCEDURE get-details:
    genlist.rec-gen = RECID(genstat).
    FIND FIRST Sourccod WHERE Sourccod.source-code = genstat.SOURCE NO-LOCK
        NO-ERROR.
    IF AVAILABLE Sourccod THEN
        genlist.source-str = Sourccod.bezeich.

    FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK
        NO-ERROR.
    IF AVAILABLE segment THEN
        genlist.segment-str = segment.bezeich.

    FIND FIRST nation WHERE nation.nationnr = genstat.nationnr NO-LOCK NO-ERROR.
    IF AVAILABLE nation THEN
        genlist.nat-str = nation.bezeich.

    FIND FIRST nation WHERE nation.nationnr = genstat.resident NO-LOCK NO-ERROR.
    IF AVAILABLE nation THEN
        genlist.ctry-str = nation.bezeich.

    FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
        genlist.rsv-name = guest.NAME.
END.
