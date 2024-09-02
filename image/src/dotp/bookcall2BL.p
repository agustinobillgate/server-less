 
/***************************************************************************\ 
***************************************************************************** 
**  Program: bookcall2.p 
**       BY: Stephen Yie 
**     DATE: 11/05/00 
** Descript: Generate calls charges from a non posted calls. 
** 
** 
** Document: 
**   Variables: 
**   Structures: 
** 
** Updates: 
***************************************************************************** 
99/07/21: IF NOT double-currency THEN set amount-foreign = 0. 
\***************************************************************************/ 
 
DEFINE INPUT  PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER zinr         AS CHAR. 
DEFINE INPUT PARAMETER calldate     AS DATE. 
DEFINE INPUT PARAMETER calltime     AS INTEGER. 
DEFINE INPUT PARAMETER destination  AS CHAR. 
DEFINE INPUT PARAMETER duration     AS INTEGER. 
DEFINE INPUT PARAMETER rufnummer    AS CHAR. 
DEFINE INPUT PARAMETER amount       AS DECIMAL. 
DEFINE INPUT PARAMETER user-init    AS CHAR. 
DEFINE OUTPUT PARAMETER success     AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER rechnr      AS INTEGER INITIAL 0. 

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "bookcall2". 
/* 
DEFINE VARIABLE zinr AS CHAR INITIAL "310". 
DEFINE VARIABLE calldate AS DATE INITIAL 08/29/99. 
DEFINE VARIABLE calltime AS INTEGER. 
calltime = time. 
DEFINE VARIABLE destination AS CHAR INITIAL "JAKARTA". 
DEFINE VARIABLE duration AS INTEGER INITIAL 90. 
DEFINE VARIABLE rufnummer AS CHAR INITIAL "02114513678". 
DEFINE VARIABLE amount AS DECIMAL INITIAL 2000. 
DEFINE VARIABLE success AS LOGICAL INITIAL NO. 
DEFINE VARIABLE rechnr AS INTEGER INITIAL 0. 
DEFINE NEW SHARED VARIABLE user-init AS CHAR INITIAL "SY". 
*/ 
DEFINE buffer bill1 FOR bill. 
DEFINE VARIABLE bil-recid   AS INTEGER. 
DEFINE VARIABLE epreis      AS DECIMAL INITIAL 0. 
DEFINE VARIABLE artnr       AS INTEGER. 
DEFINE VARIABLE resnr       AS INTEGER. 
DEFINE VARIABLE billno      AS INTEGER. 
DEFINE VARIABLE master-flag AS LOGICAL. 
DEFINE VARIABLE bill-date   AS DATE. 
DEFINE VARIABLE usr-init    AS CHAR. 
DEFINE VARIABLE bookflag    AS INTEGER. 
 
DEFINE VARIABLE price-decimal   AS INTEGER INITIAL 0. 
DEFINE VARIABLE foreign-rate    AS LOGICAL. 
DEFINE VARIABLE double-currency AS LOGICAL. 
DEFINE VARIABLE exchg-rate      AS DECIMAL INITIAL 1. 
DEFINE VARIABLE amount-foreign  AS DECIMAL INITIAL 0. 
 
/* calls-type: 0 local, 1 long distance, 2 overseas */
DEFINE VARIABLE calls-type AS INTEGER INITIAL 0 NO-UNDO. 

IF zinr = "" THEN RETURN.

/* try FIRST WITH the main guest */ 
FIND FIRST res-line WHERE res-line.resstatus = 6 AND res-line.zinr = zinr 
  NO-LOCK NO-ERROR. 
IF NOT AVAILABLE res-line THEN 
DO: 
/* try now WITH a room sharer, according TO the algorithm it should NOT exist, 
   but still try */ 
  FIND FIRST res-line WHERE res-line.resstatus = 13 
    AND res-line.zinr = zinr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE res-line THEN RETURN. 
END. 
resnr = res-line.resnr. 
 
IF SUBSTRING(rufnummer,1,2) = "00" THEN calls-type = 2.
ELSE IF SUBSTR(rufnummer,1,1) = "0" THEN calls-type = 1.

/* artnr FOR telephone */ 
FIND FIRST htparam WHERE paramnr = 113 NO-LOCK. 
artnr = htparam.finteger. 
FIND FIRST artikel WHERE artikel.artnr = artnr 
  AND artikel.departement = 0 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE artikel THEN RETURN. 
 
IF calls-type = 1 THEN
do:
  FIND FIRST htparam WHERE paramnr = 114 NO-LOCK.
  FIND FIRST artikel WHERE artikel.artnr = htparam.finteger
    AND artikel.departement = 0 AND artikel.artart = 0 NO-LOCK NO-ERROR.
  IF AVAILABLE artikel THEN artnr = htparam.finteger.
end.
ELSE IF calls-type = 2 THEN
do:
  FIND FIRST htparam WHERE paramnr = 115 NO-LOCK.
  FIND FIRST artikel WHERE artikel.artnr = htparam.finteger
    AND artikel.departement = 0 AND artikel.artart = 0 NO-LOCK NO-ERROR.
  IF AVAILABLE artikel THEN artnr = htparam.finteger.
  ELSE
  DO:
    FIND FIRST htparam WHERE paramnr = 114 NO-LOCK.
    FIND FIRST artikel WHERE artikel.artnr = htparam.finteger
      AND artikel.departement = 0 AND artikel.artart = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE artikel THEN artnr = htparam.finteger.
  END.
