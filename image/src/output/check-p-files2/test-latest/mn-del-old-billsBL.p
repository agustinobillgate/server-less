
DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN del-old-bills.

PROCEDURE del-old-bills: 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
DEFINE VARIABLE anz AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 160 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz = 0 THEN anz = 60. 
  /*MTmess-str = translateExtended ("Deleted closed bills",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FIND FIRST bill WHERE bill.flag = 1 AND bill.datum LT (ci-date - anz) 
    USE-INDEX flagdat_ix NO-LOCK NO-ERROR. 
  DO TRANSACTION WHILE AVAILABLE bill: 
    i = i + 1. 
    /*MTmess-str = translateExtended ("Deleted closed bills",lvCAREA,"") + " " + STRING(i). 
    DISP mess-str WITH FRAME frame1. */
    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr: 
      IF bill.rechnr NE 0 /* AND bill.resnr GT 0 */ THEN RUN create-blinehis. 
      delete bill-line. 
    END. 
    FIND CURRENT bill EXCLUSIVE-LOCK. 
    IF bill.rechnr NE 0 /* AND bill.resnr NE 0 */ THEN RUN create-billhis. 
    delete bill. 
    FIND NEXT bill WHERE bill.flag = 1 AND bill.datum LT (ci-date - anz) 
    USE-INDEX flagdat_ix NO-LOCK NO-ERROR. 
  END. 
  /*MTPAUSE 0. */
END. 


PROCEDURE create-blinehis: 
  DO TRANSACTION: 
    CREATE vhp.blinehis. 
    ASSIGN 
      vhp.blinehis.artnr = bill-line.artnr 
      vhp.blinehis.departement = bill-line.departement 
      vhp.blinehis.bezeich = bill-line.bezeich 
      vhp.blinehis.rechnr = bill-line.rechnr 
      vhp.blinehis.bill-datum = bill-line.bill-datum 
      vhp.blinehis.anzahl = bill-line.anzahl 
      vhp.blinehis.epreis = bill-line.epreis 
      vhp.blinehis.betrag = bill-line.betrag 
      vhp.blinehis.fremdwbetrag = bill-line.fremdwbetrag 
      vhp.blinehis.waehrungsnr = bill-line.waehrungsnr 
      vhp.blinehis.zinr = bill-line.zinr 
      vhp.blinehis.userinit = bill-line.userinit 
      vhp.blinehis.sysdate = bill-line.sysdate 
      vhp.blinehis.zeit = bill-line.zeit. 
    FIND CURRENT vhp.blinehis NO-LOCK.
  END. 
END. 
 
PROCEDURE create-billhis: 
DEF VAR mwst1    AS DECIMAL.
  DO TRANSACTION:
    CREATE vhp.billhis. 
    ASSIGN 
      vhp.billhis.gastnr = bill.gastnr 
      vhp.billhis.name = bill.name 
      vhp.billhis.rechnr = bill.rechnr 
      vhp.billhis.saldo = bill.saldo 
      vhp.billhis.mwst[99] = bill.mwst[99] 
      vhp.billhis.resnr = bill.resnr 
      vhp.billhis.parent-nr = bill.parent-nr 
      vhp.billhis.billnr = bill.billnr 
      vhp.billhis.datum = bill.datum 
      vhp.billhis.zinr = bill.zinr. 
    IF bill.resnr GT 0 THEN vhp.billhis.reslinnr = bill.reslinnr. 
    ELSE vhp.billhis.reslinnr = bill.rechnr. 
    FIND CURRENT vhp.billhis NO-LOCK.
  END. 
END. 
