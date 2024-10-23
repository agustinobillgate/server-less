
DEFINE INPUT  PARAMETER number3  AS INT.
DEFINE INPUT  PARAMETER mc-num   AS CHAR.
DEFINE OUTPUT PARAMETER billdate AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER frdate   AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER todate   AS DATE NO-UNDO. 
DEFINE OUTPUT PARAMETER saldo    AS DECIMAL INITIAL 0  NO-UNDO.


RUN check-creditlimit.

PROCEDURE check-creditlimit: 

  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK.
  billdate = vhp.htparam.fdate.
  frdate = DATE(MONTH(billdate), 1, YEAR(billdate)).
  todate = frdate + 31.
  todate = DATE(MONTH(todate), 1, YEAR(todate)) - 1.

  /*FOR EACH vhp.h-journal WHERE vhp.h-journal.bill-datum GE frdate
    AND vhp.h-journal.bill-datum LE todate AND vhp.h-journal.departement GE 1
    AND vhp.h-journal.segmentcode = number3
    AND h-journal.zeit GE 0 USE-INDEX segment_ix NO-LOCK:
      saldo = saldo - vhp.h-journal.betrag.
  END.*/

  FOR EACH queasy WHERE queasy.KEY = 197 AND queasy.char1 = mc-num
      AND queasy.date1 GE frdate AND queasy.date1 LE todate
      AND queasy.number1 = number3 NO-LOCK:
        saldo = saldo + queasy.deci1.
  END.

END. 
