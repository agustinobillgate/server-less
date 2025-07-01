
DEFINE INPUT PARAMETER fdate        AS DATE.
DEFINE INPUT PARAMETER tdate        AS DATE.
DEFINE INPUT PARAMETER datum        AS DATE.
DEFINE INPUT PARAMETER segmentcode  AS INT.
DEFINE INPUT PARAMETER room         AS INT.
DEFINE INPUT PARAMETER person       AS INT.
DEFINE INPUT PARAMETER logis        AS DECIMAL.
DEFINE INPUT PARAMETER delta-rm     AS INT.
DEFINE INPUT PARAMETER delta-pax    AS INT.

IF fdate EQ ? THEN
DO:
    RETURN.
END.
IF tdate EQ ? THEN
DO:
    RETURN.
END.

DO datum = fdate TO tdate:
    FIND FIRST segmentstat WHERE segmentstat.datum = datum AND segmentstat.segmentcode = segmentcode NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE segmentstat THEN 
    DO: 
       CREATE segmentstat. 
       ASSIGN
         segmentstat.datum = datum
         segmentstat.segmentcode = segmentcode
       . 
    END. 
    FIND CURRENT segmentstat EXCLUSIVE-LOCK.
    ASSIGN
      segmentstat.budzimmeranz = room
      segmentstat.budpersanz = person 
      segmentstat.budlogis = logis
    .
    IF delta-rm GT 0 THEN 
    ASSIGN
      segmentstat.budzimmeranz = segmentstat.budzimmeranz + 1
      delta-rm = delta-rm - 1
    .
    IF delta-pax GT 0 THEN 
    ASSIGN
      segmentstat.budpersanz = segmentstat.budpersanz + 1
      delta-pax = delta-pax - 1
    .
    FIND CURRENT segmentstat NO-LOCK.
    RELEASE segmentstat.
END.
