
DEF INPUT  PARAMETER cost-acct AS CHAR.
DEF OUTPUT PARAMETER err-code  AS INT INIT 0.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = cost-acct NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct THEN 
DO: 
  err-code = 1.
  RETURN NO-APPLY. 
END. 
IF AVAILABLE gl-acct AND gl-acct.acc-type EQ 1 THEN
DO:
  err-code = 2.
  RETURN NO-APPLY. 
END.
