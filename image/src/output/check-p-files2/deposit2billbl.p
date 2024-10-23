DEF INPUT PARAMETER resno    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER reslinno AS INTEGER NO-UNDO.

DEF VARIABLE bill-date       AS DATE    NO-UNDO.
DEF VARIABLE sys-id          AS CHAR    NO-UNDO.
DEF VARIABLE it-is           AS LOGICAL NO-UNDO.
DEF VARIABLE inv-nr          AS INTEGER NO-UNDO.
DEF VARIABLE deposit         AS DECIMAL NO-UNDO. 
DEF VARIABLE deposit-foreign AS DECIMAL NO-UNDO. 

DEF BUFFER art1              FOR artikel.

RUN htpdate.p (110, OUTPUT bill-date).

FIND FIRST res-line WHERE res-line.resnr = resno
    AND res-line.reslinnr = reslinno NO-LOCK.

FIND FIRST bill WHERE bill.resnr = resno
    AND bill.reslinnr = reslinno.

FIND FIRST reservation WHERE reservation.resnr = resno.
ASSIGN reservation.bestat-dat = bill-date. 
          
RUN calculate-deposit-amount. 
          
FIND FIRST htparam WHERE htparam.paramnr = 104 NO-LOCK. 
sys-id = htparam.fchar. 
 
RUN check-masterbill(OUTPUT it-is). 
IF it-is THEN RUN update-mastbill(OUTPUT inv-nr). 
ELSE 
DO: 
  FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK
    NO-ERROR. 
  IF NOT AVAILABLE counters THEN 
  DO: 
    CREATE counters. 
    ASSIGN 
      counters.counter-no = 3
      counters.counter-bez = "Counter for Bill No" 
    . 
  END. 
  counters.counter = counters.counter + 1. 
      
  ASSIGN
    bill.rechnr = counters.counter
    bill.saldo  = bill.saldo + deposit /* deposit value is negative */ 
    bill.mwst[99] = bill.mwst[99] + deposit-foreign
    bill.rgdruck = 0
  . 
  FIND CURRENT counter NO-LOCK. 
  inv-nr = bill.rechnr. 
END. 
    
FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK. 
FIND FIRST artikel WHERE artikel.artnr = htparam.finteger 
  AND artikel.departement = 0 NO-LOCK. 

FIND FIRST art1 WHERE art1.artnr = reservation.zahlkonto 
AND art1.departement = 0 NO-LOCK NO-ERROR. 
 
CREATE bill-line. 
ASSIGN
  bill-line.rechnr = inv-nr
  bill-line.artnr = artikel.artnr
  bill-line.bezeich = artikel.bezeich 
  bill-line.anzahl = 1
  bill-line.betrag = deposit 
  bill-line.fremdwbetrag = deposit-foreign
  bill-line.zeit = TIME
  bill-line.userinit = sys-id 
  bill-line.zinr = res-line.zinr
  bill-line.massnr = res-line.resnr
  bill-line.billin-nr = res-line.reslinnr 
  bill-line.arrangement = res-line.arrangement 
  bill-line.bill-datum = bill-date
. 
IF AVAILABLE art1 THEN 
   bill-line.bezeich = bill-line.bezeich + " [" + art1.bezeich + "]". 
 
FIND CURRENT bill-line NO-LOCK. 
 
CREATE billjournal. 
ASSIGN
  billjournal.rechnr = inv-nr
  billjournal.artnr = artikel.artnr 
  billjournal.anzahl = 1
  billjournal.fremdwaehrng = deposit-foreign
  billjournal.betrag = deposit
  billjournal.bezeich = artikel.bezeich + " " + STRING(reservation.resnr) 
  billjournal.zinr = res-line.zinr
  billjournal.epreis = 0
  billjournal.zinr = res-line.zinr
  billjournal.zeit = TIME 
  billjournal.userinit = sys-id
  billjournal.bill-datum = bill-date
. 
IF AVAILABLE art1 THEN 
  billjournal.bezeich = billjournal.bezeich + " [" + art1.bezeich + "]". 
 
FIND CURRENT billjournal NO-LOCK. 
 
FIND FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
  AND umsatz.departement = 0 
  AND umsatz.datum = bill-date EXCLUSIVE-LOCK  NO-ERROR. 
          
IF NOT AVAILABLE umsatz THEN 
DO: 
  CREATE umsatz. 
  ASSIGN
    umsatz.artnr = artikel.artnr
    umsatz.datum = bill-date
  . 
