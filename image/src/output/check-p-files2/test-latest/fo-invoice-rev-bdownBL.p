
DEF INPUT  PARAMETER bil-recid          AS INT.
DEF INPUT  PARAMETER currZeit           AS INTEGER.
DEF INPUT  PARAMETER exchg-rate         AS DECIMAL.
DEF INPUT  PARAMETER amount             AS DECIMAL.
DEF INPUT  PARAMETER t-artnr            AS INT.
DEF INPUT  PARAMETER t-dept             AS INT.
DEF INPUT  PARAMETER arran-argtnr       AS INT.
DEF INPUT  PARAMETER price-decimal      AS INT.
DEF INPUT  PARAMETER bill-date          AS DATE.
DEF INPUT  PARAMETER curr-room          AS CHAR.
DEF INPUT  PARAMETER cancel-str         AS CHAR.
DEF INPUT  PARAMETER user-init          AS CHAR.
DEF INPUT  PARAMETER curr-department    AS INT.
DEF INPUT  PARAMETER qty                AS INT.
DEF INPUT  PARAMETER double-currency    AS LOGICAL.
DEF INPUT  PARAMETER foreign-rate       AS LOGICAL.
DEF INPUT  PARAMETER price              LIKE bill-line.epreis.
DEF INPUT  PARAMETER balance-foreign    LIKE bill.saldo.
DEF OUTPUT PARAMETER balance            AS DECIMAL.

DEFINE VARIABLE rm-vat          AS LOGICAL. 
DEFINE VARIABLE rm-serv         AS LOGICAL. 
DEFINE VARIABLE service         AS DECIMAL. 
DEFINE VARIABLE vat             AS DECIMAL. 
DEFINE VARIABLE service-foreign AS DECIMAL. 
DEFINE VARIABLE vat-foreign     AS DECIMAL. 
DEFINE VARIABLE rest-betrag     AS DECIMAL. 
DEFINE VARIABLE argt-betrag     AS DECIMAL. 
DEFINE VARIABLE frate           AS DECIMAL. 

DEFINE VARIABLE p-sign          AS INTEGER INITIAL 1 NO-UNDO. 
DEFINE VARIABLE qty1            AS INTEGER NO-UNDO. 

DEFINE VARIABLE ex-rate         AS DECIMAL. 

DEFINE BUFFER artikel1 FOR artikel. 

FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK.
FIND FIRST artikel WHERE artikel.artnr = t-artnr 
    AND artikel.departement = t-dept NO-LOCK.
FIND FIRST arrangement WHERE arrangement.argtnr 
    = arran-argtnr NO-LOCK. 

FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK. 
rm-vat = NOT htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 128 NO-LOCK. 
rm-serv = NOT htparam.flogical. 

FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
    AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR. 
IF AVAILABLE res-line THEN
DO:
    IF res-line.adrflag THEN frate = 1. 
    ELSE IF res-line.reserve-dec NE 0 THEN frate = res-line.reserve-dec. 
END.
ELSE frate = exchg-rate. 
 
rest-betrag = amount. 
IF amount LT 0 THEN p-sign = -1. 
 
FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
    AND NOT argt-line.kind2 NO-LOCK:  /* kind2 = YES => fix cost e.g extrabed */ 
    RUN argt-betrag.p(RECID(res-line), RECID(argt-line), 
      OUTPUT argt-betrag, OUTPUT ex-rate). 
    argt-betrag = round(argt-betrag * ex-rate, price-decimal). 
    rest-betrag = rest-betrag - argt-betrag * p-sign. 

    IF argt-betrag NE 0 THEN 
    DO: 
      /*MT 21/09/12 */
      IF argt-line.vt-percnt = 0 THEN 
      DO:
          IF argt-line.betriebsnr = 0 THEN qty1 = res-line.erwachs * p-sign. 
          ELSE qty1 = argt-line.betriebsnr * p-sign. 
      END.
      ELSE IF argt-line.vt-percnt = 1 THEN 
      DO:
          IF argt-line.betriebsnr = 0 THEN qty1 = res-line.kind1 * p-sign.
          ELSE qty1 = argt-line.betriebsnr * p-sign. 
      END.
      ELSE IF argt-line.vt-percnt = 2 THEN 
      DO:
          IF argt-line.betriebsnr = 0 THEN qty1 = res-line.kind2 * p-sign. 
          ELSE qty1 = argt-line.betriebsnr * p-sign. 
      END.
      /*MT 21/09/12 */

      /*MT 21/09/12
      IF argt-line.betriebsnr = 0 THEN qty1 = res-line.erwachs * p-sign. 
      ELSE qty1 = argt-line.betriebsnr * p-sign. 
      */
 
      FIND FIRST artikel1 WHERE artikel1.artnr = argt-line.argt-artnr 
        AND artikel1.departement = argt-line.departement NO-LOCK. 
      FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
        AND umsatz.departement = artikel1.departement 
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE umsatz THEN 
      DO: 
        CREATE umsatz.
        ASSIGN
          umsatz.artnr = artikel1.artnr
          umsatz.datum = bill-date
          umsatz.departement = artikel1.departement
        . 
      END.
      ASSIGN
        umsatz.betrag = umsatz.betrag + argt-betrag * p-sign
        umsatz.anzahl = umsatz.anzahl + qty1
      . 
      FIND CURRENT umsatz NO-LOCK. 
      CREATE billjournal. 
      ASSIGN
        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel1.artnr 
        billjournal.anzahl = qty1
        billjournal.fremdwaehrng = argt-line.betrag * p-sign
        billjournal.betrag = argt-betrag * p-sign
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = curr-room
        billjournal.departement = artikel1.departement
        billjournal.epreis = 0
        billjournal.zeit = currZeit
        billjournal.stornogrund = cancel-str 
        billjournal.userinit = user-init
        billjournal.bill-datum = bill-date
      . 
      FIND CURRENT billjournal NO-LOCK. 
    END. 
