
DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN del-old-po.


PROCEDURE del-old-po: 
DEFINE VARIABLE anz AS INTEGER. 
DEFINE buffer l-od FOR l-order. 
/*
  FIND FIRST htparam WHERE paramnr = 160 NO-LOCK. 
  anz = htparam.finteger. 
  anz = 60.                      /* changed: 11/17/2001 */ 
*/
  
/* changed on dec 05, 2007 */
  FIND FIRST htparam WHERE paramnr = 237 NO-LOCK. 
  IF htparam.feldtyp = 1 THEN
  DO:
      anz = htparam.finteger.
      IF anz LT 60 THEN anz = 60.
  END.
  ELSE anz = 60.

  /*MTmess-str = translateExtended ("Deleted closed purchase orders",lvCAREA,"") 
      + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
/* l-order.loeschflag 1: = closed, 2: = deleted */ 
  FIND FIRST l-order WHERE l-order.loeschflag GE 1 AND l-order.pos = 0 
  NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE l-order: 
    IF (l-order.lieferdatum-eff + anz) LT ci-date THEN 
    DO: 
      DO TRANSACTION: 
        i = i + 1. 
        /*MTmess-str = translateExtended ("Deleted closed purchase orders",lvCAREA,"") 
            + " " + STRING(i). 
        DISP mess-str WITH FRAME frame1. */
        FOR EACH l-od WHERE l-od.docu-nr = l-order.docu-nr AND l-od.pos GT 0: 
          delete l-od. 
        END. 
        FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = l-order.docu-nr 
        NO-ERROR. 
        IF AVAILABLE l-orderhdr THEN delete l-orderhdr. 
        FIND CURRENT l-order EXCLUSIVE-LOCK. 
        delete l-order. 
      END. 
    END. 
    FIND NEXT l-order WHERE l-order.loeschflag GE 1 AND l-order.pos = 0 
    NO-LOCK NO-ERROR. 
  END. 
  /*MTPAUSE 0. */
END. 

