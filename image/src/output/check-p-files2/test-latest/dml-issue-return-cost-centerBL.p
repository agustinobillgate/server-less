
DEF INPUT-OUTPUT PARAMETER cost-center AS CHAR.
DEF OUTPUT PARAMETER cost-acct  AS CHAR.
DEF OUTPUT PARAMETER avail-acct AS LOGICAL INIT NO.

FIND FIRST gl-acct WHERE gl-acct.bezeich = cost-center NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-acct THEN
DO:
  avail-acct = YES.
  RETURN NO-APPLY.
END.
ELSE
DO:
  cost-acct = gl-acct.fibukonto.
  cost-center = gl-acct.bezeich.
END. 