END. 
 
FIND FIRST artikel1 WHERE artikel1.artnr = arrangement.artnr-logis 
    AND artikel1.departement = curr-department NO-LOCK. 
FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
    AND umsatz.departement = artikel1.departement 
    AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
IF NOT AVAILABLE umsatz THEN 
DO: 
    CREATE umsatz. 
    ASSIGN
      umsatz.artnr = artikel1.artnr
      umsatz.datum = bill-date
      umsatz.departement = artikel1.departement
    . 
END.
ASSIGN
    umsatz.betrag = umsatz.betrag + rest-betrag
    umsatz.anzahl = umsatz.anzahl + qty
. 
FIND CURRENT umsatz NO-LOCK. 
  
CREATE billjournal. 
ASSIGN
    billjournal.rechnr = bill.rechnr 
    billjournal.artnr = artikel1.artnr 
    billjournal.anzahl = qty
    billjournal.betrag = rest-betrag 
    billjournal.bezeich = artikel1.bezeich 
    billjournal.zinr = curr-room
    billjournal.departement = artikel1.departement 
    billjournal.epreis = 0
    billjournal.zeit = currZeit 
    billjournal.stornogrund = cancel-str 
    billjournal.userinit = user-init
    billjournal.bill-datum = bill-date
  . 
IF double-currency THEN 
    billjournal.fremdwaehrng = round(rest-betrag / exchg-rate, 6). 
FIND CURRENT billjournal NO-LOCK. 
 
