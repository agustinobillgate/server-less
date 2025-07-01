
DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN del-old-debt.

PROCEDURE del-old-debt: 
DEFINE buffer debt1 FOR debitor. 
DEFINE VARIABLE anz AS INTEGER. 
DEFINE VARIABLE curr-counter AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 163 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz = 0 THEN anz = 90. 
  /*MTmess-str = translateExtended ("Deleted old debt records",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FIND FIRST debitor WHERE debitor.opart = 2 AND debitor.zahlkonto GT 0 
    AND (debitor.rgdatum + anz) LT ci-date NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE debitor: 
    FIND FIRST debt1 WHERE debt1.counter = debitor.counter 
      AND debt1.zahlkonto GT 0 AND RECID(debt1) NE RECID(debitor) 
      AND (debt1.rgdatum + anz) GE ci-date NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE debt1 THEN 
    DO TRANSACTION: 
      i = i + 1. 
      /*MTmess-str = translateExtended ("Deleted old debt records",lvCAREA,"") + " " + STRING(i). 
      DISP mess-str WITH FRAME frame1. */
      curr-counter = debitor.counter. 
      FOR EACH debt1 WHERE debt1.counter = curr-counter EXCLUSIVE-LOCK: 
        RUN create-debthis(RECID(debt1)). 
        delete debt1. 
      END. 
/* 
      FIND CURRENT debitor EXCLUSIVE-LOCK. 
      RUN create-debthis(RECID(debitor)). 
      delete debitor. 
*/ 
    END. 
    FIND NEXT debitor WHERE debitor.opart = 2 AND debitor.zahlkonto GT 0 
      AND (debitor.rgdatum + anz) LT ci-date NO-LOCK NO-ERROR. 
  END. 
  /*MTPAUSE 0. */
END. 



PROCEDURE create-debthis: 
DEFINE INPUT PARAMETER ar-recid AS INTEGER. 
DEFINE buffer debt FOR debitor. 
  DO TRANSACTION:       
    FIND FIRST debt WHERE RECID(debt) = ar-recid NO-LOCK. 
    
        CREATE vhp.debthis. 
        ASSIGN 
          vhp.debthis.artnr = debt.artnr 
          vhp.debthis.rechnr = debt.rechnr 
          vhp.debthis.rgdatum = debt.rgdatum 
          vhp.debthis.counter = debt.counter 
          vhp.debthis.zahlkonto = debt.zahlkonto 
          vhp.debthis.gastnr = debt.gastnr 
          vhp.debthis.gastnrmember = debt.gastnrmember 
          vhp.debthis.name = debt.NAME 
          vhp.debthis.zinr = debt.zinr 
          vhp.debthis.saldo = debt.saldo 
          vhp.debthis.vesrdep = debt.vesrdep 
          vhp.debthis.vesrcod = debt.vesrcod 
          vhp.debthis.verstat = debt.verstat 
          vhp.debthis.bediener-nr = debt.bediener-nr. 
        FIND CURRENT vhp.debthis NO-LOCK. 
    
  END. 
END. 

