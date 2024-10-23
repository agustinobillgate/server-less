
DEF OUTPUT PARAMETER curr-date  AS DATE.
DEF OUTPUT PARAMETER curr-yr    AS INTEGER.
DEF OUTPUT PARAMETER err-code   AS INT INIT 0.

DEFINE VARIABLE curr-month AS INTEGER. 
DEFINE VARIABLE end-month AS INTEGER. 
FIND FIRST htparam WHERE paramnr = 993 NO-LOCK. 
end-month = htparam.finteger. 

/********** Check IF the closing DATE is correct ********/ 
FIND FIRST htparam WHERE paramnr = 558 no-lock.   /* LAST closing DATE */ 
curr-date = htparam.fdate. 
curr-month = month(htparam.fdate). 
/*MT
IF NOT CONNECTED("vhparch") THEN 
DO: 
    RUN vhparch-connect.p.
END.
*/
IF curr-month NE end-month THEN 
DO: 
    err-code = 1.
    RETURN. 
END. 

FIND FIRST htparam WHERE paramnr = 795 no-lock. /* LAST Closing Year*/ 
IF (YEAR(htparam.fdate) + 1) NE YEAR(curr-date) THEN 
DO:
  err-code = 2.
  RETURN. 
END. 
ASSIGN curr-yr = YEAR(htparam.fdate) + 1. 
 
/**** check IF Beginning year P/L Account was set correctly */ 
FIND FIRST htparam WHERE paramnr = 599 NO-LOCK. 
IF htparam.flogical THEN 
DO: 
DEFINE VARIABLE acct-correct AS LOGICAL INITIAL YES. 
  FIND FIRST htparam WHERE paramnr = 612 NO-LOCK. 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = htparam.fchar 
    NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE gl-acct THEN acct-correct = NO. 
  ELSE 
  DO:    
    IF gl-acct.fibukonto = "" THEN acct-correct = NO. 
    IF gl-acct.acc-type NE 4 THEN acct-correct = NO. 
  END.
  IF NOT acct-correct THEN 
  DO:
    err-code = 3.
    RETURN. 
  END. 
END. 
  
/******** WARNING TO user   ******/ 
err-code = 4.
