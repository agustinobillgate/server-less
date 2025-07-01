
DEF INPUT  PARAMETER cost-acct AS CHAR.
DEF OUTPUT PARAMETER err-flag  AS INT INIT 0.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = cost-acct NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct THEN 
DO: 
    err-flag = 1.
    /*HIDE MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("Account Number incorrect.",lvCAREA,"") VIEW-AS ALERT-BOX INFORMATION. 
    APPLY "entry" TO cost-acct.*/
    RETURN NO-APPLY. 
END. 
IF AVAILABLE gl-acct AND gl-acct.acc-type NE 2 AND gl-acct.acc-type NE 5 THEN 
DO: 
    err-flag = 2.
    /*HIDE MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("Wrong Type of Account Number.",lvCAREA,"") VIEW-AS ALERT-BOX INFORMATION. 
    APPLY "entry" TO cost-acct.*/
    RETURN NO-APPLY. 
END.