END.
ASSIGN
  umsatz.anzahl = umsatz.anzahl + 1 
  umsatz.betrag = umsatz.betrag + deposit
. 
FIND CURRENT umsatz NO-LOCK. 
    
IF AVAILABLE bill THEN FIND CURRENT bill NO-LOCK. 

PROCEDURE check-masterbill: 
DEFINE OUTPUT PARAMETER master-flag AS LOGICAL INITIAL NO. 
  FIND FIRST master WHERE master.resnr = res-line.resnr 
    AND master.active = YES AND master.flag = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE master THEN master-flag = YES. 
END. 
 
PROCEDURE update-mastbill: 
DEFINE OUTPUT PARAMETER inv-nr AS INTEGER. 
DEFINE BUFFER mbill FOR bill. 
 
  FIND FIRST mbill WHERE mbill.resnr = res-line.resnr 
    AND mbill.reslinnr = 0 EXCLUSIVE-LOCK. 
 
  mbill.gesamtumsatz = mbill.gesamtumsatz + deposit. 
  mbill.rgdruck = 0. 
  mbill.datum = bill-date. 
  mbill.saldo = mbill.saldo + deposit. 
  mbill.mwst[99] = mbill.mwst[99] + deposit-foreign. 
  IF mbill.rechnr = 0 THEN 
  DO: 
    FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK
      NO-ERROR. 
    IF NOT AVAILABLE counters THEN 
    DO: 
      CREATE counters. 
      ASSIGN 
        counters.counter-no = 3 
        counters.counter-bez = "Counter for Bill No" 
      . 
    END. 
    counters.counter = counters.counter + 1. 
    mbill.rechnr = counters.counter. 
    FIND CURRENT counter NO-LOCK. 
    FIND CURRENT master EXCLUSIVE-LOCK. 
    master.rechnr = mbill.rechnr. 
    FIND CURRENT master NO-LOCK. 
  END. 
  inv-nr = mbill.rechnr. 
  FIND CURRENT mbill NO-LOCK. 
END. 
 
PROCEDURE calculate-deposit-amount: 
DEFINE VARIABLE deposit-exrate  AS DECIMAL INITIAL 1  NO-UNDO. 
DEFINE VARIABLE exchg-rate      AS DECIMAL INITIAL 1. 
DEFINE VARIABLE price-decimal   AS INTEGER. 
DEFINE VARIABLE double-currency AS LOGICAL INITIAL NO. 
    
  FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK. 
  FIND FIRST artikel WHERE artikel.artnr = htparam.finteger 
    AND artikel.departement = 0 NO-LOCK. 
  
  IF NOT artikel.pricetab THEN
    ASSIGN deposit = - reservation.depositbez - reservation.depositbez2. 
  ELSE
  DO:
    deposit-exrate = 1.
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr
      NO-LOCK NO-ERROR.
    IF reservation.zahldatum = bill-date THEN
    DO:
      IF AVAILABLE waehrung THEN 
        deposit-exrate = waehrung.ankauf / waehrung.einheit.
    END.
    ELSE
    DO:
      FIND FIRST exrate WHERE exrate.artnr = artikel.betriebsnr
        AND exrate.datum = reservation.zahldatum NO-LOCK NO-ERROR.
      IF AVAILABLE exrate THEN deposit-exrate = exrate.betrag.
      ELSE IF AVAILABLE waehrung THEN
        deposit-exrate = waehrung.ankauf / waehrung.einheit.
    END.
    deposit = - reservation.depositbez * deposit-exrate.
    IF reservation.depositbez2 NE 0 THEN
    DO:
      deposit-exrate = 1.
      IF reservation.zahldatum = bill-date THEN
      DO:
        IF AVAILABLE waehrung THEN 
          deposit-exrate = waehrung.ankauf / waehrung.einheit.
      END.
      ELSE
      DO:
        FIND FIRST exrate WHERE exrate.artnr = artikel.betriebsnr
          AND exrate.datum = reservation.zahldatum2 NO-LOCK NO-ERROR.
        IF AVAILABLE exrate THEN deposit-exrate = exrate.betrag.
        ELSE IF AVAILABLE waehrung THEN 
          deposit-exrate = waehrung.ankauf / waehrung.einheit.
      END.
    END.
    deposit = deposit - reservation.depositbez2 * deposit-exrate.
  END.
    
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
  ASSIGN deposit-foreign = ROUND(deposit / exchg-rate, 2). 

END. 
 
