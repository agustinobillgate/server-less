DEF TEMP-TABLE t-zimmer LIKE zimmer.
DEF TEMP-TABLE t-outorder LIKE outorder.

DEF INPUT PARAMETER pvILanguage             AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER res-mode                AS CHAR     NO-UNDO.
DEF INPUT PARAMETER prev-zinr               AS CHAR     NO-UNDO.
DEF INPUT PARAMETER curr-zinr               AS CHAR     NO-UNDO.
DEF INPUT PARAMETER prev-zikat              AS CHAR     NO-UNDO.
DEF INPUT PARAMETER curr-zikat              AS CHAR     NO-UNDO.
DEF INPUT PARAMETER reslin-list-zipreis     AS DECIMAL  NO-UNDO.
DEF INPUT PARAMETER inp-resnr               AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER inp-reslinnr            AS INTEGER  NO-UNDO.

DEF OUTPUT PARAMETER curr-setup             AS CHAR     NO-UNDO INIT "".
DEF OUTPUT PARAMETER msg-str                AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER inactive-flag          AS LOGICAL  NO-UNDO INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-zimmer.
DEF OUTPUT PARAMETER TABLE FOR t-outorder.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-resline".

FIND FIRST zimmer WHERE zimmer.zinr = curr-zinr NO-LOCK NO-ERROR.
IF NOT AVAILABLE zimmer THEN
DO:
    msg-str = translateExtended ("No such room number:",lvCAREA,"")
        + " " + STRING(curr-zinr).
    RETURN.
END.

CREATE t-zimmer.
BUFFER-COPY zimmer TO t-zimmer.

IF zimmer.setup GT 0 THEN
DO:
  FIND FIRST paramtext WHERE paramtext.txtnr 
    = (9200 + zimmer.setup) NO-LOCK NO-ERROR.
  IF AVAILABLE paramtext THEN curr-setup = SUBSTR(paramtext.notes,1,1).
END.

IF NOT zimmer.sleeping THEN
DO:
  msg-str = msg-str + CHR(2) + "&W"
          + translateExtended ("The room is inactive!",lvCAREA,"").
  inactive-flag = YES.
END.

IF prev-zikat NE curr-zikat THEN 
DO: 
  IF reslin-list-zipreis NE 0 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("The Room Type was changed,",lvCAREA,"")
            + CHR(10)
            + "update the roomrate if necessary.".
  END. 
END. 

IF res-mode = "qci" THEN RETURN.
IF prev-zinr = "" THEN RETURN.
IF prev-zinr = curr-zinr THEN RETURN.

FIND FIRST res-line WHERE res-line.resnr = inp-resnr
    AND res-line.reslinnr = inp-reslinnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE res-line THEN RETURN.
IF res-line.active-flag GT 0 THEN RETURN.

RUN read-outorderbl.p(1, prev-zinr, inp-resnr,
  ?,?, OUTPUT TABLE t-outorder).
FIND FIRST t-outorder NO-ERROR.
IF AVAILABLE t-outorder THEN
msg-str = msg-str + CHR(2)
  + translateExtended ("The Room Type was changed,",lvCAREA,"").
