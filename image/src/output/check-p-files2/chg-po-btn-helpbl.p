
DEF INPUT PARAMETER acct AS CHAR.
DEF OUTPUT PARAMETER cost-acct LIKE gl-acct.fibukonto.
DEF OUTPUT PARAMETER avail-gl-acct AS LOGICAL INIT NO.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = acct NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct THEN 
DO: 
  cost-acct = acct. 
  avail-gl-acct = YES.
END.
