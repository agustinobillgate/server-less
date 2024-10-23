DEF OUTPUT PARAMETER ci-date AS DATE NO-UNDO.
DEF OUTPUT PARAMETER walk-in AS INTEGER NO-UNDO INIT 0.
DEF OUTPUT PARAMETER wi-grp  AS INTEGER NO-UNDO INIT 0.

FIND FIRST htparam WHERE paramnr = 48 NO-LOCK. 
FIND FIRST segment WHERE segment.segmentcode = htparam.finteger 
  NO-LOCK NO-ERROR. 
IF NOT AVAILABLE segment THEN RETURN. 
 
ASSIGN
  walk-in = htparam.finteger
  wi-grp  = segment.segmentgrup
. 
 
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 
