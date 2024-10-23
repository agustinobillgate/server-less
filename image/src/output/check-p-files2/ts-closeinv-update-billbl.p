
DEFINE TEMP-TABLE t-h-bill  LIKE h-bill
    FIELD rec-id AS INT.

DEFINE INPUT-OUTPUT PARAMETER amount LIKE vhp.bill-line.betrag.
DEFINE INPUT-OUTPUT PARAMETER amount-foreign LIKE vhp.bill-line.betrag.
DEFINE INPUT-OUTPUT PARAMETER balance AS DECIMAL.

DEFINE INPUT PARAMETER rec-bill-guest   AS INT.
DEFINE INPUT PARAMETER foreign-rate     AS LOGICAL.
DEFINE INPUT PARAMETER curr-dept        AS INT.
DEFINE INPUT PARAMETER rec-h-artikel    AS INT.
DEFINE INPUT PARAMETER rec-h-bill       AS INT.
DEFINE INPUT PARAMETER h-artart         AS INTEGER. 
DEFINE INPUT PARAMETER h-artnrfront     AS INTEGER. 
DEFINE INPUT PARAMETER unit-price       AS DECIMAL.
DEFINE INPUT PARAMETER double-currency  AS LOGICAL.
DEFINE INPUT PARAMETER exchg-rate       AS DECIMAL.
DEFINE INPUT PARAMETER price-decimal    AS INT.
DEFINE INPUT PARAMETER qty              AS INT.
DEFINE INPUT PARAMETER kreditlimit      AS DECIMAL.
DEFINE INPUT PARAMETER billart          AS INT.
DEFINE INPUT PARAMETER description      AS CHAR.
DEFINE INPUT PARAMETER change-str       AS CHAR.
DEFINE INPUT PARAMETER nett-amount      LIKE vhp.h-bill-line.betrag.
DEFINE INPUT PARAMETER tischnr          AS INT.
DEFINE INPUT PARAMETER price            LIKE vhp.bill-line.epreis.
DEFINE INPUT PARAMETER bill-date        AS DATE.
DEFINE INPUT PARAMETER b-list-departement AS INT.
DEFINE INPUT PARAMETER avail-b-list     AS LOGICAL.
DEFINE INPUT PARAMETER cc-comment       AS CHAR.
DEFINE INPUT PARAMETER b-list-waehrungsnr AS INT.
DEFINE INPUT PARAMETER hoga-card        AS CHAR.
DEFINE INPUT PARAMETER cancel-str       AS CHAR.
DEFINE INPUT PARAMETER req-str          AS CHAR.
DEFINE INPUT PARAMETER curr-waiter      AS INT.
DEFINE INPUT PARAMETER pay-type         AS INT.
DEFINE INPUT PARAMETER transfer-zinr    AS CHAR.
DEFINE INPUT PARAMETER curr-room        AS CHAR.
DEFINE INPUT PARAMETER user-init        AS CHAR.
DEFINE INPUT PARAMETER deptname         AS CHAR.

DEFINE OUTPUT PARAMETER service-foreign LIKE vhp.h-bill-line.betrag INITIAL 0.
DEFINE OUTPUT PARAMETER mwst-foreign LIKE vhp.h-bill-line.betrag INITIAL 0.
DEFINE OUTPUT PARAMETER service LIKE vhp.h-bill-line.betrag INITIAL 0.
DEFINE OUTPUT PARAMETER mwst LIKE vhp.h-bill-line.betrag INITIAL 0.
DEFINE OUTPUT PARAMETER bcol AS INT INIT 2.
DEFINE OUTPUT PARAMETER balance-foreign AS DECIMAL.
DEFINE OUTPUT PARAMETER closed AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

DEFINE VARIABLE h-service AS DECIMAL.
DEFINE VARIABLE h-service-foreign AS DECIMAL.
DEFINE VARIABLE h-mwst AS DECIMAL.
DEFINE VARIABLE h-mwst-foreign AS DECIMAL.
DEFINE VARIABLE sysdate AS DATE. 
DEFINE VARIABLE zeit AS INTEGER. 

FIND FIRST h-artikel WHERE RECID(h-artikel) = rec-h-artikel NO-ERROR.
FIND FIRST h-bill WHERE RECID(h-bill) = rec-h-bill.

