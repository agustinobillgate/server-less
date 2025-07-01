

DEF OUTPUT PARAMETER from-date  AS DATE.
DEF OUTPUT PARAMETER close-date AS DATE.
DEF OUTPUT PARAMETER close-year AS DATE.
DEF OUTPUT PARAMETER to-date    AS DATE.
DEF OUTPUT PARAMETER curr-yr    AS INTEGER.
DEF OUTPUT PARAMETER from-main  AS INTEGER.
DEF OUTPUT PARAMETER main-bez   AS CHAR.
DEF OUTPUT PARAMETER gst-flag   AS LOGICAL.
DEF OUTPUT PARAMETER cflow-flag AS LOGICAL INIT NO.

DEFINE VARIABLE tmp-date AS DATE NO-UNDO.           /* Rulita 091224 | Fixing serverless issue git 242 */

FIND FIRST htparam WHERE paramnr = 558 NO-LOCK NO-ERROR.     /* LAST Accounting Period */ 
from-date = htparam.fdate + 1. 
FIND FIRST htparam WHERE paramnr = 597 NO-LOCK NO-ERROR.     /* journal closing DATE */ 
close-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 795 NO-LOCK NO-ERROR.     /* LAST closing year DATE */ 
close-year = htparam.fdate. 
/* Rulita 091224 | Fixing serverless issue git 242 */
tmp-date = DATE(MONTH(close-year), day(close-year), YEAR(close-year)). 
close-year = tmp-date  + 1.
/* End Rulita */
to-date = TODAY.
curr-yr = YEAR(htparam.fdate) + 1.


FIND FIRST gl-main NO-LOCK. 
IF AVAILABLE gl-main THEN 
DO: 
  from-main = gl-main.code. 
  main-bez = gl-main.bezeich. 
END. 


/*gst for penang*/
FIND FIRST l-lieferant WHERE l-lieferant.firma = "GST" NO-LOCK NO-ERROR.
IF AVAILABLE l-lieferant THEN ASSIGN gst-flag = YES.
ELSE ASSIGN gst-flag = NO.

/*for penang*/
FIND FIRST queasy WHERE queasy.KEY = 177 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN ASSIGN cflow-flag = YES.

