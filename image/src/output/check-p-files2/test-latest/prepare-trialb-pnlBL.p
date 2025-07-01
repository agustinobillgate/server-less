
DEFINE TEMP-TABLE gl-depart-list
    FIELD nr        LIKE gl-depart.nr
    FIELD bezeich   LIKE gl-depart.bezeich.

DEF OUTPUT PARAMETER pbal-flag  AS LOGICAL.
DEF OUTPUT PARAMETER to-date    AS DATE.
DEF OUTPUT PARAMETER close-date AS DATE.
DEF OUTPUT PARAMETER pnl-acct   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR gl-depart-list.

DEFINE VARIABLE beg-month AS INTEGER. 
DEFINE VARIABLE end-month AS INTEGER. 
FIND FIRST htparam WHERE paramnr = 993 NO-LOCK. 
end-month = htparam.finteger. 
beg-month = htparam.finteger + 1. 
IF beg-month GT 12 THEN beg-month = 1.

FIND FIRST htparam WHERE paramnr = 460 no-lock.   /* show LAST month YTD */ 
pbal-flag = htparam.flogical. 
 
FIND FIRST htparam WHERE paramnr = 558 no-lock.    /* LAST Accounting Period */ 
to-date = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 597 no-lock.    /* Curr Accounting Period */ 
close-date = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 979 no-lock.  /* PNL AccntNo */ 
/* Rulita 031224 | Fixing serverless issue git 248 */
/* FIND FIRST gl-acct WHERE gl-acct.fibukonto = fchar NO-LOCK NO-ERROR.  */
FIND FIRST gl-acct WHERE gl-acct.fibukonto = htparam.fchar NO-LOCK NO-ERROR. 
/* End Rulita */
IF AVAILABLE gl-acct THEN pnl-acct = htparam.fchar. 

FOR EACH gl-depart:
    CREATE gl-depart-list.
    ASSIGN gl-depart-list.nr = gl-depart.nr
           gl-depart-list.bezeich = gl-depart.bezeich.
END.
