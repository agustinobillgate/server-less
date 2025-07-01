DEF OUTPUT PARAMETER fb-close-date AS DATE.
DEF OUTPUT PARAMETER mat-close-date AS DATE.
DEF OUTPUT PARAMETER last-journ-transgl AS DATE.
DEF OUTPUT PARAMETER flag-fb  AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER flag-mat AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER partial  AS LOGICAL INIT NO.


DEFINE VARIABLE last-rcv-transgl AS DATE NO-UNDO.
DEFINE VARIABLE last-date        AS DATE NO-UNDO.
DEFINE VARIABLE bill-date        AS DATE NO-UNDO.
DEFINE VARIABLE tmp-date         AS DATE NO-UNDO.
DEFINE VARIABLE tmp-month        AS INTEGER NO-UNDO.


DEF BUFFER ophis-fnb FOR l-ophis.
DEF BUFFER ophis-mat FOR l-ophis.


RUN htpdate.p(224, OUTPUT fb-close-date).
RUN htpdate.p(221, OUTPUT mat-close-date).
/*fb-close-date = DATE(month(fb-close-date), 1, year(fb-close-date)).
mat-close-date = DATE(month(mat-close-date), 1, year(mat-close-date)). */

FIND FIRST htparam WHERE paramnr = 1035 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN last-journ-transgl = htparam.fdate.           /* Rulita 210225 | Fixing if avail serveless issue git 638 */

FIND FIRST htparam WHERE paramnr = 269 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN last-rcv-transgl = htparam.fdate.             /* Rulita 210225 | Fixing if avail serveless issue git 638 */

FIND FIRST htparam WHERE paramnr = 1360 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.bezeich NE "not used" THEN ASSIGN partial = htparam.flogical.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN bill-date = htparam.fdate.

IF MONTH(bill-date) = 12 THEN
DO:
    tmp-date = DATE(1, 1, YEAR(bill-date) + 1).                         /* Rulita 210225 | Fixing tmp date serveless issue git 638 */
    ASSIGN last-date = tmp-date - 1.
END.
ELSE 
DO:
    tmp-month   = MONTH(bill-date) + 1.                                 /* Rulita 210225 | Fixing tmp month serveless issue git 638 */
    tmp-date    = DATE(tmp-month, 1, YEAR(bill-date)).                  /* Rulita 210225 | Fixing tmp date serveless issue git 638 */
    last-date   = tmp-date - 1.
END.

IF last-journ-transgl NE ? AND last-journ-transgl LT last-date THEN
    ASSIGN flag-fb  = NO
           flag-mat = NO.


IF last-rcv-transgl NE ? AND last-rcv-transgl LT last-date THEN
    ASSIGN flag-fb  = NO
           flag-mat = NO.


IF fb-close-date = last-journ-transgl THEN
DO:
   /*
  FIND FIRST ophis-fnb WHERE ophis-fnb.op-art = 1 
    AND MONTH(ophis-fnb.datum) = MONTH(fb-close-date) 
    AND YEAR(ophis-fnb.datum) = YEAR(fb-close-date) NO-LOCK NO-ERROR.
  IF AVAILABLE ophis-fnb THEN flag-fb = NO.
  ELSE IF NOT AVAILABLE ophis-fnb THEN flag-fb = YES.*/
    
    ASSIGN flag-fb = YES.
    FOR EACH ophis-fnb WHERE MONTH(ophis-fnb.datum) = MONTH(fb-close-date) 
        AND YEAR(ophis-fnb.datum) = YEAR(fb-close-date) NO-LOCK :
        FIND FIRST l-artikel WHERE l-artikel.artnr = ophis-fnb.artnr
            AND l-artikel.endkum LE 2 NO-LOCK NO-ERROR.
        IF AVAILABLE l-artikel THEN DO:
            ASSIGN flag-fb = NO.
            LEAVE.
        END.
    END.
END.
ELSE flag-fb = NO.

IF mat-close-date = last-journ-transgl THEN
DO:
  /*
  FIND FIRST ophis-mat WHERE ophis-mat.op-art = 3 
    AND MONTH(ophis-mat.datum) = MONTH(mat-close-date) 
    AND YEAR(ophis-mat.datum) = YEAR(mat-close-date) NO-LOCK NO-ERROR.
  IF AVAILABLE ophis-mat THEN flag-mat = NO.
  ELSE IF NOT AVAILABLE ophis-mat THEN flag-mat = YES.*/

    ASSIGN flag-mat = YES.
    FOR EACH ophis-mat WHERE MONTH(ophis-mat.datum) = MONTH(mat-close-date) 
        AND YEAR(ophis-mat.datum) = YEAR(mat-close-date) NO-LOCK :
        FIND FIRST l-artikel WHERE l-artikel.artnr = ophis-mat.artnr
            AND l-artikel.endkum GT 2 NO-LOCK NO-ERROR.
        IF AVAILABLE l-artikel THEN DO:
            ASSIGN flag-mat = NO.
            LEAVE.
        END.
    END.
END.
ELSE flag-mat = NO.
/*
IF flag-fb AND flag-mat THEN errnr = 3.

IF NOT AVAILABLE ophis-fnb AND NOT AVAILABLE ophis-mat THEN
DO:
    errnr = 3.
    /*ENABLE btn-Closefnb btn-Closemat btn-Closeall WITH FRAME frame1.*/
END.*/
