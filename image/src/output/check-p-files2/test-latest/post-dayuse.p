/* 
{supertrans.i} 
DEF VAR lvCAREA AS CHAR INITIAL "post-dayuse". 
*/ 
 
/* Posting Dayuse Arrangement */ 
 
DEFINE INPUT PARAMETER resnr AS INTEGER. 
DEFINE INPUT PARAMETER reslinnr AS INTEGER. 
/* 
DEFINE VARIABLE resnr AS INTEGER INITIAL 1. 
DEFINE VARIABLE reslinnr AS INTEGER INITIAL 1. 
*/ 
DEFINE VARIABLE user-init AS CHAR FORMAT "x(2)". 
DEFINE VARIABLE master-flag AS LOGICAL. 
DEFINE VARIABLE gastnrmember AS INTEGER. 
DEFINE VARIABLE amount AS DECIMAL. 
DEFINE VARIABLE amount-foreign AS DECIMAL INITIAL 0. 
DEFINE VARIABLE description AS CHAR FORMAT "x(24)". 
DEFINE VARIABLE bill-date AS DATE. 
DEFINE VARIABLE price-decimal AS INTEGER. 
 
DEFINE VARIABLE exchg-rate AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ex-rate AS DECIMAL. 
 
DEFINE VARIABLE double-currency AS LOGICAL. 
DEFINE VARIABLE foreign-rate AS LOGICAL. 
 
DEFINE VARIABLE billart AS INTEGER. 
DEFINE VARIABLE qty AS INTEGER INITIAL 1. 
DEFINE VARIABLE curr-room AS CHAR. 
DEFINE VARIABLE cancel-str AS CHAR. 
DEFINE VARIABLE master-str AS CHAR. 
DEFINE VARIABLE master-rechnr AS CHAR. 
DEFINE VARIABLE curr-department AS INTEGER INITIAL 0. 
DEFINE VARIABLE price AS DECIMAL. 
 
DEFINE VARIABLE currZeit    AS INTEGER.
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE n           AS INTEGER INITIAL 1. 
 
FIND FIRST htparam WHERE paramnr = 104 NO-LOCK. 
user-init = htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 
 
FIND FIRST res-line WHERE res-line.resnr = resnr 
   AND res-line.reslinnr = reslinnr NO-LOCK. 
gastnrmember = res-line.gastnrmember. 
price = res-line.zipreis. 
amount = res-line.zipreis. 
curr-room = res-line.zinr. 
 
FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK. 
foreign-rate = htparam.flogical. 
FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = htparam.flogical. 
IF double-currency OR foreign-rate OR res-line.betriebsnr NE 0 THEN 
DO: 
  IF res-line.betriebsnr NE 0 THEN FIND FIRST waehrung WHERE 
    waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
  ELSE 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  END. 
  IF AVAILABLE waehrung THEN 
  DO: 
    exchg-rate = waehrung.ankauf / waehrung.einheit. 
    IF res-line.adrflag AND res-line.betriebsnr = 0 THEN exchg-rate = 1. 
    amount-foreign = res-line.zipreis. 
    amount = round(res-line.zipreis * exchg-rate, price-decimal). 
    IF foreign-rate AND price-decimal = 0 THEN 
    DO: 
      FIND FIRST htparam WHERE paramnr = 145 NO-LOCK. 
      IF htparam.finteger NE 0 THEN 
      DO: 
        n = 1. 
        DO i = 1 TO finteger: 
          n = n * 10. 
        END. 
        amount = ROUND(amount / n, 0) * n. 
      END. 
    END. 
  END. 
END. 
 
FIND FIRST arrangement 
  WHERE arrangement.arrangement = res-line.arrangement NO-LOCK. 
FIND FIRST artikel WHERE artikel.departement = 0 
  AND artikel.artnr = arrangement.argt-artikelnr NO-LOCK. 
