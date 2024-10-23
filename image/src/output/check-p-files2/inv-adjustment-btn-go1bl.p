
DEF INPUT PARAMETER from-grp AS INT.
DEF INPUT PARAMETER mat-grp AS INT.
DEF INPUT PARAMETER early-adjust AS LOGICAL.
DEF INPUT PARAMETER edit-mode AS LOGICAL.
DEF INPUT PARAMETER inv-postdate AS DATE.

DEF OUTPUT PARAMETER transdate AS DATE.

DEFINE VARIABLE its-ok AS LOGICAL INITIAL YES. 

IF from-grp = mat-grp THEN 
DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 221 NO-LOCK. 
    /* transdate = fdate.  */                   /* Rulita 211024 | Fixing for serverless */
    transdate = htparam.fdate. 
END. 
ELSE 
DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 224 NO-LOCK. 
    /* transdate = fdate.  */                   /* Rulita 211024 | Fixing for serverless */
    transdate = htparam.fdate. 
END. 

IF early-adjust AND inv-postdate LT transdate THEN
transdate = inv-postdate.
