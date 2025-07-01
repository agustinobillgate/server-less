
RUN chg-sysdates.

PROCEDURE chg-sysdates: 
    DEFINE VARIABLE curr-date AS DATE. 
    DEFINE VARIABLE new-date  AS DATE. 
    DEFINE buffer htp FOR htparam. 
     
    /* 
    /* A/P posting DATE */ 
    FIND FIRST htparam WHERE paramnr = 349 EXCLUSIVE-LOCK. 
    htparam.fdate = htparam.fdate + 1. 
    FIND CURRENT htparam NO-LOCK. 
    */ 
    
    /* stock accounting posting DATE */ 
    FIND FIRST htparam WHERE paramnr = 474 NO-LOCK.
    IF (htparam.fdate + 1) LE TODAY THEN
    DO:
      FIND CURRENT htparam EXCLUSIVE-LOCK. 
      ASSIGN htparam.fdate = htparam.fdate + 1. 
      FIND CURRENT htparam NO-LOCK. 
    END.

    /* accounting posting DATE */ 
    FIND FIRST htparam WHERE paramnr = 372 EXCLUSIVE-LOCK. 
    curr-date = htparam.fdate. 
    new-date = curr-date + 1. 
    FIND FIRST htp WHERE htp.paramnr = 597 no-lock. /* CURRENT Accounting Period */ 
    IF curr-date GT htp.fdate THEN curr-date = htp.fdate. 
    htparam.fdate = new-date. 
    FIND CURRENT htparam NO-LOCK. 
END.
