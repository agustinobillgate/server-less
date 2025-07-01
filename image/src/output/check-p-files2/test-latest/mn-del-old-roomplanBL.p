
DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN del-old-roomplan.

PROCEDURE del-old-roomplan: 
DEFINE VARIABLE anz AS INTEGER. 
  /*MTmess-str = translateExtended ("Deleted records",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FIND FIRST resplan WHERE resplan.datum LT ci-date NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE resplan: 
    DO TRANSACTION: 
      i = i + 1. 
      /*MTmess-str = translateExtended ("Deleted records",lvCAREA,"") + " " + STRING(i). 
      DISP mess-str WITH FRAME frame1. */
      FIND CURRENT resplan EXCLUSIVE-LOCK. 
      DELETE resplan. 
      RELEASE resplan.
    END. 
    FIND NEXT resplan WHERE resplan.datum LT ci-date NO-LOCK NO-ERROR. 
  END. 
  FIND FIRST zimplan WHERE zimplan.datum LT ci-date NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE zimplan: 
    DO TRANSACTION: 
      i = i + 1. 
      /*MTmess-str = translateExtended ("Deleted records",lvCAREA,"") + " " + STRING(i). 
      DISP mess-str WITH FRAME frame1.*/
      FIND CURRENT zimplan EXCLUSIVE-LOCK. 
      DELETE zimplan. 
      RELEASE zimplan.
    END. 
    FIND NEXT zimplan WHERE zimplan.datum LT ci-date NO-LOCK NO-ERROR. 
  END. 
  /*MTPAUSE 0. */
END. 

