
DEF INPUT  PARAMETER t-gastnr   AS INT.
DEF INPUT  PARAMETER room       AS CHAR.

DEF OUTPUT PARAMETER gname      AS CHAR.
DEF OUTPUT PARAMETER resnr1     AS INT.
DEF OUTPUT PARAMETER hoga-resnr AS INT.
DEF OUTPUT PARAMETER resline    AS LOGICAL INIT NO.

RELEASE res-line.
FIND FIRST guest WHERE guest.gastnr = t-gastnr NO-LOCK.
gname = guest.NAME + "," + guest.vorname1.

IF room NE "" THEN 
    FIND FIRST res-line WHERE res-line.active-flag = 1 
      AND res-line.zinr = room AND res-line.gastnrmember = guest.gastnr
      NO-LOCK NO-ERROR.
IF NOT AVAILABLE res-line THEN
  ASSIGN 
      resnr1        = guest.gastnr 
      hoga-resnr    = guest.gastnr.
ELSE resline = YES.
