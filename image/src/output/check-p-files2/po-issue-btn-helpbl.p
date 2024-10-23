
DEF INPUT PARAMETER cost-acct AS CHAR.
DEF OUTPUT PARAMETER cost-center AS CHAR.
DEF OUTPUT PARAMETER jobnr AS INT.
DEF OUTPUT PARAMETER flag AS INT INIT 0.
DEF OUTPUT PARAMETER avail-glacct AS LOGICAL INIT NO.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = cost-acct NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct THEN 
DO: 
  avail-glacct = YES.
  cost-center = gl-acct.bezeich. 
  jobnr = 0. 
  FIND FIRST htparam WHERE paramnr = 933 NO-LOCK. 
  IF gl-acct.main-nr = htparam.finteger AND gl-acct.main-nr NE 0 THEN 
    /*MTRUN select-jobnr.p(OUTPUT jobnr)*/ flag = 1.

  RETURN NO-APPLY. 
END.