END.

FIND FIRST bill1 WHERE bill1.zinr = res-line.zinr 
  AND bill1.reslinnr = res-line.reslinnr 
  AND bill1.resnr = res-line.resnr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE bill1 THEN RETURN. 
 
FIND FIRST htparam WHERE paramnr = 335 NO-LOCK. 
billno = htparam.finteger. 
IF billno = 0 THEN billno = 1. 
IF billno GT 2 THEN billno = 2. 
 
FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.   /* bill DATE */ 
bill-date = htparam.fdate. 
FIND FIRST htparam WHERE htparam.paramnr = 317 NO-LOCK.   /* System User-ID */ 
usr-init = htparam.fchar. 
FIND FIRST htparam WHERE htparam.paramnr = 559 NO-LOCK. 
  /* Holdback the 3 LAST digits */ 
IF htparam.flogical AND length(rufnummer) GT 3 THEN 
  rufnummer = SUBSTR(rufnummer, 1, length(rufnummer) - 3). 
 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK.   /* DECIMAL Place */ 
price-decimal = htparam.finteger. 
 
amount-foreign = 0. 
FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK. 
foreign-rate = htparam.flogical. 
FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = htparam.flogical. 
 
IF foreign-rate OR double-currency THEN 
DO: 
  IF artikel.pricetab AND artikel.betriebsnr NE 0 THEN 
  DO: 
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr 
      AND waehrung.ankauf NE 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
  ELSE 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
END. 
 
IF double-currency THEN 
DO: 
  amount-foreign = amount. 
  amount = amount * exchg-rate. 
END. 
ELSE IF foreign-rate THEN 
DO: 
  amount-foreign = amount / exchg-rate. 
END. 
amount = round(amount, price-decimal). 
 
DO: 
  IF billno GT 1 THEN 
  DO: 
    FIND bill WHERE bill.resnr = bill1.resnr AND bill.parent-nr = bill1.parent-nr 
      AND bill.billnr = billno AND bill.flag = 0 AND bill.zinr = bill1.zinr 
      EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE bill THEN 
    DO: 
      RUN create-newbillbl.p (INPUT RECID(res-line), INPUT bill1.parent-nr, 
        INPUT billno, OUTPUT bil-recid). 
      FIND FIRST bill WHERE RECID(bill) = bil-recid EXCLUSIVE-LOCK. 
    END. 
  END. 
  ELSE FIND FIRST bill WHERE RECID(bill) = RECID(bill1) EXCLUSIVE-LOCK. 
  bill.sonst-umsatz = bill.sonst-umsatz + amount. 
  bill.gesamtumsatz = bill.gesamtumsatz + amount. 
  bill.rgdruck = 0. 
  bill.saldo = bill.saldo + amount. 
  bill.mwst[99] = bill.mwst[99] + amount-foreign. 
  bill.datum = bill-date. 
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
    bill-line.massnr = bill.resnr 
    bill-line.billin-nr = bill.reslinnr 
    bill-line.artnr = artnr
    bill-line.bezeich = artikel.bezeich + " - " 
      + SUBSTR(rufnummer, 1, length(rufnummer))
    bill-line.anzahl = 1 
    bill-line.betrag = amount
    bill-line.fremdwbetrag = amount-foreign 
    bill-line.zinr = zinr
    bill-line.departement = artikel.departement
    bill-line.epreis = epreis
    bill-line.zeit = TIME
    bill-line.userinit = usr-init
    bill-line.arrangement = res-line.arrangement
    bill-line.bill-datum = bill-date
    bill-line.origin-id = "CALLS" + " " + STRING(calldate) + ";" 
      + STRING(calltime,"HH:MM") + ";" + rufnummer + ";" 
      + destination + ";" + STRING(duration,"HH:MM:SS") + ";"
  . 
  FIND CURRENT bill-line NO-LOCK. 
 
  FIND FIRST umsatz WHERE umsatz.artnr = artnr AND umsatz.departement = 0 
    AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    create umsatz. 
    umsatz.artnr = artnr. 
    umsatz.datum = bill-date. 
    umsatz.departement = 0. 
  END. 
  umsatz.betrag = umsatz.betrag + amount. 
  umsatz.anzahl = umsatz.anzahl + 1. 
  FIND CURRENT umsatz NO-LOCK. 
 
  create billjournal. 
  billjournal.rechnr = bill.rechnr. 
  billjournal.artnr = artnr. 
  billjournal.anzahl = 1. 
  billjournal.betrag = amount. 
  billjournal.fremdwaehrng = amount-foreign. 
  billjournal.bezeich = artikel.bezeich + " - " 
    + SUBSTR(rufnummer, 1, length(rufnummer)). 
  billjournal.zinr = zinr. 
  billjournal.departement = artikel.departement. 
  billjournal.epreis = epreis. 
  billjournal.zeit = time. 
  billjournal.userinit = user-init. 
  billjournal.bill-datum = bill-date. 
  FIND CURRENT billjournal NO-LOCK. 
 
  FIND CURRENT bill NO-LOCK NO-ERROR. 
  success = YES. 
  rechnr = bill.rechnr. 
END. 
 
