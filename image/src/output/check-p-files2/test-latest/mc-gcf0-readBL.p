
DEF INPUT  PARAMETER case-type  AS INTEGER.
DEF INPUT  PARAMETER int1       AS INTEGER.
DEF OUTPUT PARAMETER flag       AS LOGICAL INIT NO.

IF case-type  = 1 THEN
DO :
    FIND FIRST mc-types WHERE mc-types.nr = int1 NO-LOCK NO-ERROR.
    IF AVAILABLE mc-types THEN flag = YES.
END.
ELSE IF case-type = 2 THEN
DO:
  FIND FIRST mc-guest WHERE mc-guest.gastnr = int1 NO-LOCK NO-ERROR.
  FIND FIRST mc-fee WHERE mc-fee.KEY = 1 AND mc-fee.gastnr = mc-guest.gastnr
      AND mc-fee.bis-datum = mc-guest.tdate NO-LOCK NO-ERROR.
  IF AVAILABLE mc-fee AND mc-fee.bezahlt NE 0 THEN flag = YES.
END.