FIND FIRST vhp.htparam WHERE paramnr = 135 NO-LOCK. 
IF NOT vhp.htparam.flogical /* service NOT included */ 
  AND h-artart = 0 AND vhp.h-artikel.service-code NE 0 THEN 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr 
    = vhp.h-artikel.service-code NO-LOCK. 
  IF vhp.htparam.fdecimal NE 0 THEN 
  DO: 
    h-service = unit-price * vhp.htparam.fdecimal / 100. 
    h-service-foreign = ROUND(h-service, 2). 
    IF double-currency THEN 
      h-service = ROUND(h-service * exchg-rate, price-decimal). 
    ELSE h-service = ROUND(h-service, price-decimal). 
    service = service + h-service * qty. 
    service-foreign = service-foreign + h-service-foreign * qty. 
  END. 
END. 

FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK. 
IF NOT vhp.htparam.flogical /* mwst NOT included */ 
  AND h-artart = 0 AND vhp.h-artikel.mwst-code NE 0 THEN 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr 
    = vhp.h-artikel.mwst-code NO-LOCK. 
  IF vhp.htparam.fdecimal NE 0 THEN 
  DO: 
    h-mwst = vhp.htparam.fdecimal. 
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 479 NO-LOCK. 
    IF vhp.htparam.flogical  /* service taxable */ THEN 
      h-mwst = h-mwst * (unit-price + h-service-foreign) / 100. 
    ELSE h-mwst = h-mwst * unit-price / 100. 
    h-mwst-foreign = ROUND(h-mwst, 2). 
    IF double-currency THEN 
      h-mwst = ROUND(h-mwst * exchg-rate, price-decimal). 
    ELSE h-mwst = ROUND(h-mwst, price-decimal). 
    mwst = mwst + h-mwst * qty. 
    mwst-foreign = mwst-foreign + h-mwst-foreign * qty. 
  END. 
END. 

amount = amount + (h-service + h-mwst) * qty. 
amount-foreign = amount-foreign 
  + (h-service-foreign + h-mwst-foreign ) * qty. 
 
DO transaction: 
  FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK NO-ERROR. 
  FIND FIRST vhp.kellne1 WHERE kellne1.kellner-nr = vhp.h-bill.kellner-nr 
    AND kellne1.departement = curr-dept NO-LOCK NO-ERROR. 

  IF h-artart EQ 0 THEN vhp.h-bill.gesamtumsatz 
    = vhp.h-bill.gesamtumsatz + amount. 
  balance = balance + amount. 
  IF balance LE kreditlimit THEN bcol = 2. 
/*    ELSE bcol = 12. */ 
  vhp.h-bill.saldo = vhp.h-bill.saldo + amount. 
  vhp.h-bill.mwst[99] = vhp.h-bill.mwst[99] + amount-foreign. 
  balance = vhp.h-bill.saldo. 
  balance-foreign = vhp.h-bill.mwst[99]. 
  IF balance NE 0 THEN vhp.h-bill.rgdruck = 0. 
  IF balance LE kreditlimit THEN bcol = 2. 
/*    ELSE bcol = 12. */ 
/* 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
  /* bill DATE */ 
  bill-date = vhp.htparam.fdate. 