billart = artikel.artnr. 
description = arrangement.argt-rgbez. 
 
FIND FIRST bill WHERE bill.resnr = resnr AND bill.reslinnr = reslinnr 
  AND bill.zinr = res-line.zinr AND bill.billnr = 1 AND bill.flag EQ 0 NO-LOCK. 
 
currZeit = TIME.
RUN update-masterbill(currZeit, OUTPUT master-flag). 
/* wrong: argt-line articles incl logding have been posted in update-masterbill
IF master-flag THEN
DO:
  FIND FIRST bill WHERE bill.resnr = resnr AND bill.reslinnr = 0
    EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE bill THEN
  DO:
    RUN tax-service(currZeit). 
    FIND CURRENT bill NO-LOCK.
  END.
END.
ELSE IF NOT master-flag THEN 
*/

IF NOT master-flag THEN
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 110 no-lock.   /* bill DATE */ 
  ASSIGN bill-date = htparam.fdate. 
  
  FIND FIRST bill WHERE bill.resnr = resnr AND bill.reslinnr = reslinnr 
      AND bill.zinr = res-line.zinr AND bill.billnr = 1 AND bill.flag EQ 0 EXCLUSIVE-LOCK. 
  IF artikel.umsatzart = 1 
         THEN bill.logisumsatz = bill.logisumsatz + amount. 
  ELSE IF artikel.umsatzart = 2 
        THEN bill.argtumsatz = bill.argtumsatz + amount. 
  ELSE IF artikel.umsatzart = 3 
        THEN bill.f-b-umsatz = bill.f-b-umsatz + amount. 
  ELSE IF artikel.umsatzart = 4 
        THEN bill.sonst-umsatz = bill.sonst-umsatz + amount. 
  IF artikel.umsatzart GE 1 AND artikel.umsatzart LE 4 THEN 
        bill.gesamtumsatz = bill.gesamtumsatz + amount. 
 
  ASSIGN
    bill.rgdruck  = 0 
    bill.saldo    = bill.saldo + amount
    bill.mwst[99] = bill.mwst[99] + amount-foreign
  .
  IF bill.datum LT bill-date THEN bill.datum = bill-date.
 
  IF bill.rechnr = 0 THEN 
  DO: 
    FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
    counters.counter = counters.counter + 1. 
    bill.rechnr = counters.counter. 
    FIND CURRENT counter NO-LOCK. 
  END. 
  
  CREATE bill-line. 
  ASSIGN
    bill-line.rechnr = bill.rechnr
    bill-line.artnr = artikel.artnr 
    bill-line.bezeich = DESCRIPTION 
    bill-line.anzahl = 1
    bill-line.betrag = amount 
    bill-line.fremdwbetrag = amount-foreign
    bill-line.zinr = res-line.zinr
    bill-line.departement = artikel.departement 
    bill-line.zeit = currZeit
    bill-line.userinit = user-init 
    bill-line.arrangement = res-line.arrangement
    bill-line.bill-datum = bill-date
    bill-line.massnr = res-line.resnr
    bill-line.billin-nr = res-line.reslinnr 
  . 
  IF double-currency THEN bill-line.epreis = amount-foreign.
  ELSE bill-line.epreis = amount. 
  FIND CURRENT bill-line NO-LOCK. 
 
  FIND FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
        AND umsatz.departement = artikel.departement 
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    create umsatz. 
    umsatz.artnr = artikel.artnr. 
    umsatz.datum = bill-date. 
    umsatz.departement = artikel.departement. 
  END. 
  umsatz.betrag = umsatz.betrag + amount. 
  umsatz.anzahl = umsatz.anzahl + 1. 
  FIND CURRENT umsatz NO-LOCK. 
 
  create billjournal. 
  billjournal.rechnr = bill.rechnr. 
  billjournal.artnr = artikel.artnr. 
  billjournal.anzahl = 1. 
  billjournal.betrag = amount. 
  billjournal.fremdwaehrng = amount-foreign. 
  billjournal.bezeich = description. 
  billjournal.zinr = res-line.zinr. 
  billjournal.departement = artikel.departement. 
  IF double-currency THEN billjournal.epreis = amount-foreign. 
  ELSE billjournal.epreis = amount. 
  billjournal.zeit = currZeit. 
  billjournal.stornogrund = "". 
  billjournal.userinit = user-init. 
  billjournal.bill-datum = bill-date. 
  FIND CURRENT billjournal NO-LOCK. 
 
  RUN tax-service(currZeit). 
 
  FIND CURRENT bill NO-LOCK NO-ERROR. 
