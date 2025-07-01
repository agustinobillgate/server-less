DEF OUTPUT PARAMETER fb-close-date AS DATE.
DEF OUTPUT PARAMETER mat-close-date AS DATE.
DEF OUTPUT PARAMETER last-journ-transgl AS DATE.
DEF OUTPUT PARAMETER flag-fb  AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER flag-mat AS LOGICAL INIT NO.

DEF BUFFER ophis-fnb FOR l-ophis.
DEF BUFFER ophis-mat FOR l-ophis.



RUN htpdate.p(224, OUTPUT fb-close-date).
RUN htpdate.p(221, OUTPUT mat-close-date).
/*fb-close-date = DATE(month(fb-close-date), 1, year(fb-close-date)).
mat-close-date = DATE(month(mat-close-date), 1, year(mat-close-date)). */

FIND FIRST htparam WHERE paramnr = 1035 NO-LOCK NO-ERROR.
last-journ-transgl = htparam.fdate.

IF fb-close-date = last-journ-transgl THEN
DO:
  FIND FIRST ophis-fnb WHERE ophis-fnb.op-art = 1 
    AND MONTH(ophis-fnb.datum) = MONTH(fb-close-date) 
    AND YEAR(ophis-fnb.datum) = YEAR(fb-close-date) NO-LOCK NO-ERROR.
  IF AVAILABLE ophis-fnb THEN flag-fb = NO.
  ELSE IF NOT AVAILABLE ophis-fnb THEN flag-fb = YES.
END.
ELSE flag-fb = NO.

IF mat-close-date = last-journ-transgl THEN
DO:
  FIND FIRST ophis-mat WHERE ophis-mat.op-art = 3 
    AND MONTH(ophis-mat.datum) = MONTH(mat-close-date) 
    AND YEAR(ophis-mat.datum) = YEAR(mat-close-date) NO-LOCK NO-ERROR.
  IF AVAILABLE ophis-mat THEN flag-mat = NO.
  ELSE IF NOT AVAILABLE ophis-mat THEN flag-mat = YES.
END.
ELSE flag-mat = NO.
/*
IF flag-fb AND flag-mat THEN errnr = 3.

IF NOT AVAILABLE ophis-fnb AND NOT AVAILABLE ophis-mat THEN
DO:
    errnr = 3.
    /*ENABLE btn-Closefnb btn-Closemat btn-Closeall WITH FRAME frame1.*/
END.*/
