
DEF INPUT PARAMETER cost-acct AS CHAR.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.


FIND FIRST gl-acct WHERE gl-acct.fibukonto = cost-acct NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct THEN 
DO: 
    err-code = 1.
    RETURN NO-APPLY. 
END. 
/*IF AVAILABLE gl-acct AND gl-acct.acc-type NE 2 
    AND gl-acct.acc-type NE 3 AND gl-acct.acc-type NE 5 THEN 
DO: 
    err-code = 2.
    RETURN NO-APPLY. 
END.
*/

/*geral 7E68C2*/
IF AVAILABLE gl-acct THEN
DO:
  FIND FIRST parameters WHERE progname = "CostCenter" 
      AND section = "Alloc" AND varname GT "" 
      AND parameters.vstring = gl-acct.fibukonto NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE parameters THEN
  DO:
     err-code = 2.
     RETURN NO-APPLY.    
  END.
END.
