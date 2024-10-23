
DEFINE OUTPUT PARAMETER  curr-date     AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER  curr-month    AS INT  NO-UNDO FORMAT "99".
DEFINE OUTPUT PARAMETER  curr-year     AS INT  NO-UNDO FORMAT "9999".
DEFINE OUTPUT PARAMETER linkgsheet     AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER linkgsheet1    AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER linkgsheet2    AS CHAR NO-UNDO.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.
IF DAY(htparam.fdate) = 1 THEN curr-Date = htparam.fDate. /*MT 06/09/12 */
ELSE
DO:
    FIND FIRST genstat WHERE genstat.datum = htparam.fdate NO-LOCK NO-ERROR.
    IF AVAILABLE genstat THEN curr-Date = htparam.fDate.
    ELSE curr-Date = htparam.fDate - 1.
END.

ASSIGN curr-month    = MONTH(curr-Date)
       curr-year     = YEAR(curr-Date).


/*Gsheet link 3 month occ Occupancy*/
FIND FIRST queasy WHERE queasy.KEY = 193 AND queasy.char1 = "tauziaRpt - occfcast" NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN linkgsheet = queasy.char2.


/*Gsheet link guestRpt*/
FIND FIRST queasy WHERE queasy.KEY = 193 AND queasy.char1 = "tauziaRpt - guestrpt" NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN linkgsheet1 = queasy.char2.

/*Gsheet link revenueRpt*/
FIND FIRST queasy WHERE queasy.KEY = 193 AND queasy.char1 = "tauziaRpt - revenuerpt" NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN linkgsheet2 = queasy.char1.