END. 
 
{ update-master.i } 
 
PROCEDURE tax-service: 
DEFINE INPUT PARAMETER currZeit AS INTEGER.

DEFINE VARIABLE service AS DECIMAL. 
DEFINE VARIABLE vat AS DECIMAL. 
DEFINE VARIABLE service-foreign AS DECIMAL. 
DEFINE VARIABLE vat-foreign AS DECIMAL. 
DEFINE buffer artikel1 FOR artikel. 
DEFINE VARIABLE argt-betrag0 AS DECIMAL. 
DEFINE VARIABLE argt-betrag AS DECIMAL. 
DEFINE VARIABLE rest-betrag AS DECIMAL. 
DEFINE VARIABLE rm-vat  AS LOGICAL. 
DEFINE VARIABLE rm-serv AS LOGICAL. 
DEFINE VARIABLE post-it AS LOGICAL. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK. 
  rm-vat = NOT htparam.flogical. 
  FIND FIRST htparam WHERE htparam.paramnr = 128 NO-LOCK. 
  rm-serv = NOT htparam.flogical. 
 
  rest-betrag = amount. 
  FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
    AND NOT argt-line.kind2 NO-LOCK:  /* kind2 = YES => fix cost e.g extrabed */ 
    post-it = NO. 
    RUN argt-betrag.p(RECID(res-line), RECID(argt-line), OUTPUT argt-betrag0, 
      OUTPUT ex-rate). 
    argt-betrag = round(argt-betrag0 * ex-rate, price-decimal). 
    FIND FIRST artikel1 WHERE artikel1.artnr = argt-line.argt-artnr 
      AND artikel1.departement = argt-line.departement NO-LOCK. 
    IF argt-line.fakt-modus = 1 THEN post-it = YES. 
    ELSE IF argt-line.fakt-modus = 2 OR argt-line.fakt-modus = 3 THEN 
    /* checked-in , once */ 
    DO: 
      FIND FIRST billjournal WHERE billjournal.rechnr = bill.rechnr 
        AND billjournal.artnr = artikel1.artnr 
        AND billjournal.betrag = argt-betrag 
        AND billjournal.departement = artikel1.departement NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE billjournal THEN post-it = YES. 
    END. 
    ELSE IF argt-line.fakt-modus = 4 THEN   /* 1st day OF month  */ 
    DO: 
       IF day(bill-date) = 1 THEN post-it = YES. 
    END. 
    ELSE IF argt-line.fakt-modus = 5 THEN   /* LAST day OF month */ 
    DO: 
       IF day(bill-date + 1) = 1 THEN post-it = YES. 
    END. 
    IF post-it AND argt-betrag NE 0 THEN 
    DO: 
      rest-betrag = rest-betrag - argt-betrag. 
      FIND FIRST artikel1 WHERE artikel1.artnr = argt-line.argt-artnr 
        AND artikel1.departement = argt-line.departement NO-LOCK. 
      FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
        AND umsatz.departement = artikel1.departement 
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE umsatz THEN 
      DO: 
        create umsatz. 
        umsatz.artnr = artikel1.artnr. 
        umsatz.datum = bill-date. 
        umsatz.departement = artikel1.departement. 
      END. 
      umsatz.betrag = umsatz.betrag + argt-betrag. 
      umsatz.anzahl = umsatz.anzahl + qty. 
      FIND CURRENT umsatz NO-LOCK. 
      create billjournal. 
      billjournal.rechnr = bill.rechnr. 
      billjournal.artnr = artikel1.artnr. 
      billjournal.anzahl = qty. 
      billjournal.fremdwaehrng = argt-betrag0. 
      billjournal.betrag = argt-betrag. 
      billjournal.bezeich = artikel1.bezeich. 
      billjournal.zinr = res-line.zinr. 
      billjournal.departement = artikel1.departement. 
      billjournal.epreis = 0. 
      billjournal.zeit = currZeit. 
      billjournal.userinit = user-init. 
      billjournal.bill-datum = bill-date. 
      FIND CURRENT billjournal NO-LOCK. 
    END. 
  END. 
  FIND FIRST artikel1 WHERE artikel1.artnr = arrangement.artnr-logis 
    AND artikel1.departement = artikel.departement NO-LOCK. 
  FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
      AND umsatz.departement = artikel1.departement 
      AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    create umsatz. 
    umsatz.artnr = artikel1.artnr. 
    umsatz.datum = bill-date. 
    umsatz.departement = artikel1.departement. 
  END. 
  umsatz.betrag = umsatz.betrag + rest-betrag. 
  umsatz.anzahl = umsatz.anzahl + 1. 
  FIND CURRENT umsatz NO-LOCK. 
  create billjournal. 
  billjournal.rechnr = bill.rechnr. 
  billjournal.artnr = artikel1.artnr. 
  billjournal.anzahl = 1. 
  billjournal.fremdwaehrng = round(rest-betrag / exchg-rate , 2). 
  billjournal.betrag = rest-betrag. 
  billjournal.bezeich = artikel1.bezeich. 
  billjournal.zinr = res-line.zinr. 
  billjournal.departement = artikel1.departement. 
  billjournal.epreis = 0. 
  billjournal.zeit = currZeit. 
  billjournal.stornogrund = "". 
  billjournal.userinit = user-init. 
  billjournal.bill-datum = bill-date. 
  FIND CURRENT billjournal NO-LOCK. 
 
  IF rm-serv AND artikel.service-code NE 0 THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = artikel.service-code NO-LOCK. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    DO: 
      service = htparam.fdecimal. 
      FIND FIRST htparam WHERE htparam.paramnr = 133 NO-LOCK. 
      FIND FIRST artikel1 WHERE artikel1.artnr = htparam.finteger 
        AND artikel1.departement = artikel.departement NO-LOCK. 
      service = service * amount-foreign / 100. 
      service-foreign = round(service, 2). 
      IF double-currency THEN 
        service = round(service * exchg-rate, price-decimal). 
      ELSE service = round(service, price-decimal). 
 
      create bill-line. 
      ASSIGN
        bill-line.rechnr = bill.rechnr
        bill-line.artnr = artikel1.artnr 
        bill-line.bezeich = artikel1.bezeich 
        bill-line.anzahl = 1 
        bill-line.fremdwbetrag = service-foreign
        bill-line.betrag = service
        bill-line.zinr = res-line.zinr 
        bill-line.departement = artikel1.departement 
        bill-line.epreis = 0
        bill-line.zeit = currZeit + 1
        bill-line.userinit = user-init 
        bill-line.arrangement = res-line.arrangement
        bill-line.bill-datum = bill-date 
        bill-line.massnr = res-line.resnr
        bill-line.billin-nr = res-line.reslinnr 
      .
      FIND CURRENT bill-line NO-LOCK. 
 
      FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
        AND umsatz.departement = artikel1.departement 
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE umsatz THEN 
      DO: 
        create umsatz. 
        umsatz.artnr = artikel1.artnr. 
        umsatz.datum = bill-date. 
        umsatz.departement = artikel1.departement. 
      END. 
      umsatz.betrag = umsatz.betrag + service. 
      umsatz.anzahl = umsatz.anzahl + 1. 
      FIND CURRENT umsatz NO-LOCK. 
 
      create billjournal. 
      billjournal.rechnr = bill.rechnr. 
      billjournal.artnr = artikel1.artnr. 
      billjournal.anzahl = 1. 
      billjournal.fremdwaehrng = service-foreign. 
      billjournal.betrag = service. 
      billjournal.bezeich = artikel1.bezeich. 
      billjournal.zinr = res-line.zinr. 
      billjournal.departement = artikel1.departement. 
      billjournal.epreis = 0. 
      billjournal.zeit = currZeit + 1. 
      billjournal.stornogrund = "". 
      billjournal.userinit = user-init. 
      billjournal.bill-datum = bill-date. 
      FIND CURRENT billjournal NO-LOCK. 
    END. 
  END. 
 
  IF rm-vat AND artikel.mwst-code NE 0 THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code NO-LOCK. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    DO: 
      vat = htparam.fdecimal. 
      FIND FIRST htparam WHERE htparam.paramnr = 132 NO-LOCK. 
      FIND FIRST artikel1 WHERE artikel1.artnr = htparam.finteger 
        AND artikel1.departement = artikel.departement NO-LOCK. 
      FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
      IF htparam.flogical THEN 
        vat = vat * (amount-foreign + service-foreign) / 100. 
      ELSE vat = vat * amount-foreign / 100. 
      vat-foreign = round(vat, 2). 
      IF double-currency THEN 
        vat = round(vat * exchg-rate, price-decimal). 
      ELSE vat = round(vat, price-decimal). 
 
      create bill-line.
      ASSIGN
        bill-line.rechnr = bill.rechnr
        bill-line.artnr = artikel1.artnr
        bill-line.bezeich = artikel1.bezeich 
        bill-line.anzahl = 1
        bill-line.fremdwbetrag = vat-foreign
        bill-line.betrag = vat
        bill-line.zinr = res-line.zinr
        bill-line.departement = artikel1.departement 
        bill-line.epreis = 0
        bill-line.zeit = currZeit + 2 
        bill-line.userinit = user-init 
        bill-line.arrangement = res-line.arrangement 
        bill-line.bill-datum = bill-date
        bill-line.massnr = res-line.resnr
        bill-line.billin-nr = res-line.reslinnr
      .
      FIND CURRENT bill-line NO-LOCK. 
 
      FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
        AND umsatz.departement = artikel.departement 
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE umsatz THEN 
      DO: 
        create umsatz. 
        umsatz.artnr = artikel1.artnr. 
        umsatz.datum = bill-date. 
        umsatz.departement = artikel1.departement. 
      END. 
      umsatz.betrag = umsatz.betrag + vat. 
      umsatz.anzahl = umsatz.anzahl + 1. 
      FIND CURRENT umsatz NO-LOCK. 
 
      create billjournal. 
      billjournal.rechnr = bill.rechnr. 
      billjournal.artnr = artikel1.artnr. 
      billjournal.anzahl = 1. 
      billjournal.fremdwaehrng = vat-foreign. 
      billjournal.betrag = vat. 
      billjournal.bezeich = artikel1.bezeich. 
      billjournal.zinr = res-line.zinr. 
      billjournal.departement = artikel1.departement. 
      billjournal.epreis = 0. 
      billjournal.zeit = currZeit + 2. 
      billjournal.stornogrund = "". 
      billjournal.userinit = user-init. 
      billjournal.bill-datum = bill-date. 
      FIND CURRENT billjournal NO-LOCK. 
    END. 
  END. 
 
  bill.saldo = bill.saldo + vat + service. 
  bill.mwst[99] = bill.mwst[99] + vat-foreign + service-foreign. 
END. 
{ master-taxserv.i } 
