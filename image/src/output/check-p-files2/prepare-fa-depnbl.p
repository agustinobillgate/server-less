
DEF OUTPUT PARAMETER last-acctdate AS DATE.
DEF OUTPUT PARAMETER datum AS DATE.
DEF OUTPUT PARAMETER acct-date AS DATE.
DEF OUTPUT PARAMETER close-year AS DATE.
DEF OUTPUT PARAMETER err-no AS INT INIT 0.

FIND FIRST htparam WHERE paramnr = 881 no-lock.    /* LAST Dep'n DATE */ 
last-acctdate = htparam.fdate. 
datum = last-acctdate + 35. 
datum = DATE(month(datum), 1, year(datum)) - 1. 
 
IF datum GT TODAY THEN 
DO: 
  err-no = 1.
  RETURN. 
END. 
 
FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* CURRENT Accounting Period */ 
acct-date = htparam.fdate. 
 
FIND FIRST htparam WHERE paramnr = 795 NO-LOCK. 
close-year = htparam.fdate. 