*/ 
  sysdate = today. 
  zeit = time. 

  CREATE vhp.h-bill-line. 
  ASSIGN
    vhp.h-bill-line.rechnr = vhp.h-bill.rechnr
    vhp.h-bill-line.artnr = billart
    vhp.h-bill-line.bezeich = description + change-str
    vhp.h-bill-line.anzahl = qty
    vhp.h-bill-line.nettobetrag = nett-amount
    vhp.h-bill-line.fremdwbetrag = amount-foreign 
    vhp.h-bill-line.betrag = amount
    vhp.h-bill-line.tischnr = tischnr 
    vhp.h-bill-line.departement = curr-dept 
    vhp.h-bill-line.epreis = price
    vhp.h-bill-line.zeit = zeit
    vhp.h-bill-line.bill-datum = bill-date 
    vhp.h-bill-line.sysdate = sysdate
  . 
  IF avail-b-list AND 
    b-list-departement LT 999 /* 999 = deleted */ THEN
    vhp.h-bill-line.bezeich = vhp.h-bill-line.bezeich + cc-comment.

  IF avail-b-list THEN 
    vhp.h-bill-line.waehrungsnr = b-list-waehrungsnr. 
  
  IF SUBSTR(description,1,5) = "RmNo " OR SUBSTR(description,1,5) = "Card " 
    THEN vhp.h-bill-line.segmentcode = INTEGER(SUBSTR(hoga-card,1,9)). 
  FIND CURRENT vhp.h-bill-line NO-LOCK. 

  IF billart NE 0 THEN 
  DO: 
    FIND FIRST vhp.h-umsatz WHERE vhp.h-umsatz.artnr = billart 
      AND vhp.h-umsatz.departement = curr-dept 
      AND vhp.h-umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE vhp.h-umsatz THEN 
    DO: 
      CREATE vhp.h-umsatz. 
      ASSIGN
        vhp.h-umsatz.artnr = billart
        vhp.h-umsatz.datum = bill-date 
        vhp.h-umsatz.departement = curr-dept
      . 
    END.
    ASSIGN
      vhp.h-umsatz.betrag = vhp.h-umsatz.betrag + amount
      vhp.h-umsatz.anzahl = vhp.h-umsatz.anzahl + qty
    . 
    FIND CURRENT vhp.h-umsatz NO-LOCK. 
  END. 

  CREATE vhp.h-journal. 
  ASSIGN
    vhp.h-journal.rechnr = vhp.h-bill.rechnr
    vhp.h-journal.artnr = billart
    vhp.h-journal.anzahl = qty
    vhp.h-journal.fremdwaehrng = amount-foreign
  . 
  IF AVAILABLE vhp.h-artikel THEN vhp.h-journal.artart 
    = vhp.h-artikel.artart. 

  IF h-artart = 6 THEN 
  DO: 
/* 
    FIND CURRENT vhp.kellner EXCLUSIVE-LOCK. 
    vhp.kellner.nullbon = YES. 
    FIND CURRENT vhp.kellner NO-LOCK. 
*/ 
    vhp.h-journal.betrag = amount. 
    FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = vhp.h-artikel.artnrfront 
      AND vhp.umsatz.departement = 0 
      AND vhp.umsatz.datum = bill-date NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.umsatz THEN FIND CURRENT vhp.umsatz EXCLUSIVE-LOCK. 
    ELSE DO: 
      CREATE vhp.umsatz. 
      ASSIGN
        vhp.umsatz.artnr = vhp.h-artikel.artnrfront
        vhp.umsatz.datum = bill-date
        vhp.umsatz.departement = 0
      . 
    END.
    ASSIGN
      vhp.umsatz.betrag = vhp.umsatz.betrag + amount
      vhp.umsatz.anzahl = vhp.umsatz.anzahl + qty
    . 
    FIND CURRENT vhp.umsatz NO-LOCK. 
  END. 
  ELSE vhp.h-journal.betrag = amount. 

  ASSIGN
    vhp.h-journal.bezeich = description + change-str
    vhp.h-journal.tischnr = tischnr
    vhp.h-journal.departement = curr-dept 
    vhp.h-journal.epreis = price
    vhp.h-journal.zeit = zeit
    vhp.h-journal.stornogrund = cancel-str
    vhp.h-journal.aendertext = req-str
    vhp.h-journal.kellner-nr = INTEGER(user-init) /*curr-waiter */
    vhp.h-journal.bill-datum = bill-date
    vhp.h-journal.sysdate = sysdate
    vhp.h-journal.artnrfront = h-artnrfront
  . 
  IF avail-b-list AND b-list-departement LT 999 /* 999 = deleted */ THEN
    vhp.h-journal.bezeich = vhp.h-journal.bezeich + cc-comment.
  
  IF billart = 0 THEN vhp.h-journal.artart = 0. 
  ELSE vhp.h-journal.artart = h-artart. 
  IF pay-type = 2 THEN vhp.h-journal.zinr = transfer-zinr. 
  IF h-artart = 11 THEN 
  ASSIGN
    vhp.h-journal.aendertext = vhp.h-bill.bilname
    vhp.h-journal.segmentcode = billart
  . 
  FIND CURRENT vhp.h-journal NO-LOCK. 
  change-str = "". 

  closed = NO. 
  IF h-artart = 2 OR h-artart = 7 THEN 
  DO: 
    DEFINE buffer   bill-guest  FOR vhp.guest. 
    FIND FIRST bill-guest WHERE RECID(bill-guest) = rec-bill-guest NO-ERROR.
    FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.h-artikel.artnrfront 
      AND vhp.artikel.departement = 0 NO-LOCK. 
    IF foreign-rate AND NOT double-currency THEN 
      amount-foreign = amount / exchg-rate. 
    IF b-list-departement = 999 /* 999 = deleted */ THEN
    RUN inv-ar(artikel.artnr, curr-dept, curr-room, bill-guest.gastnr, 
      bill-guest.gastnr, vhp.h-bill.rechnr, amount, amount-foreign, 
      bill-date, bill-guest.name, user-init, ""). 
    ELSE
    RUN inv-ar(artikel.artnr, curr-dept, curr-room, bill-guest.gastnr, 
      bill-guest.gastnr, vhp.h-bill.rechnr, amount, amount-foreign, 
      bill-date, bill-guest.name, user-init, cc-comment).
  END. 
  IF h-artart = 2 OR h-artart = 7 OR h-artart = 11 
    OR h-artart = 12 THEN 
  DO: 
    IF balance = 0 THEN 
    DO: 
      closed = YES. 
      FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
      vhp.h-bill.flag = 1. 
      FIND CURRENT vhp.h-bill NO-LOCK. 
    END. 
  END. 
