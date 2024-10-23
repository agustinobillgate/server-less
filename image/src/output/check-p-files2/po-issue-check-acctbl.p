DEFINE INPUT PARAMETER case-type      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER cost-acct      AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER avail-gl-acct AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER fl-code       AS INTEGER NO-UNDO.

IF case-type = 1 THEN
DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = cost-acct NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE gl-acct THEN 
    DO: 
        fl-code = 1.
        RETURN NO-APPLY. 
    END. 
    /*IF AVAILABLE gl-acct AND gl-acct.acc-type NE 2 
          AND gl-acct.acc-type NE 3 AND gl-acct.acc-type NE 5 THEN 
    DO: 
        fl-code = 2.
        RETURN NO-APPLY. 
    END.*/ 

    /*geral 7E68C2*/
    IF AVAILABLE gl-acct THEN
    DO:
       FIND FIRST parameters WHERE progname = "CostCenter" 
           AND section = "Alloc" AND varname GT "" 
           AND parameters.vstring = gl-acct.fibukonto NO-LOCK NO-ERROR. 
       IF NOT AVAILABLE parameters THEN
       DO:
          fl-code = 2.
          RETURN NO-APPLY.    
       END.
    END.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = cost-acct NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE gl-acct THEN RETURN NO-APPLY.
    ELSE avail-gl-acct = YES.
END.

