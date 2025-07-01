/*MCH Nov 01, 2024 => Ticket FE94ED - Add Room Number and take out if not available t-list validation*/

DEF TEMP-TABLE t-list
    FIELD gastnr    AS INTEGER
    FIELD mgastnr   AS INTEGER
    FIELD gname     AS CHAR FORMAT "x(32)"
    FIELD resNr     AS INTEGER FORMAT ">>>>>>>9"
    FIELD reslinnr  AS INTEGER
    FIELD fdate     AS DATE INITIAL TODAY
    FIELD tdate     AS DATE INITIAL 01/01/1900
    FIELD ankunft   AS DATE INITIAL ?
    FIELD abreise   AS DATE INITIAL ?
    FIELD zimmeranz AS INTEGER FORMAT ">>9"
    FIELD dlodge    AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD dnite     AS INTEGER FORMAT ">>9"
    FIELD drate     AS DECIMAL FORMAT "->>,>>>,>>9.99"
    FIELD mlodge    AS DECIMAL FORMAT "->>,>>>,>>9.99"
    FIELD mnite     AS INTEGER FORMAT ">>9"
    FIELD mrate     AS DECIMAL FORMAT "->,>>>,>>9.99"
    FIELD ylodge    AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD ynite     AS INTEGER FORMAT ">>9"
    FIELD yrate     AS DECIMAL FORMAT "->,>>>,>>9.99"
    FIELD zinr      AS CHARACTER
    .


DEFINE INPUT PARAMETER gastNo       AS INTEGER.
DEFINE INPUT PARAMETER segmcode     AS INTEGER.
DEFINE INPUT PARAMETER jan-date     AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.

DEF OUTPUT PARAMETER avail-guest AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER f-tittle    AS CHAR    INIT "".
DEF OUTPUT PARAMETER TABLE FOR t-list.

FIND FIRST guest WHERE guest.gastnr = gastNo NO-LOCK NO-ERROR.
IF NOT AVAILABLE guest THEN RETURN.
ELSE avail-guest = YES.
FIND FIRST segment WHERE segment.segmentcode = segmcode NO-LOCK.
f-tittle = ": " + ENTRY(1, segment.bezeich, "$$0") + " - " + guest.NAME.


RUN create-list.


PROCEDURE create-list:
    FOR EACH genstat NO-LOCK WHERE 
        genstat.gastnr = gastNo        AND
        genstat.datum GE jan-date      AND
        genstat.datum LE to-date       AND
        genstat.segmentcode = segmcode AND
        genstat.res-logic[2]           AND
        (genstat.erwachs + genstat.kind1) GT 0:
        FIND FIRST t-list WHERE t-list.resnr = genstat.resnr NO-ERROR.
        FIND FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
        /*IF NOT AVAIL t-list THEN
        DO:*/
            CREATE t-list.
            ASSIGN t-list.resnr    = genstat.resnr
                   t-list.reslinnr = genstat.res-int[1]
                   t-list.mgastnr  = genstat.gastnrmember
                   t-list.gastnr   = genstat.gastnr
                   t-list.zinr     = genstat.zinr
            .
            IF AVAILABLE guest THEN
            t-list.gname    = guest.NAME + ", " + guest.vorname1 + ", " 
                            + guest.anrede1 + guest.anredefirma.
        /*END.*/
        IF t-list.ankunft = ? OR t-list.ankunft GT genstat.res-date[1] THEN
           t-list.ankunft = genstat.res-date[1].
        IF t-list.abreise = ? OR t-list.abreise LT genstat.res-date[2] THEN
           t-list.abreise = genstat.res-date[2].

        IF t-list.fdate GT genstat.datum THEN ASSIGN t-list.fdate = genstat.datum.
        IF t-list.tdate LT genstat.datum THEN ASSIGN t-list.tdate = genstat.datum.

        IF genstat.datum = to-date THEN
        DO:
          ASSIGN t-list.dlodge = t-list.dlodge + genstat.logis.
          /*ITA 071216
          IF genstat.res-int[1] NE 13 THEN t-list.dnite  = t-list.dnite  + 1.*/
          IF genstat.resstatus NE 13 THEN t-list.dnite  = t-list.dnite  + 1.
        END.
        IF MONTH(genstat.datum) = MONTH(to-date) THEN
        DO:
          ASSIGN t-list.mlodge = t-list.mlodge + genstat.logis.
          /*ITA 071216
          IF genstat.res-int[1] NE 13 THEN ASSIGN t-list.mnite  = t-list.mnite  + 1.*/
          IF genstat.resstatus NE 13 THEN ASSIGN t-list.mnite  = t-list.mnite  + 1.
        END.
        DO:
          ASSIGN t-list.ylodge = t-list.ylodge + genstat.logis.
          /*ITA 071216
          IF genstat.res-int[1] NE 13 THEN ASSIGN t-list.ynite  = t-list.ynite  + 1.*/
          IF genstat.resstatus NE 13 THEN ASSIGN t-list.ynite  = t-list.ynite  + 1.
        END.
    END.

    FOR EACH t-list:
      IF t-list.dnite NE 0 THEN ASSIGN t-list.drate = t-list.dlodge / t-list.dnite.
      IF t-list.mnite NE 0 THEN ASSIGN t-list.mrate = t-list.mlodge / t-list.mnite.
      IF t-list.ynite NE 0 THEN ASSIGN t-list.yrate = t-list.ylodge / t-list.ynite.
    END.
END.