IF rm-serv AND artikel.service-code NE 0 THEN 
DO: 
    FIND FIRST htparam WHERE htparam.paramnr = artikel.service-code NO-LOCK. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    DO: 
      service = htparam.fdecimal. 
      FIND FIRST htparam WHERE htparam.paramnr = 133 NO-LOCK. 
      FIND FIRST artikel1 WHERE artikel1.artnr = htparam.finteger 
        AND artikel1.departement = curr-department NO-LOCK. 
      ASSIGN
        service = service * price / 100
        service-foreign = round(service, 2) * qty
      . 
      IF double-currency THEN 
        service = round(service * exchg-rate, price-decimal) * qty. 
      ELSE service = round(service, price-decimal) * qty. 
 
      IF artikel1.umsatzart = 1 THEN
      ASSIGN
        bill.logisumsatz = bill.logisumsatz + service
        bill.argtumsatz = bill.argtumsatz + service
      . 
      ELSE IF artikel1.umsatzart = 2 
        THEN bill.argtumsatz = bill.argtumsatz + service. 
      ELSE IF (artikel1.umsatzart = 3 OR artikel1.umsatzart = 5 
        OR artikel1.umsatzart = 6) 
        THEN bill.f-b-umsatz = bill.f-b-umsatz + service. 
      ELSE IF artikel1.umsatzart = 4 
        THEN bill.sonst-umsatz = bill.sonst-umsatz + service. 
      IF artikel1.umsatzart GE 1 AND artikel1.umsatzart LE 4 THEN 
        bill.gesamtumsatz = bill.gesamtumsatz + service. 
 
      CREATE bill-line. 
      ASSIGN
        bill-line.rechnr = bill.rechnr
        bill-line.artnr = artikel1.artnr
        bill-line.bezeich = artikel1.bezeich
        bill-line.anzahl = qty
        bill-line.fremdwbetrag = service-foreign 
        bill-line.betrag = service
        bill-line.zinr = curr-room 
        bill-line.departement = artikel1.departement 
        bill-line.epreis = 0
        bill-line.zeit = currZeit + 1 
        bill-line.userinit = user-init 
        bill-line.bill-datum = bill-date
      .
      IF AVAILABLE res-line THEN bill-line.arrangement = res-line.arrangement. 
      FIND CURRENT bill-line NO-LOCK. 
 
      FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
        AND umsatz.departement = artikel1.departement 
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE umsatz THEN 
      DO: 
        CREATE umsatz. 
        ASSIGN
          umsatz.artnr = artikel1.artnr
          umsatz.datum = bill-date
          umsatz.departement = artikel1.departement
        . 
      END.
      ASSIGN 
        umsatz.betrag = umsatz.betrag + service
        umsatz.anzahl = umsatz.anzahl + qty
      . 
      FIND CURRENT umsatz NO-LOCK. 
 
      CREATE billjournal. 
      ASSIGN
        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel1.artnr 
        billjournal.anzahl = qty
        billjournal.fremdwaehrng = service-foreign
        billjournal.betrag = service
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = curr-room
        billjournal.departement = artikel1.departement
        billjournal.epreis = 0
        billjournal.zeit = currZeit + 1
        billjournal.stornogrund = cancel-str 
        billjournal.userinit = user-init
        billjournal.bill-datum = bill-date
      . 
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
        AND artikel1.departement = curr-department NO-LOCK. 
      FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
      IF htparam.flogical THEN 
        vat = vat * (price + service-foreign / qty) / 100. 
      ELSE vat = vat * price / 100. 
      vat-foreign = round(vat, 2) * qty. 
      IF double-currency THEN 
        vat = round(vat * exchg-rate, price-decimal) * qty. 
      ELSE vat = round(vat, price-decimal) * qty. 
 
      IF artikel1.umsatzart = 1 THEN
      ASSIGN 
        bill.logisumsatz = bill.logisumsatz + vat
        bill.argtumsatz = bill.argtumsatz + vat
      . 
      ELSE IF artikel1.umsatzart = 2 
        THEN bill.argtumsatz = bill.argtumsatz + vat. 
      ELSE IF (artikel1.umsatzart = 3 OR artikel1.umsatzart = 5 
        OR artikel1.umsatzart = 6) 
        THEN bill.f-b-umsatz = bill.f-b-umsatz + vat. 
      ELSE IF artikel1.umsatzart = 4 
        THEN bill.sonst-umsatz = bill.sonst-umsatz + vat. 
      IF artikel1.umsatzart GE 1 AND artikel1.umsatzart LE 4 THEN 
        bill.gesamtumsatz = bill.gesamtumsatz + vat. 
 
      CREATE bill-line. 
      ASSIGN
        bill-line.rechnr = bill.rechnr
        bill-line.artnr = artikel1.artnr 
        bill-line.bezeich = artikel1.bezeich 
        bill-line.anzahl = qty
        bill-line.fremdwbetrag = vat-foreign 
        bill-line.betrag = vat
        bill-line.zinr = curr-room 
        bill-line.departement = artikel1.departement 
        bill-line.epreis = 0
        bill-line.zeit = currZeit + 2 
        bill-line.userinit = user-init 
        bill-line.bill-datum = bill-date
      .
      IF AVAILABLE res-line THEN bill-line.arrangement = res-line.arrangement. 
      FIND CURRENT bill-line NO-LOCK. 
 
      FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
        AND umsatz.departement = artikel1.departement 
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE umsatz THEN 
      DO: 
        CREATE umsatz.
        ASSIGN
          umsatz.artnr = artikel1.artnr
          umsatz.datum = bill-date
          umsatz.departement = artikel1.departement
        . 
      END.
      ASSIGN
        umsatz.betrag = umsatz.betrag + vat
        umsatz.anzahl = umsatz.anzahl + qty
      . 
      FIND CURRENT umsatz NO-LOCK. 
 
      CREATE billjournal. 
      ASSIGN
        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel1.artnr 
        billjournal.anzahl = qty
        billjournal.fremdwaehrng = vat-foreign
        billjournal.betrag = vat
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = curr-room
        billjournal.departement = artikel1.departement 
        billjournal.epreis = 0
        billjournal.zeit = currZeit + 2 
        billjournal.stornogrund = cancel-str 
        billjournal.userinit = user-init
        billjournal.bill-datum = bill-date
      .
      FIND CURRENT billjournal NO-LOCK. 
    END. 
END. 

bill.saldo = bill.saldo + vat + service. 
IF price-decimal = 0 AND bill.saldo LE 0.4 AND bill.saldo GE -0.4 THEN 
    bill.saldo = 0. 
 
IF double-currency OR foreign-rate THEN bill.mwst[99] = 
    bill.mwst[99] + vat-foreign + service-foreign. 
balance = bill.saldo. 
IF double-currency OR foreign-rate THEN balance-foreign = bill.mwst[99].
