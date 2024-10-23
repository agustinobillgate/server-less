DEF TEMP-TABLE t-res-line LIKE res-line.

DEF INPUT PARAMETER inp-resnr    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inp-resline  AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER anz-sharer  AS INTEGER NO-UNDO INIT 0.
DEF OUTPUT PARAMETER gnation     AS CHAR    NO-UNDO INIT "".
DEF OUTPUT PARAMETER ci-date     AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-res-line.

DEFINE BUFFER rline FOR res-line.

FIND FIRST res-line WHERE res-line.resnr = inp-resnr
    AND res-line.reslinnr = inp-resline NO-LOCK NO-ERROR.
IF NOT AVAILABLE res-line THEN RETURN.

CREATE t-res-line.
BUFFER-COPY res-line TO t-res-line.

RUN htpdate.p(87, OUTPUT ci-date).

FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK.
IF guest.karteityp = 0 THEN gnation = guest.nation1.
ELSE gnation = guest.land.

IF res-line.erwachs = 1 THEN RETURN.

anz-sharer = res-line.erwachs - 1.
FOR EACH rline WHERE rline.resnr = inp-resnr
    AND (rline.resstatus = 11 OR rline.resstatus = 13)
    AND rline.active-flag LE 1 NO-LOCK:
    anz-sharer = anz-sharer - 1.
END.

IF res-line.zimmeranz GT 1 THEN
DO:
    gnation = gnation + CHR(2) + STRING(res-line.zimmeranz).
    IF anz-sharer GT 1 THEN anz-sharer = 1.
END.
