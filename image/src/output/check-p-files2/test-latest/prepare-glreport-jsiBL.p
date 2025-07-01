
DEF TEMP-TABLE t-gl-depart
    FIELD nr LIKE gl-depart.nr
    FIELD bezeich LIKE gl-depart.bezeich.

DEF TEMP-TABLE t-gl-department
    FIELD nr LIKE gl-department.nr
    FIELD bezeich LIKE gl-department.bezeich.

DEF INPUT PARAMETER lvCAREA AS CHAR.
DEF OUTPUT PARAMETER end-month AS INT.
DEF OUTPUT PARAMETER beg-month AS INT.
DEF OUTPUT PARAMETER pbal-flag AS LOGICAL.
DEF OUTPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER close-date AS DATE.
DEF OUTPUT PARAMETER close-year AS DATE.
DEF OUTPUT PARAMETER close-month AS INT.
DEF OUTPUT PARAMETER pnl-acct AS CHAR.
DEF OUTPUT PARAMETER c-977 AS CHAR.
DEF OUTPUT PARAMETER pr-opt-str AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-gl-depart.
DEF OUTPUT PARAMETER TABLE FOR t-gl-department.


FIND FIRST queasy WHERE queasy.KEY = 140
    AND queasy.char1 = lvCAREA NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
pr-opt-str = queasy.char3.

FIND FIRST htparam WHERE paramnr = 977 NO-LOCK. 
c-977 = htparam.fchar. 

FIND FIRST htparam WHERE paramnr = 993 NO-LOCK. 
end-month = htparam.finteger. 
beg-month = htparam.finteger + 1. 
IF beg-month GT 12 THEN beg-month = 1. 

FIND FIRST htparam WHERE paramnr = 460 no-lock.   /* show LAST month YTD */ 
pbal-flag = htparam.flogical. 
MESSAGE pbal-flag "test"
    VIEW-AS ALERT-BOX INFO BUTTONS OK.
 
FIND FIRST htparam WHERE paramnr = 558 no-lock.    /* LAST Accounting Period */ 
to-date = htparam.fdate. 
from-date = DATE(month(to-date), 1, year(to-date)). 
close-month = month(to-date). 
 
FIND FIRST htparam WHERE paramnr = 597 no-lock.    /* Curr Accounting Period */ 
close-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 795 no-lock.   /* LAST closing year DATE */ 
close-year = htparam.fdate. 
close-year = DATE(month(close-year), day(close-year), year(close-year) + 1). 
 
FIND FIRST htparam WHERE paramnr = 979 no-lock.  /* PNL AccntNo */ 
FIND FIRST gl-acct WHERE gl-acct.fibukonto = fchar NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct THEN pnl-acct = htparam.fchar. 

FOR EACH gl-depart:
    CREATE t-gl-depart.
    ASSIGN t-gl-depart.nr = gl-depart.nr
           t-gl-depart.bezeich = gl-depart.bezeich.
END.

FOR EACH gl-department:
    CREATE t-gl-department.
    ASSIGN
    t-gl-department.nr = gl-department.nr
    t-gl-department.bezeich = gl-department.bezeich.
END.
