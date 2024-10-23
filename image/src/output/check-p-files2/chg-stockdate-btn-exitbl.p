  
DEF INPUT PARAMETER billdate AS DATE.  
DEF INPUT PARAMETER init-time   AS INT.  
DEF INPUT PARAMETER init-date   AS DATE.  
DEF OUTPUT PARAMETER err-code AS INT INIT 0.  
  
DEF VAR flag-ok AS LOGICAL.  
DEF VAR a AS INT.  
DEF VAR b AS DATE.  
  
RUN check-timebl.p(3, 474, ?, "htparam", init-time, init-date,  
                   OUTPUT flag-ok, OUTPUT a, OUTPUT b).  
IF NOT flag-ok THEN  
DO:  
    err-code = 2.  
    RETURN NO-APPLY.  
END.  
  
FIND FIRST htparam WHERE paramnr = 474 EXCLUSIVE-LOCK.   
htparam.fdate = billdate.   
htparam.lupdate = today.  
FIND CURRENT htparam.  
  
FIND FIRST gl-jouhdr WHERE gl-jouhdr.jtype = 6 /** receiving **/   
    AND gl-jouhdr.datum GE billdate NO-LOCK NO-ERROR.   
IF AVAILABLE gl-jouhdr THEN err-code = 1.  
  
RUN check-timebl.p(2, 474, ?, "htparam", init-time, init-date,  
                   OUTPUT flag-ok, OUTPUT a, OUTPUT b).  
