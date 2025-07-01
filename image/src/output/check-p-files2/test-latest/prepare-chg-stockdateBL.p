  
DEF OUTPUT PARAMETER close-date AS DATE.  
DEF OUTPUT PARAMETER billdate AS DATE.  
DEF OUTPUT PARAMETER record-use AS LOGICAL INIT NO.  
DEF OUTPUT PARAMETER init-time  AS INT.  
DEF OUTPUT PARAMETER init-date  AS DATE.  
  
DEF VAR flag-ok AS LOGICAL.  
  
RUN check-timebl.p(1, 474, ?, "htparam", ?, ?, OUTPUT flag-ok,  
                   OUTPUT init-time, OUTPUT init-date).  
IF NOT flag-ok THEN  
DO:  
    record-use = YES.  
    RETURN NO-APPLY.  
END.  
  
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK.   
close-date = htparam.fdate.           /* Rulita 211024 | Fixing for serverless */
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK.   
billdate = htparam.fdate.  
