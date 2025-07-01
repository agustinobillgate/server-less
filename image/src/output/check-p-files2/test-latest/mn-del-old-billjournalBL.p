 
DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN del-old-billjournal.


PROCEDURE del-old-billjournal: 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
DEFINE VARIABLE anz AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 161 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz = 0 THEN anz = 60. 
  /*MTmess-str = translateExtended ("Deleted bill journals",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FOR EACH hoteldpt NO-LOCK: 
    FIND FIRST billjournal WHERE billjournal.bill-datum LT (ci-date - anz) 
      AND billjournal.departement = hoteldpt.num 
      AND billjournal.zeit GE 0 AND billjournal.subtime GE 0 
      USE-INDEX depdate_ix NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE billjournal: 
      DO TRANSACTION: 
        i = i + 1. 
        /*MTmess-str = translateExtended ("Deleted bill journals",lvCAREA,"") + " " + STRING(i). 
        DISP mess-str WITH FRAME frame1. */
        FIND CURRENT billjournal EXCLUSIVE-LOCK. 
        delete billjournal. 
      END. 
      FIND NEXT billjournal WHERE billjournal.bill-datum LT (ci-date - anz) 
        AND billjournal.departement = hoteldpt.num 
        AND billjournal.zeit GE 0 AND billjournal.subtime GE 0 
        USE-INDEX depdate_ix NO-LOCK NO-ERROR. 
    END. 
  END. 
  /*MTPAUSE 0. */
END. 