END. 

FIND CURRENT vhp.h-bill.
CREATE t-h-bill.
BUFFER-COPY h-bill TO t-h-bill.
ASSIGN t-h-bill.rec-id = RECID(h-bill).



procedure inv-ar:
  DEFINE INPUT PARAMETER curr-art       AS INTEGER.
  DEFINE INPUT PARAMETER curr-dept      AS INTEGER.
  DEFINE INPUT PARAMETER zinr           LIKE zimmer.zinr.
  DEFINE INPUT PARAMETER gastnr         AS INTEGER.
  DEFINE INPUT PARAMETER gastnrmember   AS INTEGER.
  DEFINE INPUT PARAMETER rechnr         AS INTEGER.
  DEFINE INPUT PARAMETER saldo          AS DECIMAL.
  DEFINE INPUT PARAMETER saldo-foreign  AS DECIMAL.
  DEFINE INPUT PARAMETER bill-DATE      AS DATE.
  DEFINE INPUT PARAMETER billname       AS CHAR.
  DEFINE INPUT PARAMETER userinit       AS CHAR FORMAT "x(2)".
  DEFINE INPUT PARAMETER voucher-nr     AS CHAR.

  DEFINE VARIABLE exchg-rate            AS DECIMAL INITIAL 1.
  DEFINE VARIABLE foreign-rate          AS LOGICAL.  
  DEFINE VARIABLE double-currency       AS LOGICAL.  
  DEFINE VARIABLE ar-license            AS LOGICAL.
  DEFINE BUFFER debt                    FOR vhp.debitor.  

  FIND FIRST vhp.htparam WHERE paramnr = 143 NO-LOCK.
  foreign-rate = vhp.htparam.fLOGICAL.

  FIND FIRST vhp.htparam WHERE paramnr = 240 NO-LOCK.
  double-currency = vhp.htparam.fLOGICAL.
  
  IF FOREIGN-RATE THEN
  DO:
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 144 NO-LOCK.
    FIND FIRST vhp.waehrung WHERE vhp.waehrung.wabkurz = htparam.fchar 
      NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.waehrung THEN exchg-rate = 
      vhp.waehrung.ankauf / vhp.waehrung.einheit.
  END.
  IF exchg-rate NE 1 THEN saldo-foreign = ROUND(saldo / exchg-rate, 2).
  
  FIND FIRST vhp.bediener WHERE vhp.bediener.userinit = userinit NO-LOCK.
  
  FIND FIRST vhp.htparam WHERE paramnr = 997 NO-LOCK.
  ar-license = vhp.htparam.flogical.

  FIND FIRST vhp.artikel WHERE vhp.artikel.departement = 0 AND 
    vhp.artikel.artnr = curr-art NO-LOCK. 

  FIND FIRST vhp.guest WHERE vhp.guest.gastnr = gastnr NO-LOCK.
  billname = vhp.guest.name + ", " + vhp.guest.vorname1 + " " 
    + vhp.guest.anrede1 + vhp.guest.anredefirma.

      
  FIND FIRST debt WHERE debt.artnr = curr-art
    AND debt.rechnr = rechnr AND debt.opart = 0 
    AND debt.betriebsnr = curr-dept
    AND debt.rgdatum = bill-DATE AND debt.counter = 0 
    AND debt.saldo = saldo NO-LOCK NO-ERROR.

  IF AVAILABLE debt THEN
  DO:
    FIND CURRENT debt EXCLUSIVE-LOCK.
    DELETE debt.
    FIND FIRST vhp.umsatz WHERE vhp.umsatz.departement = 0 
      AND vhp.umsatz.artnr = curr-art 
      AND vhp.umsatz.datum = bill-DATE EXCLUSIVE-LOCK.
    vhp.umsatz.anzahl = vhp.umsatz.anzahl - 1.
    vhp.umsatz.betrag = vhp.umsatz.betrag + saldo.
    FIND CURRENT vhp.umsatz NO-LOCK.
    RELEASE vhp.umsatz.
    CREATE vhp.billjournal.
    vhp.billjournal.rechnr = rechnr.
    vhp.billjournal.bill-datum = bill-DATE.
    vhp.billjournal.artnr = curr-art.
    vhp.billjournal.betriebsnr = curr-dept.
    vhp.billjournal.anzahl = 1.
    vhp.billjournal.betrag = saldo.
    IF double-currency THEN
      vhp.billjournal.fremdwaehrng = saldo-foreign.
    vhp.billjournal.bezeich = vhp.artikel.bezeich. 
    vhp.billjournal.zinr = zinr.
    vhp.billjournal.zeit = TIME.
    vhp.billjournal.bediener-nr = vhp.bediener.nr.
    vhp.billjournal.userinit = userinit.
    RELEASE vhp.billjournal.
    RETURN.
  END.

  IF ar-license THEN
  DO:
    IF voucher-nr NE "" THEN voucher-nr = "/" + voucher-nr.
    CREATE vhp.debitor.
    ASSIGN
      vhp.debitor.artnr           = curr-art
      vhp.debitor.betrieb-gastmem = vhp.artikel.betriebsnr
      vhp.debitor.betriebsnr      = curr-dept
      vhp.debitor.zinr            = zinr
      vhp.debitor.gastnr          = gastnr
      vhp.debitor.gastnrmember    = gastnrmember
      vhp.debitor.rechnr          = rechnr
      vhp.debitor.saldo           = - saldo
      vhp.debitor.transzeit       = TIME
      vhp.debitor.rgdatum         = bill-DATE
      vhp.debitor.bediener-nr     = vhp.bediener.nr
      vhp.debitor.name            = billname
      vhp.debitor.vesrcod         = deptname + voucher-nr
    .

    IF double-currency OR foreign-rate THEN
      vhp.debitor.vesrdep    = - saldo-foreign.

    RELEASE vhp.debitor.
  END.

  FIND FIRST vhp.umsatz WHERE vhp.umsatz.departement = 0 
    AND vhp.umsatz.artnr = curr-art 
    AND vhp.umsatz.datum = bill-DATE EXCLUSIVE-LOCK NO-ERROR.
  IF NOT AVAILABLE vhp.umsatz THEN 
  DO:
    CREATE vhp.umsatz.
    vhp.umsatz.artnr = curr-art.
    vhp.umsatz.datum = bill-DATE.
  END.
  vhp.umsatz.anzahl = vhp.umsatz.anzahl + 1.
  vhp.umsatz.betrag = vhp.umsatz.betrag + saldo.
  FIND CURRENT vhp.umsatz NO-LOCK.
  RELEASE vhp.umsatz.

  CREATE vhp.billjournal.
  vhp.billjournal.rechnr = rechnr.
  vhp.billjournal.bill-datum = bill-DATE.
  vhp.billjournal.artnr = curr-art.
  vhp.billjournal.betriebsnr = curr-dept.
  vhp.billjournal.anzahl = 1.
  vhp.billjournal.betrag = saldo.
  IF double-currency THEN
    vhp.billjournal.fremdwaehrng = saldo-foreign.
  vhp.billjournal.bezeich = vhp.artikel.bezeich. 
  vhp.billjournal.zinr = zinr.
  vhp.billjournal.zeit = TIME.
  vhp.billjournal.bediener-nr = vhp.bediener.nr.
  vhp.billjournal.userinit = userinit.
  RELEASE vhp.billjournal.
END. 
