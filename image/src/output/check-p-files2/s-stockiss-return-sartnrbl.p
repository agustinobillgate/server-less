
DEF INPUT PARAMETE fibu AS CHAR.
DEF OUTPUT PARAMETER avail-gl AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER cost-acct LIKE gl-acct.fibukonto INITIAL "00000000000000".

FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibu
  NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct AND (gl-acct.acc-type = 2 OR gl-acct.acc-type = 5) THEN 
DO: 
    cost-acct = gl-acct.fibukonto. 
    avail-gl = YES.
END.
