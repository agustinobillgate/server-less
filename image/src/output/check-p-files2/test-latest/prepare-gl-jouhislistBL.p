DEFINE TEMP-TABLE gl-main-list
    FIELD code    LIKE gl-main.code
    FIELD nr      LIKE gl-main.nr
    FIELD bezeich LIKE gl-main.bezeich.

DEFINE TEMP-TABLE gl-depart-list
    FIELD nr      LIKE gl-depart.nr
    FIELD bezeich LIKE gl-depart.bezeich.

DEF OUTPUT PARAMETER from-date  AS DATE.
DEF OUTPUT PARAMETER close-date AS DATE.
DEF OUTPUT PARAMETER close-year AS DATE.
DEF OUTPUT PARAMETER from-main  AS INTEGER.
DEF OUTPUT PARAMETER main-bez   AS CHAR.
DEF OUTPUT PARAMETER chr977     AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR gl-main-list.
DEF OUTPUT PARAMETER TABLE FOR gl-depart-list.

DEF BUFFER gl-main1 FOR gl-main.
FIND FIRST htparam WHERE paramnr = 110 no-lock.    /* LAST Accounting Period */ 
ASSIGN
  from-date = htparam.fdate
  from-date = DATE(1, 1, YEAR(htparam.fdate) - 3).


FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* journal closing DATE */ 
close-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 795 no-lock.   /* LAST closing year DATE */ 
close-year = htparam.fdate. 
close-year = DATE(MONTH(close-year), day(close-year), YEAR(close-year) + 1). 

FIND FIRST gl-main NO-LOCK. 
IF AVAILABLE gl-main THEN 
DO: 
  from-main = gl-main.code. 
  main-bez = gl-main.bezeich. 
END. 

FOR EACH gl-main:
    CREATE gl-main-list.
    ASSIGN
        gl-main-list.code = gl-main.code
        gl-main-list.nr   = gl-main.nr
        gl-main-list.bezeich   = gl-main.bezeich.
END.

FOR EACH gl-depart:
    CREATE gl-depart-list.
    ASSIGN
        gl-depart-list.nr      = gl-depart.nr
        gl-depart-list.bezeich = gl-depart.bezeich.
END.

FIND FIRST htparam WHERE paramnr = 977 NO-LOCK. 
chr977 = htparam.fchar.
